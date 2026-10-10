"""Native Gold references, independent driver oracles, and unfinished learners."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
TASK = 'gold-ordering-native-source-acceptance'
SPECS = [dict(folder='UG24-Why-Did-the-Cow-Cross-the-Road-III', stem='circlecross',
              sha='ea1f4bdf621a01ca72097485451c193b4ad6a92304e848085da1dd1df74ec34c', tasks=5,
              unfinished='Complete the five CircleCross tasks before producing an answer'),
         dict(folder='UG27-Snow-Boots', stem='snowboots',
              sha='e184f5769e7aeb4e18808e1bd2c4aa26647e9ef25acffc7caa1b4e05ba948069', tasks=6,
              unfinished='Complete the six Snow Boots tasks before producing an answer')]


def run(command, cwd, timeout=30):
    child = subprocess.Popen(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
    print(json.dumps(dict(event='start', parentTaskId=TASK, cwd=str(cwd), command=command,
                          pid=child.pid, startTime=time.time(), timeoutSeconds=timeout)), flush=True)
    try:
        out, err = child.communicate(timeout=timeout)
    except BaseException:
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        child.communicate()
        print(json.dumps(dict(event='cleanup', parentTaskId=TASK, pid=child.pid,
                              endTime=time.time(), exitCode=child.returncode,
                              childProcessGroupCleanup='terminated')), flush=True)
        raise
    print(json.dumps(dict(event='end', parentTaskId=TASK, pid=child.pid,
                          endTime=time.time(), exitCode=child.returncode,
                          childProcessGroupCleanup='exited')), flush=True)
    return subprocess.CompletedProcess(command, child.returncode, out, err)


def circle_case(labels):
    n = len(labels) // 2
    positions = {cow:[] for cow in range(1, n+1)}
    for i, cow in enumerate(labels):
        positions[cow].append(i)
    assert all(len(p) == 2 for p in positions.values())
    intervals = list(positions.values())
    total = 0
    for i, (a, b) in enumerate(intervals):
        for c, d in intervals[i+1:]:
            total += (a < c < b) != (a < d < b)
    return str(n) + '\n' + ''.join(str(cow)+'\n' for cow in labels), str(total)+'\n'


def snow_case(depths, boots):
    answers = []
    for depth, step in boots:
        reachable = [False] * len(depths)
        reachable[0] = True
        for i in range(len(depths)):
            if reachable[i]:
                for j in range(i+1, min(len(depths), i+step+1)):
                    if depths[j] <= depth:
                        reachable[j] = True
        answers.append(int(reachable[-1]))
    text = f'{len(depths)} {len(boots)}\n' + ' '.join(map(str, depths)) + '\n'
    text += ''.join(f'{depth} {step}\n' for depth, step in boots)
    return text, ''.join(str(answer)+'\n' for answer in answers)


def fixtures(stem, sample):
    rng = random.Random(20261010)
    if stem == 'circlecross':
        small = [circle_case([3,2,4,4,1,3,2,1]), circle_case([1,1]),
                 circle_case([1,1,2,2]), circle_case([1,2,2,1]), circle_case([1,2,1,2])]
        for _ in range(25):
            n = rng.randint(2,25)
            labels = list(range(1,n+1)) * 2
            rng.shuffle(labels)
            small.append(circle_case(labels))
        text, expected = small[0]
        labels = [3,2,4,4,1,3,2,1]
        rotated = circle_case(labels[3:]+labels[:3])
        reversed_case = circle_case(list(reversed(labels)))
        relabeled = circle_case([5-i for i in labels])
        assert rotated[1] == reversed_case[1] == relabeled[1] == expected
        small.extend([rotated, reversed_case, relabeled])
        n = 50000
        ordered = list(range(1,n+1))
        maximum = str(n*(n-1)//2)+'\n'
        large = [(str(n)+'\n'+''.join(str(x)+'\n' for x in ordered*2), maximum),
                 (str(n)+'\n'+''.join(str(x)+'\n' for x in ordered+list(reversed(ordered))), '0\n'),
                 (str(n)+'\n'+''.join(f'{x}\n{x}\n' for x in ordered), '0\n')]
        invalid = ['', '0\n', '50001\n', '2 extra\n', 'N\n', '1\n1\n',
                   '1\n0\n1\n', '1\n1\n2\n', '2\n1\n1\n1\n2\n',
                   '2\n1\n2\n2\n2\n', '1\n1 1\n1\n', '1\n1.5\n1\n',
                   '1\n999999999999999999999\n1\n', sample+'late-invalid\n']
        probe = '''    static long bruteForTesting(Input input) {
        int[] first = new int[input.n], last = new int[input.n];
        java.util.Arrays.fill(first, -1);
        for (int i = 0; i < input.labels.length; i++) {
            int cow = input.labels[i];
            if (first[cow] < 0) first[cow] = i; else last[cow] = i;
        }
        long answer = 0;
        for (int a = 0; a < input.n; a++) {
            for (int b = a+1; b < input.n; b++) {
                boolean firstInside = first[a] < first[b] && first[b] < last[a];
                boolean lastInside = first[a] < last[b] && last[b] < last[a];
                if (firstInside != lastInside) answer++;
            }
        }
        return answer;
    }

'''
    else:
        small = [snow_case([0,3,8,5,6,9,0,0], [(0,5),(0,6),(6,2),(8,1),(10,1),(5,3),(150,7)]),
                 snow_case([0,0], [(0,1),(1000000000,1)]),
                 snow_case([0,7,0], [(6,1),(7,1),(0,2),(7,1)]),
                 snow_case([0,5,5,5,0], [(4,3),(4,4),(5,1),(0,4)]),
                 snow_case([0,0,0,0], [(0,1),(0,3),(1000000000,2)])]
        for _ in range(25):
            n = rng.randint(2,22)
            depths = [0] + [rng.choice([0,1,5,7,1000000000]) for _ in range(n-2)] + [0]
            boots = [(rng.choice([0,1,5,7,8,1000000000]), rng.randint(1,n-1)) for _ in range(20)]
            small.append(snow_case(depths, boots))
        reordered = snow_case([0,7,0], [(7,1),(0,2),(7,1),(6,1)])
        assert reordered[1] == '1\n1\n1\n0\n'
        small.append(reordered)
        n = b = 100000
        boots = [(1000000000,1) if i%3 == 0 else (0,n-1) if i%3 == 1 else (0,n-2) for i in range(b)]
        body = ''.join(f'{depth} {step}\n' for depth,step in boots)
        large = [(f'{n} {b}\n'+'0 '+'1000000000 '*(n-2)+'0\n'+body,
                  ''.join('0\n' if i%3 == 2 else '1\n' for i in range(b))),
                 (f'{n} {b}\n'+'0 '*(n-1)+'0\n'+body, '1\n'*b)]
        invalid = ['', '1 1\n0\n0 1\n', '0 1\n', '100001 1\n', '2 0\n',
                   '2 100001\n', '2 1 extra\n', 'N B\n', '2 1\n0\n0 1\n',
                   '2 1\n0 0 0\n0 1\n', '2 1\n1 0\n0 1\n', '2 1\n0 1\n0 1\n',
                   '3 1\n0 -1 0\n0 1\n', '3 1\n0 1000000001 0\n0 1\n',
                   '2 1\n0 0\n', '2 1\n0 0\n-1 1\n', '2 1\n0 0\n1000000001 1\n',
                   '2 1\n0 0\n0 0\n', '2 1\n0 0\n0 2\n', '2 1\n0 0\n0 1 extra\n',
                   '2 1\n0 0\n0 1.5\n', '2 1\n0 0\n99999999999999999 1\n',
                   sample+'late-invalid\n', '2 2\n0 0\n0 1\n0 0\n']
        probe = '''    static int[] bruteForTesting(Input input) {
        int[] answers = new int[input.boots.length];
        for (Boot boot : input.boots) {
            boolean[] reached = new boolean[input.depths.length];
            reached[0] = true;
            for (int i = 0; i < reached.length; i++) {
                if (reached[i]) {
                    for (int j = i+1; j < reached.length && j-i <= boot.step; j++) {
                        if (input.depths[j] <= boot.depth) reached[j] = true;
                    }
                }
            }
            answers[boot.index] = reached[reached.length-1] ? 1 : 0;
        }
        return answers;
    }

'''
    assert small[0][0] == sample
    return small, large, invalid, probe


def verify(spec, javac, java):
    pack = ROOT / spec['folder']
    before = {str(p.relative_to(pack)):p.read_bytes() for p in pack.rglob('*') if p.is_file()}
    original = before['solution/Main.java'].replace(b'\r\n', b'\n')
    tracked = subprocess.run(['git','show','HEAD:'+spec['folder']+'/solution/Main.java'],
                             cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    assert original == tracked and hashlib.sha256(original).hexdigest() == spec['sha']
    for role in ['starter','solution']:
        assert {p.name for p in (pack/role).iterdir()} == {'Main.java','README.md','sample.in'}
        guide = (pack/role/'README.md').read_text()
        for heading in ['Prerequisites and input','Trace and explain','Native workflow','Verify and explain']:
            assert '## '+heading in guide
    starter = (pack/'starter/Main.java').read_text()
    assert starter != (pack/'solution/Main.java').read_text()
    assert all('TASK '+str(i)+':' in starter for i in range(1,spec['tasks']+1))
    assert before['starter/sample.in'] == before['solution/sample.in']
    sample = (pack/'starter/sample.in').read_text()
    small, large, invalid, helper = fixtures(spec['stem'], sample)
    marker = 'throw new UnsupportedOperationException('+json.dumps(spec['unfinished'])+');'
    assert starter.count(marker) == 1
    probe = starter.replace(marker, 'return bruteForTesting(input);')
    probe = probe.replace('    public static void main(String[] args)', helper+'    public static void main(String[] args)')
    # The independently completed tiny probe validates the driver only. It never
    # changes or fills any task in the exported learner and is not a Gold solver.
    with tempfile.TemporaryDirectory(prefix=spec['stem']+'-source-') as temporary:
        work = Path(temporary)
        classes = {}
        for role, source in [('starter',starter),('solution',(pack/'solution/Main.java').read_text()),('driver-probe',probe)]:
            directory = work/role
            directory.mkdir()
            (directory/'Main.java').write_text(source)
            result = run([javac,'--release','17','-encoding','UTF-8','-Xlint:all','-Werror','Main.java'], directory)
            assert result.returncode == 0, result.stderr
            classes[role] = directory
        execution = work/'execution'
        execution.mkdir()
        input_path = execution/(spec['stem']+'.in')
        output_path = execution/(spec['stem']+'.out')
        unrelated = execution/'retained-attempt.txt'
        unrelated.write_bytes(b'separate saved learner work\n')
        def execute(role):
            return run([java,'-ea','-Xmx256m','-cp',str(classes[role]),'Main'], execution)
        valid = small + large + [(sample.replace('\n','\r\n'),small[0][1])]
        for text, expected in valid:
            input_path.write_text(text, newline='')
            output_path.write_text('old answer\n')
            result = execute('solution')
            assert result.returncode == 0 and result.stderr == '', result
            assert output_path.read_text() == expected
            if spec['stem'] == 'circlecross':
                assert result.stdout == ''
            else:
                diagnostics = result.stdout.splitlines()
                header = text.splitlines()[0].split()
                assert len(diagnostics) == int(header[1])
                assert all(1 <= int(value) < int(header[0]) for value in diagnostics)
            assert input_path.read_bytes() == text.encode()
        learner_space = (' \t'+sample.replace('\n',' \t\n').replace(' ','\t')+'\n \n', small[0][1])
        for text, expected in small+[learner_space]:
            input_path.write_text(text)
            output_path.write_text('old answer\n')
            result = execute('driver-probe')
            assert result.returncode == 0 and result.stdout == result.stderr == '', result
            assert output_path.read_text() == expected and input_path.read_text() == text
        unfinished = [sample,small[1][0],large[0][0]]
        for text in unfinished:
            input_path.write_text(text)
            for existing in [False,True]:
                if output_path.exists(): output_path.unlink()
                if existing: output_path.write_text('retained old answer\n')
                result = execute('starter')
                assert result.returncode == 2 and result.stdout == ''
                assert result.stderr == f'Cannot solve {spec["stem"]}.in: {spec["unfinished"]}\n'
                assert output_path.exists() == existing
                if existing: assert output_path.read_text() == 'retained old answer\n'
                assert input_path.read_text() == text
        for text in invalid:
            input_path.write_text(text)
            output_path.write_text('retained old answer\n')
            for role in ['starter','driver-probe']:
                result = execute(role)
                assert result.returncode == 2 and result.stdout == '' and result.stderr.startswith('Cannot solve '+spec['stem']+'.in:')
                assert output_path.read_text() == 'retained old answer\n' and input_path.read_text() == text
        input_path.unlink()
        for role in ['starter','driver-probe']:
            result = execute(role)
            assert result.returncode == 2 and result.stdout == '' and result.stderr.startswith('Cannot solve '+spec['stem']+'.in:')
            assert output_path.read_text() == 'retained old answer\n'
        assert unrelated.read_bytes() == b'separate saved learner work\n'
    assert {str(p.relative_to(pack)):p.read_bytes() for p in pack.rglob('*') if p.is_file()} == before
    receipt = dict(event='gold-ordering-pack-accepted', parentTaskId=TASK, folder=spec['folder'],
                   validReferenceCases=len(valid), tinyIndependentDriverCases=len(small)+1,
                   maximumN=50000 if spec['stem']=='circlecross' else 100000,
                   maximumBoots=100000 if spec['stem']=='snowboots' else None,
                   refusedLearnerAndDriverInputs=len(invalid), unfinishedLearnerCases=6,
                   missingInputCases=2, referencePreserved=True, referenceGitSha256=spec['sha'],
                   sourceFilesUnchanged=True, inputAndUnrelatedWorkPreserved=True,
                   historicalReferenceInvalidInputClaims=False, completedProbeGoldPerformanceClaim=False,
                   referenceStdout='silent' if spec['stem']=='circlecross' else 'widest-gap diagnostics, not answers',
                   sourceHashes={name:hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest() for name,data in before.items()})
    print(json.dumps(receipt), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--javac', default='javac')
    parser.add_argument('--java', default='java')
    args = parser.parse_args()
    for spec in SPECS:
        verify(spec, args.javac, args.java)
