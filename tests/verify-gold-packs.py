"""Independent integer and route-enumeration checks through real C++ file I/O."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import random
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKS = {'UG1-Dynamic-Programming-with-Fibonacci': 'fibonacci', 'UG5-Marathon': 'marathon'}


def route_length(points):
    return sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(points,points[1:]))


def marathon_case(original, commands):
    points = list(original)
    answers = []
    for command in commands:
        if command[0] == 'U':
            points[command[1]-1] = (command[2], command[3])
        else:
            a,b = command[1]-1, command[2]-1
            path = points[a:b+1]
            candidates = [path] + [path[:i]+path[i+1:] for i in range(1,len(path)-1)]
            answers.append(min(route_length(candidate) for candidate in candidates))
    text = f'{len(original)} {len(commands)}\n' + ''.join(f'{x} {y}\n' for x,y in original)
    text += ''.join(' '.join(map(str,row))+'\n' for row in commands)
    return text, answers


def fixtures(folder):
    if folder == 'UG1-Dynamic-Programming-with-Fibonacci':
        for n in range(93):
            # F(n) counts tilings of length n-1 by pieces of size one and two.
            expected = 0 if n == 0 else sum(math.comb(n-1-k,k) for k in range((n-1)//2+1))
            if n == 92:
                assert expected == 7540113804746346429
            yield str(n)+'\n',[expected]
        return
    sample = marathon_case([(-4,4),(-5,-3),(-1,5),(-3,4),(0,5)],
                           [('Q',1,5),('U',4,0,1),('U',4,-1,1),('Q',2,4),('Q',1,4)])
    assert sample[1] == [11,8,8]
    yield sample
    for original in [[(0,0)],[(0,0),(0,0)],[(0,0),(1000,-1000)],
                     [(0,0),(1,0),(2,0),(3,0)],[(0,0),(1000,1000),(0,0)]]:
        n = len(original)
        commands = [('Q',a,b) for a in range(1,n+1) for b in range(a,n+1)]
        for index,x,y in [(1,1000,-1000),(n,-1000,1000),(1,0,0),(n,0,0)]:
            commands.append(('U',index,x,y))
            commands += [('Q',a,b) for a in range(1,n+1) for b in range(a,n+1)]
        yield marathon_case(original,commands)
    rng = random.Random(495)
    for _ in range(100):
        n = rng.randint(1,18)
        original = [(rng.randint(-8,8),rng.randint(-8,8)) for _ in range(n)]
        commands = []
        for _ in range(70):
            if rng.randrange(3) == 0:
                commands.append(('U',rng.randint(1,n),rng.randint(-8,8),rng.randint(-8,8)))
            else:
                a = rng.randint(1,n)
                commands.append(('Q',a,rng.randint(a,n)))
        yield marathon_case(original,commands)
    # At full scale only the middle checkpoint moves. All other points coincide;
    # skipping the sole interior detour leaves distance zero. Endpoint-protected
    # queries keep its distance. This oracle does not reuse tree/gain operations.
    n,q,middle = 100000,100000,50000
    commands,answers = [],[]
    for cycle in range(q//5):
        x = (cycle % 2001)-1000
        y = 1000-(cycle*37 % 2001)
        distance = abs(x)+abs(y)
        commands += [('U',middle,x,y),('Q',1,n),('Q',middle,middle+1),('Q',1,middle),('Q',middle,middle)]
        answers += [0,distance,distance,0]
    text = f'{n} {q}\n' + '0 0\n'*n + ''.join(' '.join(map(str,row))+'\n' for row in commands)
    yield text,answers


def verify(compiler,mode):
    flags = ['-std=c++20','-Wall','-Wextra','-Wpedantic','-Werror','-O1']
    if mode == 'sanitized':
        flags += ['-g','-fsanitize=address,undefined','-fno-omit-frame-pointer']
        if os.uname().sysname == 'Linux':
            flags += ['-fno-pie','-no-pie']
    leaks = '1' if os.uname().sysname == 'Linux' else '0'
    environment = {**os.environ,'ASAN_OPTIONS':'detect_leaks='+leaks+':halt_on_error=1','UBSAN_OPTIONS':'halt_on_error=1:print_stacktrace=1'}
    results = []
    with tempfile.TemporaryDirectory(prefix='gold-native-') as directory:
        working = Path(directory)
        for folder,basename in PACKS.items():
            binary,learner = working/(basename+'-reference'),working/(basename+'-learner')
            reference_source,starter_source = ROOT/folder/'solution/main.cpp',ROOT/folder/'starter/main.cpp'
            subprocess.run([compiler,*flags,str(reference_source),'-o',str(binary)],check=True,timeout=90)
            subprocess.run([compiler,*flags,str(starter_source),'-o',str(learner)],check=True,timeout=90)
            input_file,output_file = working/(basename+'.in'),working/(basename+'.out')
            count=queries=0
            for text,expected in fixtures(folder):
                input_file.write_text(text);output_file.unlink(missing_ok=True)
                process=subprocess.run([str(binary)],cwd=working,env=environment,capture_output=True,text=True,timeout=15)
                assert process.returncode==0,(folder,count,process.stderr)
                actual=output_file.read_text().split()
                assert actual==list(map(str,expected)),(folder,count,actual[:15],expected[:15])
                count+=1;queries+=len(expected)
            invalid_indices=0
            if basename=='fibonacci':
                for text in ['-1\n','93\n','not-an-index\n']:
                    input_file.write_text(text);output_file.unlink(missing_ok=True)
                    process=subprocess.run([str(binary)],cwd=working,env=environment,capture_output=True,text=True,timeout=15)
                    assert process.returncode==2 and '0 through 92' in process.stderr,(process.returncode,process.stderr)
                    assert not output_file.exists()
                    invalid_indices+=1
            input_file.write_bytes((ROOT/folder/'starter'/(basename+'.in')).read_bytes())
            output_file.unlink(missing_ok=True)
            process=subprocess.run([str(learner)],cwd=working,env=environment,capture_output=True,text=True,timeout=15)
            assert process.returncode==2 and 'Complete ' in process.stderr,(folder,process.returncode,process.stderr)
            assert not output_file.exists(),'Untouched starter must not create a completed answer'
            results.append({'folder':folder,'fileIOCases':count,'outputRecords':queries,'independentOracle':True,
                            'maximumSizeCase':True,'starterUnfinished':True,'invalidIndexCases':invalid_indices,
                            'referenceSha256':hashlib.sha256(reference_source.read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
                            'starterSha256':hashlib.sha256(starter_source.read_bytes().replace(b'\r\n',b'\n')).hexdigest()})
    print(json.dumps({'compiler':compiler,'mode':mode,'packs':results},sort_keys=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--compiler',default='c++')
    parser.add_argument('--mode',choices=['ordinary','sanitized'],default='ordinary')
    args=parser.parse_args()
    verify(args.compiler,args.mode)
