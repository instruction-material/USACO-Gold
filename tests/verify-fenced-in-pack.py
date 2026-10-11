"""Accept real native role ZIPs with independent trees and a bounded Java heap."""
import argparse
import datetime
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'UG20-Fenced-In'
parser = argparse.ArgumentParser()
parser.add_argument('--javac', default='javac')
parser.add_argument('--java', default='java')
args = parser.parse_args()


def cancel(sig, frame):
    raise KeyboardInterrupt('Fenced In acceptance cancelled')


signal.signal(signal.SIGTERM, cancel)


def run(command, cwd, success=True, timeout=60):
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True, start_new_session=True)
    record = dict(event='fenced-in-command', parentTaskId=os.environ.get(
        'CLASSES_FAMILY_TASK_ID', 'gold-fenced-in-native'), cwd=str(cwd),
        command=command, pid=child.pid, startTime=datetime.datetime.now(
            datetime.timezone.utc).isoformat(), timeoutSeconds=timeout,
        childProcessGroupCleanup=False)
    try:
        stdout, stderr = child.communicate(timeout=timeout)
    except BaseException:
        os.killpg(child.pid, signal.SIGTERM)
        try:
            child.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.communicate()
        record['childProcessGroupCleanup'] = True
        raise
    finally:
        record.update(endTime=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      exitCode=child.returncode)
        print(json.dumps(record), flush=True)
    if success and child.returncode:
        raise AssertionError((command, child.returncode, stdout[-1000:], stderr[-1000:]))
    return subprocess.CompletedProcess(command, child.returncode, stdout, stderr)


def compile_role(directory, probe=False):
    run([args.javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all',
         '-Werror', 'Main.java', *(['Probe.java'] if probe else [])], directory)


def execute(directory, success=True):
    return run([args.java, '-ea', '-Xmx256m', 'Main'], directory, success)


def encoded(case):
    a, b, vertical, horizontal = case
    return f'{a} {b} {len(vertical)} {len(horizontal)}\n' + ''.join(
        f'{value}\n' for value in [*vertical, *horizontal])


def exhaustive_tree(case):
    """Enumerate every spanning subset, using flood fill rather than Kruskal/DSU."""
    a, b, vertical, horizontal = case
    xs, ys = sorted([0, *vertical, a]), sorted([0, *horizontal, b])
    columns, rows = len(xs) - 1, len(ys) - 1
    vertices = list(itertools.product(range(columns), range(rows)))
    edges = []
    for column, row in vertices:
        if column + 1 < columns:
            edges.append(((column, row), (column + 1, row), ys[row + 1] - ys[row]))
        if row + 1 < rows:
            edges.append(((column, row), (column, row + 1), xs[column + 1] - xs[column]))
    answer = None
    for subset in itertools.combinations(edges, len(vertices) - 1):
        neighbors = {v: [] for v in vertices}
        total = 0
        for first, second, weight in subset:
            neighbors[first].append(second)
            neighbors[second].append(first)
            total += weight
        seen, queue = {vertices[0]}, [vertices[0]]
        while queue:
            for neighbor in neighbors[queue.pop()]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        if len(seen) == len(vertices) and (answer is None or total < answer):
            answer = total
    assert answer is not None
    return answer


sample = (15, 15, [2, 5, 10, 6, 4], [11, 3])
tiny = [(1, 1, [], []), (1, 7, [], [2, 5]), (7, 1, [2, 5], []),
        (9, 8, [6, 2], [5, 1]), (6, 6, [4, 2], [4, 2]),
        (1000000000, 1000000000, [1], [999999999]), (7, 9, [3], [4, 1])]
rng = random.Random(1110202608)
for _ in range(20):
    a, b = rng.randint(3, 9), rng.randint(3, 9)
    tiny.append((a, b, rng.sample(range(1, a), rng.randint(0, 2)),
                 rng.sample(range(1, b), rng.randint(0, 2))))
tiny += [(b, a, horizontal, vertical) for a, b, vertical, horizontal in list(tiny)]
assert len(tiny) == 54
unit = (2001, 2001, list(range(1, 2001)), list(range(1, 2001)))
constant = (2001000, 6003000, [1000 * i for i in range(1, 2001)],
            [3000 * i for i in range(1, 2001)])
