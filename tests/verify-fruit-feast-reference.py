"""Check native answers against independent state search and explicit traces."""
import argparse
from collections import deque
import datetime
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'UG40-Fruit-Feast/solution/Main.java'
TASK = os.environ.get('CLASSES_FAMILY_TASK_ID','gold-fruit-feast-reference')

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def run(command,cwd):
    child = subprocess.Popen(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    record = dict(parentTaskId=TASK,cwd=str(cwd),command=command,pid=child.pid,startTime=now(),timeoutSeconds=45)
    print(json.dumps(dict(event='start',**record)),flush=True)
    try:
        out,err = child.communicate(timeout=45)
        assert child.returncode == 0 and not err, (child.returncode,err.decode())
        return out.decode().replace('\r\n','\n')
    except BaseException:
        if child.poll() is None:
            os.killpg(child.pid,signal.SIGTERM)
            try:
                child.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid,signal.SIGKILL)
                child.communicate()
        record['childProcessGroupCleanup'] = True
        raise
    finally:
        print(json.dumps(dict(event='end',**record,endTime=now(),exitCode=child.returncode)),flush=True)

def oracle(t,a,b):
    seen = {(0,False)}
    queue = deque(seen)
    while queue:
        fullness,water = queue.popleft()
        candidates = [(fullness+a,water),(fullness+b,water)]
        if not water:
            candidates.append((fullness//2,True))
        for state in candidates:
            if state[0] <= t and state not in seen:
                seen.add(state)
                queue.append(state)
    return max(x[0] for x in seen)

def verify(javac,java):
    original = SOURCE.read_bytes()
    preserved = {name:(SOURCE.parent/name).read_bytes() for name in ['Main.java','feast.in','feast.out'] if (SOURCE.parent/name).exists()}
    small = [(8,5,6),(1,1,1),(7,4,6),(20,6,9),(25,8,11),(11,11,11),
             (19,3,7),(30,13,17),(2,2,2),(9,6,6),(23,5,8),(17,4,9)]
    cases = [(case,oracle(*case)) for case in small]
    cases += [((5000000,2,3),5000000),((5000000,1,1),5000000),((5000000,4999999,4999998),4999999)]
    with tempfile.TemporaryDirectory(prefix='gold-fruit-feast-reference-') as temp:
        directory = Path(temp)
        (directory/'Main.java').write_bytes(original)
        run([javac,'--release','17','-encoding','UTF-8','-Xlint:all','-Werror','Main.java'],directory)
        for case,expected in cases:
            (directory/'feast.in').write_text(' '.join(map(str,case))+'\n')
            assert run([java,'-Xmx256m','Main'],directory) == '', case
            assert (directory/'feast.out').read_text().strip() == str(expected),case
        (directory/'feast.in').write_text('8 5 6\n')
        trace = run([java,'-Xmx256m','Main','--trace'],directory)
        assert trace == ''.join(str(value)+'\n' for value in range(9))
        assert (directory/'feast.out').read_text().strip() == '8'
    assert SOURCE.read_bytes() == original
    assert all((SOURCE.parent/name).read_bytes()==data for name,data in preserved.items())
    print(json.dumps(dict(event='gold-fruit-feast-reference-accepted',parentTaskId=TASK,
                          validReferenceCases=15,independentSmallStateBfsCases=12,
                          maximumFullness=5000000,largeReferenceCases=3,traceCases=1,
                          normalStdoutEmpty=True,optionalTraceExplicit=True,
                          sourceFilesUnchanged=True,inputAndUnrelatedWorkPreserved=True,
                          referenceGitSha256=hashlib.sha256(original.replace(b'\r\n',b'\n')).hexdigest(),
                          formalJudgePerformanceClaim=False,restoredLearner=False)),flush=True)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--javac',default='javac')
    parser.add_argument('--java',default='java')
    args = parser.parse_args()
    try:
        verify(args.javac,args.java)
    finally:
        print(json.dumps(dict(event='cleanup',parentTaskId=TASK,pid=os.getpid(),time=now())),flush=True)
