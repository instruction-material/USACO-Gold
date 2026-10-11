"""Native bounded-time reference checks and restricted learner file-driver probes."""
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

TASK = 'gold-time-mooney-native-acceptance'
LEGACY_SHA = 'f44155e3b84ca0b3503ca4ca44b1c91f98ffeb7baf12d7a337572a29343350d1'

DRIVER_PROBE = r'''
// Acceptance-only walk enumeration, restricted to four cities and eight days.
class TimeDriverProbe {
    static boolean negative;
    static int solve(Main.Problem problem) {
        int reward = 0;
        for (int value : problem.money) reward = Math.max(reward, value);
        if (problem.money.length > 4 || reward / problem.cost > 8) {
            throw new IllegalArgumentException("Tiny probe supports at most four cities and eight days");
        }
        if (negative) return -1;
        int[] answer = {0};
        walk(problem, 0, 0, 0, reward / problem.cost, answer);
        return answer[0];
    }
    static void walk(Main.Problem p, int city, int day, int gross, int limit, int[] answer) {
        if (city == 0) answer[0] = Math.max(answer[0], gross - p.cost * day * day);
        if (day == limit) return;
        for (int[] edge : p.edges) {
            if (edge[0] == city) walk(p, edge[1], day + 1, gross + p.money[edge[1]], limit, answer);
        }
    }
    public static void main(String[] args) {
        negative = true;
        Main.main(new String[0]);
    }
}
'''


def run(command, cwd, expected=0, timeout=30):
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    print(json.dumps(dict(event='start', parentTaskId=TASK, cwd=str(cwd), command=command, pid=child.pid, startTime=time.time(), timeoutSeconds=timeout)), flush=True)
    try:
        out, err = child.communicate(timeout=timeout)
    except BaseException:
        try:
            os.killpg(child.pid, signal.SIGTERM)
            child.communicate(timeout=3)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGKILL)
                child.communicate()
        print(json.dumps(dict(event='cleanup', parentTaskId=TASK, pid=child.pid, exitCode=child.returncode, endTime=time.time(), childProcessGroupCleanup='terminated')), flush=True)
        raise
    print(json.dumps(dict(event='end', parentTaskId=TASK, pid=child.pid, exitCode=child.returncode, endTime=time.time(), childProcessGroupCleanup='exited')), flush=True)
    assert child.returncode == expected, (command, child.returncode, out, err)
    return out, err


def encode(money, edges, cost):
    return f'{len(money)} {len(edges)} {cost}\n' + ' '.join(map(str, money)) + '\n' + ''.join(f'{a+1} {b+1}\n' for a, b in edges)