descending_positions = list(itertools.accumulate(range(2001, 1, -1)))
varied = (2003001, 4006002, list(reversed(descending_positions)),
          [2002 * i for i in range(1, 2001)])
single_column = (1000000000, 2001, [], list(range(1, 2001)))
single_row = (2001, 1000000000, list(range(1, 2001)), [])
# Uniform and one-orientation graph structures give these totals directly.
full = [(unit, 4004000), (constant, 4008000000), (varied, 4010006000),
        (single_column, 2000000000000), (single_row, 2000000000000)]
bad = [None, '', 'x\n', '0 1 0 0\n', '1000000001 1 0 0\n',
       '1 0 0 0\n', '1 1000000001 0 0\n', '3 3 -1 0\n',
       '3 3 2001 0\n', '3 3 0 -1\n', '3 3 0 2001\n',
       '3 3 1 0\n0\n', '3 3 1 0\n3\n', '3 3 2 0\n1\n1\n',
       '3 3 0 1\n0\n', '3 3 0 1\n3\n', '3 3 0 2\n1\n1\n',
       '3 3 1 0\n', '3 3 0 0\nextra\n', '3 3 1 0\nx\n',
       '9223372036854775808 3 0 0\n']
assert len(bad) == 21
tracked = {p: p.read_bytes() for p in PACK.rglob('*') if p.is_file()}
legacy = (PACK / 'legacy/Main.java').read_bytes()
assert hashlib.sha256(legacy).hexdigest() == 'bd5b6690e97f6a0c9d88b589e314f0c96adad554ed5f336415431c4fe7b3fb92'
assert hashlib.sha256(legacy.replace(b'\r\n', b'\n')).hexdigest() == 'a361fca9d6d94a77dab59a89136e21f0e0e48b1b16d1557c5d3c9fdb6748db32'
reference = (PACK / 'solution/Main.java').read_text()
learner = (PACK / 'starter/Main.java').read_text()
assert learner.count('// TODO ') == 4 and learner != reference
assert reference.count('CHANGED:') == 5 and 'long[] edges' in reference
original = legacy.decode().replace('\r\n', '\n')
assert original[original.index('    static class DisjointSets {'):original.index('    static class Edge ')] == reference[reference.index('    static class DisjointSets {'):reference.index('    public static long Kruskal()')]
for role in ['starter', 'solution']:
    guide = (PACK / role / 'README.md').read_text()
    assert all(value in guide for value in ['## Contract', '## Prediction',
        '## Tasks and walkthrough', '## State and reasoning', '## Build and run',
        '## Independent checks', 'JDK 17', 'PowerShell', 'exit status',
        'fencedin.in', 'fencedin.out', '256 MiB'])
    assert (PACK / role / 'fencedin.in').read_text() == encoded(sample)
assert (PACK / 'solution/fencedin.out').read_text() == '44\n'
counts = dict(zipRoles=0, compiledRoles=0, independentTinyCases=0,
              officialSampleCases=0, constructedFullLimitCases=0,
              unfinishedLearnerRuns=0, refusedLearnerInputs=0,
              parserProbes=0, invalidResultProbes=0)
