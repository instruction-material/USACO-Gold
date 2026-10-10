"""Native references, independent tiny models, full limits and unfinished drivers."""
import argparse
from collections import deque
from functools import lru_cache
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
TASK = 'gold-fenwick-practice-native-acceptance'
SPECS = [
    dict(folder='UG23-Balanced-Photo', stem='bphoto', title='Balanced Photo', sha='0d32ca793c716e085b62d3b243ffbb0126f6257aa13d47f68384ba14cffee4ee'),
    dict(folder='UG25-Sleepy-Cow-Sorting', stem='sleepy', title='Sleepy Cow Sorting', sha='fe3b05326beffd47e07a8da55fdf7e56440cad1b70904a227b590c7e3fa97d93'),
    dict(folder='UG26-Out-of-Sorts', stem='sort', title='Out of Sorts, Gold bidirectional sweeps', sha='301583420c366b781ff7269f804b71cc2944710f5134b569eaf60c03a18b2aff'),
]


def run(command, cwd, timeout=30):
    child = subprocess.Popen(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    print(json.dumps(dict(event='start', parentTaskId=TASK, cwd=str(cwd), command=command, pid=child.pid, startTime=time.time(), timeoutSeconds=timeout)), flush=True)
    try:
        out, err = child.communicate(timeout=timeout)
    except BaseException:
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        child.communicate()
        print(json.dumps(dict(event='cleanup', parentTaskId=TASK, pid=child.pid, endTime=time.time(), exitCode=child.returncode, childProcessGroupCleanup='terminated')), flush=True)
        raise
    print(json.dumps(dict(event='end', parentTaskId=TASK, pid=child.pid, endTime=time.time(), exitCode=child.returncode, childProcessGroupCleanup='exited')), flush=True)
    return subprocess.CompletedProcess(command, child.returncode, out, err)


def text_for(stem, values):
    separator = ' ' if stem == 'sleepy' else '\n'
    return str(len(values)) + '\n' + separator.join(map(str, values)) + '\n'


def unbalanced(values):
    answer = 0
    for i, height in enumerate(values):
        left = sum(v > height for v in values[:i])
        right = sum(v > height for v in values[i + 1:])
        answer += max(left, right) > 2 * min(left, right)
    return answer


def gold_sweeps(values):
    values = list(values)
    iterations = 0
    while True:
        iterations += 1
        for i in range(len(values) - 1):
            if values[i + 1] < values[i]:
                values[i], values[i + 1] = values[i + 1], values[i]
        for i in range(len(values) - 2, -1, -1):
            if values[i + 1] < values[i]:
                values[i], values[i + 1] = values[i + 1], values[i]
        if all(a <= b for a, b in zip(values, values[1:])):
            return iterations
        assert iterations <= len(values)


@lru_cache(maxsize=None)
def minimum_moves(n):
    """Reverse BFS from sorted order, independent of the suffix/Fenwick solver."""
    goal = tuple(range(1, n + 1))
    distances = {goal: 0}
    queue = deque([goal])
    while queue:
        state = queue.popleft()
        for k in range(1, n):
            predecessor = (state[k],) + state[:k] + state[k + 1:]
            if predecessor not in distances:
                distances[predecessor] = distances[state] + 1
                queue.append(predecessor)
    assert len(distances) == __import__('math').factorial(n)
    return distances


def check_answer(stem, values, output, expected):
    tokens = output.split()
    numbers = [int(token) for token in tokens]
    if stem != 'sleepy':
        assert len(numbers) == 1 and numbers[0] == expected, (stem, numbers, expected)
        return
    assert numbers and 0 <= numbers[0] < len(values)
    k, steps = numbers[0], numbers[1:]
    assert len(steps) == k and all(1 <= step < len(values) for step in steps)
    if expected is not None:
        assert steps == expected and k == len(expected)
    else:
        assert k == minimum_moves(len(values))[tuple(values)], (values, numbers)
        state = list(values)
        for step in steps:
            front = state.pop(0)
            state.insert(step, front)
        assert state == sorted(values), (values, numbers, state)


def fixtures(stem):
    rng = random.Random(20261010)
    if stem == 'bphoto':
        tiny = [[34, 6, 23, 0, 5, 99, 2], [0], [1, 2, 3], [3, 2, 1], [1, 3, 2], [0, 1000000000]]
        tiny += [rng.sample(range(100), rng.randint(2, 24)) for _ in range(22)]
        original = tiny[0]
        tiny += [list(reversed(original)), [2 * v + 1 for v in original]]
        assert unbalanced(original) == unbalanced(tiny[-1]) == unbalanced(tiny[-2]) == 3
        small = [(v, unbalanced(v)) for v in tiny]
        large = [(list(range(100000)), 99999), (list(range(99999, -1, -1)), 99999)]
    elif stem == 'sleepy':
        tiny = [[1, 2, 4, 3], [1], [1, 2, 3], [6, 5, 4, 3, 2, 1], [2, 3, 1, 4]]
        tiny += [list(v) for v in itertools.permutations(range(1, 5))]
        for _ in range(18):
            v = list(range(1, rng.randint(2, 6) + 1))
            rng.shuffle(v)
            tiny.append(v)
        small = [(v, None) for v in tiny]
        large = [(list(range(1, 100001)), []), (list(range(100000, 0, -1)), list(range(99999, 0, -1)))]
    else:
        tiny = [[1, 8, 5, 3, 2], [0], [1, 2, 3], [3, 2, 1], [2, 1, 1], [4, 4, 4], [0, 1000000000, 0, 1000000000]]
        tiny += [[rng.choice([0, 1, 2, 4, 1000000000]) for _ in range(rng.randint(2, 26))] for _ in range(24)]
        small = [(v, gold_sweeps(v)) for v in tiny]
        assert small[0][1] == 2 and small[4][1] == 1
        large = [(list(range(100000)), 1), (list(range(99999, -1, -1)), 50000), ([7] * 100000, 1)]
    sample = text_for(stem, small[0][0])
    invalid = ['', '0\n', '100001\n', 'N\n', '2 extra\n', '1\n', '1\n1.5\n', '1\n99999999999999999\n', sample + 'late-invalid\n']
    if stem == 'sleepy':
        invalid += ['2\n1\n', '2\n1 2 3\n', '2\n1\n2\n', '2\n1 1\n', '2\n0 2\n', '2\n1 3\n', '2\n-1 2\n']
    else:
        invalid += ['2\n1\n', '1\n1 2\n', '1\n-1\n', '1\n1000000001\n']
        if stem == 'bphoto':
            invalid += ['2\n1\n1\n']
    return small, large, invalid


PROBES = {
    'bphoto': '''    static int bruteForTesting(Input input) {
        int answer = 0;
        for (int i = 0; i < input.n; i++) {
            int left = 0, right = 0;
            for (int j = 0; j < i; j++) if (input.values[j] > input.values[i]) left++;
            for (int j = i + 1; j < input.n; j++) if (input.values[j] > input.values[i]) right++;
            if (Math.max(left, right) > 2 * Math.min(left, right)) answer++;
        }
        return answer;
    }

''',
    'sort': '''    static int bruteForTesting(Input input) {
        int[] values = input.values.clone();
        int iterations = 0;
        while (true) {
            iterations++;
            for (int i = 0; i + 1 < values.length; i++) {
                if (values[i + 1] < values[i]) { int t = values[i]; values[i] = values[i + 1]; values[i + 1] = t; }
            }
            for (int i = values.length - 2; i >= 0; i--) {
                if (values[i + 1] < values[i]) { int t = values[i]; values[i] = values[i + 1]; values[i + 1] = t; }
            }
            boolean sorted = true;
            for (int i = 0; i + 1 < values.length; i++) if (values[i + 1] < values[i]) sorted = false;
            if (sorted) return iterations;
        }
    }

''',
    'sleepy': '''    static Plan bruteForTesting(Input input) {
        int[] goal = new int[input.n];
        for (int i = 0; i < goal.length; i++) goal[i] = i;
        String target = java.util.Arrays.toString(goal);
        String start = java.util.Arrays.toString(input.values);
        java.util.ArrayDeque<int[]> queue = new java.util.ArrayDeque<>();
        java.util.HashMap<String, String> previous = new java.util.HashMap<>();
        java.util.HashMap<String, Integer> move = new java.util.HashMap<>();
        previous.put(start, null);
        queue.add(input.values.clone());
        while (!queue.isEmpty() && !previous.containsKey(target)) {
            int[] state = queue.removeFirst();
            String key = java.util.Arrays.toString(state);
            for (int k = 1; k < input.n; k++) {
                int[] next = state.clone();
                System.arraycopy(state, 1, next, 0, k);
                next[k] = state[0];
                String label = java.util.Arrays.toString(next);
                if (!previous.containsKey(label)) { previous.put(label, key); move.put(label, k); queue.addLast(next); }
            }
        }
        if (!previous.containsKey(target)) throw new IllegalArgumentException("No sorting plan");
        java.util.ArrayList<Integer> backwards = new java.util.ArrayList<>();
        for (String key = target; !key.equals(start); key = previous.get(key)) backwards.add(move.get(key));
        int[] steps = new int[backwards.size()];
        for (int i = 0; i < steps.length; i++) steps[i] = backwards.get(steps.length - i - 1);
        return new Plan(steps);
    }

'''
}


def verify(spec, javac, java):
    pack = ROOT / spec['folder']
    before = {str(p.relative_to(pack)): p.read_bytes() for p in pack.rglob('*') if p.is_file() and p.name != '.DS_Store'}
    original = before['solution/Main.java'].replace(b'\r\n', b'\n')
    assert hashlib.sha256(original).hexdigest() == spec['sha']
    tracked = subprocess.check_output(['git', 'show', 'HEAD:' + spec['folder'] + '/solution/Main.java'], cwd=ROOT)
    assert tracked == original
    for role in ['starter', 'solution']:
        expected = {'Main.java', 'README.md', 'sample.in'}
        if spec['stem'] == 'bphoto' and role == 'solution':
            expected |= {'bphoto.in', 'bphoto.out'}
        assert {p.name for p in (pack / role).iterdir() if p.name != '.DS_Store'} == expected
        guide = (pack / role / 'README.md').read_text()
        for heading in ['Prerequisites and input', 'Trace and explain', 'Native workflow', 'Verify and explain']:
            assert '## ' + heading in guide
    learner = (pack / 'starter/Main.java').read_text()
    assert learner != (pack / 'solution/Main.java').read_text()
    assert all('TASK ' + str(i) + ':' in learner for i in range(1, 6))
    assert before['starter/sample.in'] == before['solution/sample.in']
    if spec['stem'] == 'bphoto':
        assert before['solution/bphoto.in'].replace(b'\r\n', b'\n').rstrip(b'\n') == before['starter/sample.in'].replace(b'\r\n', b'\n').rstrip(b'\n')
        assert before['solution/bphoto.out'].replace(b'\r\n', b'\n') == b'3\n'
    small, large, invalid = fixtures(spec['stem'])
    sample = text_for(spec['stem'], small[0][0])
    assert (pack / 'starter/sample.in').read_text() == sample
    unfinished = 'Complete the five ' + spec['title'] + ' tasks before producing an answer'
    marker = 'throw new UnsupportedOperationException(' + json.dumps(unfinished) + ');'
    assert learner.count(marker) == 1
    probe = learner.replace(marker, 'return bruteForTesting(input);')
    probe = probe.replace('    public static void main(String[] args)', PROBES[spec['stem']] + '    public static void main(String[] args)')
    with tempfile.TemporaryDirectory(prefix=spec['stem'] + '-acceptance-') as temporary:
        work = Path(temporary)
        classes = {}
        for role, source in [('starter', learner), ('solution', (pack / 'solution/Main.java').read_text()), ('driver-probe', probe)]:
            directory = work / role
            directory.mkdir()
            (directory / 'Main.java').write_text(source)
            result = run([javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-Werror', 'Main.java'], directory)
            assert result.returncode == 0, result.stderr
            classes[role] = directory
        execution = work / 'execution'
        execution.mkdir()
        input_path, output_path = execution / (spec['stem'] + '.in'), execution / (spec['stem'] + '.out')
        retained = execution / 'retained-attempt.txt'
        retained.write_bytes(b'separate saved learner work\n')
        def execute(role):
            return run([java, '-ea', '-Xmx256m', '-cp', str(classes[role]), 'Main'], execution)
        valid = small + large
        for values, expected in valid:
            text = text_for(spec['stem'], values)
            input_path.write_text(text)
            output_path.write_text('old answer\n')
            result = execute('solution')
            assert result.returncode == 0 and result.stdout == result.stderr == '', result
            check_answer(spec['stem'], values, output_path.read_text(), expected)
            assert input_path.read_text() == text
        crlf = sample.replace('\n', '\r\n')
        input_path.write_bytes(crlf.encode())
        output_path.write_text('old answer\n')
        result = execute('solution')
        assert result.returncode == 0 and result.stdout == result.stderr == '', result
        check_answer(spec['stem'], small[0][0], output_path.read_text(), small[0][1])
        assert input_path.read_bytes() == crlf.encode()
        for values, expected in small:
            text = text_for(spec['stem'], values)
            input_path.write_text(text)
            output_path.write_text('old answer\n')
            result = execute('driver-probe')
            assert result.returncode == 0 and result.stdout == result.stderr == '', result
            check_answer(spec['stem'], values, output_path.read_text(), expected)
            assert input_path.read_text() == text
        whitespace = ' \t' + sample.replace('\n', ' \t\r\n') + '\r\n \t\r\n'
        input_path.write_bytes(whitespace.encode())
        output_path.write_text('old answer\n')
        result = execute('driver-probe')
        assert result.returncode == 0 and result.stdout == result.stderr == '', result
        check_answer(spec['stem'], small[0][0], output_path.read_text(), small[0][1])
        assert input_path.read_bytes() == whitespace.encode()
        for values in [small[0][0], small[1][0], large[0][0]]:
            text = text_for(spec['stem'], values)
            input_path.write_text(text)
            for existing in [False, True]:
                if output_path.exists():
                    output_path.unlink()
                if existing:
                    output_path.write_text('retained old answer\n')
                result = execute('starter')
                assert result.returncode == 2 and result.stdout == ''
                assert result.stderr == f'Cannot solve {spec["stem"]}.in: {unfinished}\n'
                assert output_path.exists() == existing
                if existing:
                    assert output_path.read_text() == 'retained old answer\n'
                assert input_path.read_text() == text
        for text in invalid:
            input_path.write_text(text)
            output_path.write_text('retained old answer\n')
            for role in ['starter', 'driver-probe']:
                result = execute(role)
                assert result.returncode == 2 and result.stdout == '' and result.stderr.startswith('Cannot solve ' + spec['stem'] + '.in:')
                assert output_path.read_text() == 'retained old answer\n' and input_path.read_text() == text
        input_path.unlink()
        for role in ['starter', 'driver-probe']:
            result = execute(role)
            assert result.returncode == 2 and result.stdout == ''
            assert result.stderr.startswith('Cannot solve ' + spec['stem'] + '.in:')
            assert output_path.read_text() == 'retained old answer\n'
        assert retained.read_bytes() == b'separate saved learner work\n'
    assert {str(p.relative_to(pack)): p.read_bytes() for p in pack.rglob('*') if p.is_file() and p.name != '.DS_Store'} == before
    print(json.dumps(dict(event='gold-fenwick-practice-pack-accepted', parentTaskId=TASK, folder=spec['folder'], validReferenceCases=len(valid) + 1, tinyIndependentDriverCases=len(small) + 1, maximumN=100000, malformedInputs=len(invalid), unfinishedLearnerCases=6, missingInputCases=2, referenceJavaPreserved=True, referenceGitSha256=spec['sha'], sourceFilesUnchanged=True, inputAndUnrelatedWorkPreserved=True, referenceInvalidInputClaims=False, completedProbeGoldPerformanceClaim=False, sleepyAnyOptimalPlanAccepted=spec['stem'] == 'sleepy', goldBidirectionalSweepAndDuplicates=spec['stem'] == 'sort', sourceHashes={name: hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest() for name, data in before.items()})), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--javac', default='javac')
    parser.add_argument('--java', default='java')
    args = parser.parse_args()
    for spec in SPECS:
        verify(spec, args.javac, args.java)