def oracle(money, edges, cost):
    current = [-1] * len(money)
    current[0] = 0
    answer = 0
    # One extra day independently checks the cutoff: its gross-profit bound is nonpositive.
    for day in range(1, max(money)//cost + 2):
        following = [-1] * len(money)
        for a, b in edges:
            if current[a] >= 0:
                following[b] = max(following[b], current[a] + money[b])
        current = following
        if current[0] >= 0:
            answer = max(answer, current[0] - cost*day*day)
    return answer


def verify(pack, javac, java):
    paths = sorted(p for p in pack.rglob('*') if p.is_file())
    before = {str(p.relative_to(pack)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert before['legacy/Main.java'] == LEGACY_SHA
    assert before['starter/Main.java'] != before['solution/Main.java']
    sample = (pack/'starter/time.in').read_text()
    assert sample == (pack/'solution/time.in').read_text()
    assert (pack/'solution/time.out').read_text() == '24\n'
    small = '2 1 1\n0 10\n1 2\n'
    zero = '2 1 1\n0 0\n1 2\n'
    valid = [('sample', sample, 24), ('no-return', small, 0), ('high-cost', '2 2 1000\n0 1000\n1 2\n2 1\n', 0)]
    rng = random.Random(993)
    for index in range(45):
        n = rng.randint(2, 16)
        money = [0] + [rng.randint(0, 1000) for _ in range(n-1)]
        edges = [(a, b) for a in range(n) for b in range(n) if a != b and rng.random() < 0.2]
        if not edges:
            edges = [(0, 1)]
        cost = rng.choice([1, 2, 3, 10, 100, 1000])
        valid.append((f'independent-day-layer-{index}', encode(money, edges, cost), oracle(money, edges, cost)))
    n = 1000
    money = [0] + [1000] * (n-1)
    edges = [(i, (i+j)%n) for i in range(n) for j in [1, 2]]
    full = encode(money, edges, 1)
    valid.append(('maximum-cities-roads-rewards', full, oracle(money, edges, 1)))
    tiny = []
    for values, roads, cost in [([0, 7], [(0, 1), (1, 0)], 1), ([0, 8], [(0, 1)], 1), ([0, 0], [(0, 1)], 1), ([0, 5, 8], [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)], 1)]:
        tiny.append((encode(values, roads, cost), oracle(values, roads, cost)))
    invalid = ['1 1 1\n', '1001 1 1\n', '2 0 1\n', '2 2001 1\n', '2 1 0\n', '2 1 1001\n', '2 1\n', 'two 1 1\n',
               '2 1 1\n1 10\n1 2\n', '2 1 1\n0 -1\n1 2\n', '2 1 1\n0 1001\n1 2\n', '2 1 1\n0 10\n1 1\n',
               '2 1 1\n0 10\n1 3\n', '2 1 1\n0\n', '2 1 1\n0 10\n', small + '1\n']
    sentinel = b'earlier answer\n'
    with tempfile.TemporaryDirectory(prefix='time-mooney-acceptance-') as temp:
        roles = {}
        for role in ['starter', 'solution', 'probe']:
            cwd = Path(temp)/role
            cwd.mkdir()
            source = (pack/('starter' if role == 'probe' else role)/'Main.java').read_bytes()
            files = ['Main.java']
            if role == 'probe':
                marker = b'throw new UnsupportedOperationException("Complete the four Time is Mooney graph-DP tasks");'
                assert source.count(marker) == 1
                source = source.replace(marker, b'return TimeDriverProbe.solve(problem);')
                (cwd/'TimeDriverProbe.java').write_text(DRIVER_PROBE)
                files.append('TimeDriverProbe.java')
            (cwd/'Main.java').write_bytes(source)
            run([javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-Werror', *files], cwd, timeout=45)
            roles[role] = cwd
        cwd = roles['solution']
        for name, data, answer in valid:
            (cwd/'time.in').write_text(data)
            (cwd/'time.out').write_bytes(sentinel)
            assert run([java, '-ea', '-Xmx256m', 'Main'], cwd) == (b'', b'')
            assert (cwd/'time.out').read_text() == f'{answer}\n', name
            assert (cwd/'time.in').read_text() == data
        cwd = roles['starter']
        for data in [sample, small, zero, full]:
            (cwd/'time.in').write_text(data)
            for previous in [False, True]:
                answer = cwd/'time.out'
                if previous:
                    answer.write_bytes(sentinel)
                else:
                    answer.unlink(missing_ok=True)
                out, err = run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
                assert not out and b'Complete the four Time is Mooney' in err
                assert answer.read_bytes() == sentinel if previous else not answer.exists()
        for data in invalid:
            (cwd/'time.in').write_text(data)
            (cwd/'time.out').write_bytes(sentinel)
            out, err = run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
            assert not out and b'Cannot solve' in err and (cwd/'time.out').read_bytes() == sentinel
        (cwd/'time.in').unlink()
        run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
        assert (cwd/'time.out').read_bytes() == sentinel
        (cwd/'time.in').write_text(small)
        run([java, '-ea', '-Xmx256m', 'Main', '--trace'], cwd, expected=2)
        assert (cwd/'time.out').read_bytes() == sentinel
        cwd = roles['probe']
        for data, answer in tiny:
            (cwd/'time.in').write_text(data)
            (cwd/'time.out').write_bytes(sentinel)
            assert run([java, '-ea', '-Xmx256m', 'Main'], cwd) == (b'', b'')
            assert (cwd/'time.out').read_text() == f'{answer}\n'
        (cwd/'time.in').write_text(tiny[0][0])
        (cwd/'time.out').write_bytes(sentinel)
        out, err = run([java, '-ea', '-Xmx256m', 'TimeDriverProbe'], cwd, expected=2)
        assert not out and b'no-trip option' in err and (cwd/'time.out').read_bytes() == sentinel
        for data in [encode([0]*5, [(0, 1)], 1), small]:
            (cwd/'time.in').write_text(data)
            out, err = run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
            assert not out and b'Tiny probe supports' in err and (cwd/'time.out').read_bytes() == sentinel
    assert before == {str(p.relative_to(pack)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    print(json.dumps(dict(event='gold-time-mooney-pack-accepted', parentTaskId=TASK, referenceFileCases=len(valid), independentDayLayerCases=45, maximumCities=1000, maximumRoads=2000, maximumReward=1000, maximumHorizon=1000, unfinishedLearnerCases=8, invalidInputCases=len(invalid), missingInputCases=1, unexpectedArgumentCases=1, tinyIndependentDriverCases=len(tiny), driverResultGuardCases=1, tinyProbeMaximumN=4, tinyProbeMaximumDays=8, originalBytesPreserved=True, roleSourceDistinct=True, sourceFilesUnchanged=True, previousAnswerPreserved=True, learnerAlgorithmUnfinished=True, historicalReferenceInvalidInputClaims=False, roleSourceSha256={role: before[f'{role}/Main.java'] for role in ['starter', 'solution']})), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pack', type=Path, default=Path(__file__).resolve().parents[1]/'UG-Time-is-Mooney')
    parser.add_argument('--javac', default='javac')
    parser.add_argument('--java', default='java')
    args = parser.parse_args()
    verify(args.pack.resolve(), args.javac, args.java)