with tempfile.TemporaryDirectory(prefix='gold-fenced-in-') as temporary:
    work = Path(temporary)
    roles = {}
    for role in ['starter', 'solution']:
        directory = work / role
        directory.mkdir()
        archive = directory / 'role.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            for path in sorted((PACK / role).iterdir()):
                if path.is_file() and path.suffix in ['.java', '.md', '.in', '.out']:
                    z.write(path, path.name)
        with zipfile.ZipFile(archive) as z:
            assert all('/' not in name and name not in ['.', '..'] for name in z.namelist())
            z.extractall(directory)
            for path in (PACK / role).iterdir():
                if path.is_file() and path.suffix in ['.java', '.md', '.in', '.out']:
                    assert (directory / path.name).read_bytes() == path.read_bytes()
        compile_role(directory)
        counts['zipRoles'] += 1
        counts['compiledRoles'] += 1
        roles[role] = directory
    directory = roles['solution']
    for case, expected in [(sample, 44), *[(v, exhaustive_tree(v)) for v in tiny], *full]:
        (directory / 'fencedin.in').write_text(encoded(case))
        (directory / 'fencedin.out').unlink(missing_ok=True)
        process = execute(directory)
        assert not process.stdout and not process.stderr
        assert (directory / 'fencedin.out').read_text() == str(expected) + '\n'
    counts.update(independentTinyCases=len(tiny), officialSampleCases=1,
                  constructedFullLimitCases=len(full))
    # Prove the original fails under the same advertised heap as the maintained role.
    old = work / 'legacy'
    old.mkdir()
    (old / 'Main.java').write_bytes(legacy)
    (old / 'fencedin.in').write_text(encoded(unit))
    compile_role(old)
    failure = execute(old, False)
    assert failure.returncode != 0 and 'OutOfMemoryError' in failure.stderr
    assert not (old / 'fencedin.out').exists()
    directory = roles['starter']
    previous = b'preserve the earlier learner answer\n'
    for case in [sample, unit, tiny[0]]:
        (directory / 'fencedin.in').write_text(encoded(case))
        for existing in [False, True]:
            output = directory / 'fencedin.out'
            if existing:
                output.write_bytes(previous)
            else:
                output.unlink(missing_ok=True)
            process = execute(directory, False)
            assert process.returncode == 2 and not process.stdout and 'Complete the four' in process.stderr
            assert output.read_bytes() == previous if existing else not output.exists()
            counts['unfinishedLearnerRuns'] += 1
    for data in bad:
        output.write_bytes(previous)
        input_file = directory / 'fencedin.in'
        if data is None:
            input_file.unlink(missing_ok=True)
        else:
            input_file.write_text(data)
        process = execute(directory, False)
        assert process.returncode == 2 and not process.stdout and 'Complete the four' not in process.stderr
        assert output.read_bytes() == previous
        counts['refusedLearnerInputs'] += 1
    # Temporary parser/serializer probes never complete a learner algorithm.
    probe = '''import java.util.Arrays;
class Probe {
    public static void main(String[] args) throws Exception {
        Main.Input input = Main.readInput();
        if (args[0].equals("parse")) {
            System.out.println(input.width + " " + input.height + " " + Arrays.toString(input.vertical) + " " + Arrays.toString(input.horizontal));
        } else {
            System.out.print(Main.output(input, Long.parseLong(args[0])));
        }
    }
}
'''
    (directory / 'Probe.java').write_text(probe)
    compile_role(directory, True)
    for case in [sample, unit, varied, single_column, single_row, tiny[0]]:
        (directory / 'fencedin.in').write_text(encoded(case))
        process = run([args.java, '-ea', '-Xmx256m', 'Probe', 'parse'], directory)
        a, b, xs, ys = case
        assert process.stdout.strip() == f'{a} {b} {xs} {ys}' and not process.stderr
        counts['parserProbes'] += 1
    for case in [tiny[0], unit]:
        (directory / 'fencedin.in').write_text(encoded(case))
        a, b, xs, ys = case
        upper = ((len(xs) + 1) * (len(ys) + 1) - 1) * max(a, b)
        for value in [-1, upper + 1]:
            process = run([args.java, '-ea', '-Xmx256m', 'Probe', str(value)], directory, False)
            assert process.returncode != 0 and not process.stdout and 'Result outside documented feasible bounds' in process.stderr
            counts['invalidResultProbes'] += 1
for path, before in tracked.items():
    assert path.read_bytes() == before
assert counts == dict(zipRoles=2, compiledRoles=2, independentTinyCases=54,
    officialSampleCases=1, constructedFullLimitCases=5, unfinishedLearnerRuns=6,
    refusedLearnerInputs=21, parserProbes=6, invalidResultProbes=4), counts
print(json.dumps(dict(event='gold-fenced-in-pack-accepted', heapMiB=256,
    maximumFencesPerOrientation=2000, originalOutOfMemoryReproduced=True,
    independentSpanningSubsetEnumeration=True, axisSwapCases=True,
    disjointSetUnchanged=True, sourceAndSampleFilesUnchanged=True,
    learnerAlgorithmUnfinished=True, previousAnswerPreserved=True,
    temporaryCopiesRemoved=True, **counts)), flush=True)
