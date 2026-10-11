"""Independent route enumeration, native helper and unfinished-driver acceptance."""
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

TASK = 'gold-shortcut-native-acceptance'
ORIGINAL_SHA = '8fcb4327928f01fdfdf72873089052470d6bd01d4aa2a54c00f318457eb146e8'
REFERENCE_SHA = '7f8fd61bf4f0c3e2f06669c8260f595e1d1ec7925ca8ec1b30d12a0cc753cf96'
SAMPLE_SHA = '6ea334f44215abf115bd17960f11c9502cd440bfb74011dcd2ee08ecd5e7f1c0'
PROBE = r'''
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class ShortcutDriverProbe {
    static String mode = "normal";
    static final class Route {
        final long time;
        final List<Integer> fields;
        final List<Integer> weights;
        Route(long time, List<Integer> fields, List<Integer> weights) {
            this.time = time;
            this.fields = new ArrayList<>(fields);
            this.weights = new ArrayList<>(weights);
        }
    }
    static Route best;
    static int lex(List<Integer> a, List<Integer> b) {
        for (int i = 0; i < Math.min(a.size(), b.size()); i++) {
            int comparison = Integer.compare(a.get(i), b.get(i));
            if (comparison != 0) return comparison;
        }
        return Integer.compare(a.size(), b.size());
    }
    static void enumerate(Main.Problem problem, int field, long time,
            List<Integer> fields, List<Integer> weights) {
        if (field == 0) {
            if (best == null || time < best.time
                    || (time == best.time && lex(fields, best.fields) < 0)) {
                best = new Route(time, fields, weights);
            }
            return;
        }
        for (Main.Edge edge : problem.roads.get(field)) {
            if (fields.contains(edge.to)) continue;
            fields.add(edge.to);
            weights.add(edge.weight);
            enumerate(problem, edge.to, time + edge.weight, fields, weights);
            weights.remove(weights.size() - 1);
            fields.remove(fields.size() - 1);
        }
    }
    // Acceptance-only route enumeration, restricted to eight fields.
    static long solve(Main.Problem problem) {
        if (problem.cows.length > 8) throw new IllegalArgumentException("Tiny driver probe only");
        if (mode.equals("negative")) return -1;
        if (mode.equals("too-large")) return Long.MAX_VALUE;
        List<Route> selected = new ArrayList<>();
        for (int start = 0; start < problem.cows.length; start++) {
            best = null;
            List<Integer> fields = new ArrayList<>();
            fields.add(start);
            enumerate(problem, start, 0, fields, new ArrayList<>());
            assert best != null;
            selected.add(best);
        }
        long answer = 0;
        for (int candidate = 0; candidate < problem.cows.length; candidate++) {
            long saving = 0;
            for (int origin = 0; origin < selected.size(); origin++) {
                Route route = selected.get(origin);
                int position = route.fields.indexOf(candidate);
                if (position == -1) continue;
                long remaining = 0;
                for (int edge = position; edge < route.weights.size(); edge++) {
                    remaining += route.weights.get(edge);
                }
                saving += problem.cows[origin] * Math.max(0L, remaining - problem.shortcutTime);
            }
            answer = Math.max(answer, saving);
        }
        return answer;
    }
    public static void main(String[] args) {
        mode = args[0];
        Main.main(new String[0]);
    }
}

class ShortcutHelperProbe {
    static String snapshot(Main.Problem problem) {
        StringBuilder result = new StringBuilder(Arrays.toString(problem.cows));
        result.append('|').append(problem.shortcutTime);
        for (int a = 0; a < problem.roads.size(); a++) {
            for (Main.Edge edge : problem.roads.get(a)) {
                result.append('|').append(a).append(':').append(edge.to).append(':').append(edge.weight);
            }
        }
        return result.toString();
    }
    public static void main(String[] args) throws Exception {
        Main.Problem problem = Main.readProblem(Path.of("shortcut.in"));
        String before = snapshot(problem);
        Main.ShortestRoutes actual = Main.shortestRoutes(problem.roads);
        List<String> expected = Files.readAllLines(Path.of("expected-routes.txt"));
        assert expected.size() == problem.cows.length;
        assert actual.distance[0] == 0 && actual.parent[0] == -1;
        for (int field = 0; field < expected.size(); field++) {
            String[] row = expected.get(field).split(" ");
            assert actual.distance[field] == Long.parseLong(row[0]) : field;
            assert actual.parent[field] == Integer.parseInt(row[1]) : field;
            if (field != 0) {
                assert actual.distance[actual.parent[field]] < actual.distance[field];
            }
        }
        assert snapshot(problem).equals(before);
    }
}
'''


def run(command, cwd, expected=0, timeout=30):
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    print(json.dumps(dict(event='start', parentTaskId=TASK, cwd=str(cwd), command=command, pid=child.pid,
                          startTime=time.time(), timeoutSeconds=timeout)), flush=True)
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
        print(json.dumps(dict(event='cleanup', parentTaskId=TASK, pid=child.pid, exitCode=child.returncode,
                              endTime=time.time(), childProcessGroupCleanup='terminated')), flush=True)
        raise
    print(json.dumps(dict(event='end', parentTaskId=TASK, pid=child.pid, exitCode=child.returncode,
                          endTime=time.time(), childProcessGroupCleanup='exited')), flush=True)
    assert child.returncode == expected, (command, child.returncode, out, err)
    return out, err


def encode(n, roads, cows, shortcut):
    return (f'{n} {len(roads)} {shortcut}\n' + ' '.join(map(str, cows)) + '\n'
            + ''.join(f'{a+1} {b+1} {weight}\n' for a, b, weight in roads))


def oracle(n, roads, cows, shortcut):
    # Enumerate simple paths directly, independently of a queue or parent tree.
    adjacency = [[] for _ in range(n)]
    for a, b, weight in roads:
        adjacency[a].append((b, weight))
        adjacency[b].append((a, weight))
    selected = []
    for start in range(n):
        best = None

        def walk(field, route, weights, distance):
            nonlocal best
            if field == 0:
                candidate = (distance, tuple(route), tuple(weights))
                if best is None or candidate[:2] < best[:2]:
                    best = candidate
                return
            for next_, weight in adjacency[field]:
                if next_ not in route:
                    walk(next_, route + [next_], weights + [weight], distance + weight)

        walk(start, [start], [], 0)
        assert best is not None
        selected.append(best)
    savings = []
    for field in range(n):
        saving = 0
        for origin, (_, route, weights) in enumerate(selected):
            if field in route:
                position = route.index(field)
                saving += cows[origin] * max(0, sum(weights[position:]) - shortcut)
        savings.append(saving)
    state = [(distance, route[1] if len(route) > 1 else -1) for distance, route, _ in selected]
    return max(savings), state


def verify(pack, javac, java):
    before = {str(f.relative_to(pack)): hashlib.sha256(f.read_bytes()).hexdigest()
              for f in pack.rglob('*') if f.is_file()}
    reference = (pack / 'solution/Main.java').read_bytes()
    original = (pack / 'legacy/Main.java').read_bytes()
    learner = (pack / 'starter/Main.java').read_bytes()
    sample = (pack / 'starter/shortcut.in').read_bytes().replace(b'\r\n', b'\n')
    assert hashlib.sha256(original).hexdigest() == ORIGINAL_SHA
    assert hashlib.sha256(reference.replace(b'\r\n', b'\n')).hexdigest() == REFERENCE_SHA
    changes = [(b'static ArrayList<Point>[] adj;', b'static ArrayList<ArrayList<Point>> adj;'),
               (b'adj = new ArrayList[N];', b'adj = new ArrayList<>(N);'),
               (b'adj[i] = new ArrayList<Point>();', b'adj.add(new ArrayList<Point>());'),
               (b'adj[p].add(new Point(w, q));', b'adj.get(p).add(new Point(w, q));'),
               (b'adj[q].add(new Point(w, p));', b'adj.get(q).add(new Point(w, p));'),
               (b'for (Point p : adj[currNode])', b'for (Point p : adj.get(currNode))')]
    repaired = original
    for old, new in changes:
        assert repaired.count(old) == 1
        repaired = repaired.replace(old, new)
    assert repaired.replace(b'\r\n', b'\n') == reference.replace(b'\r\n', b'\n')
    assert learner != reference and learner.count(b'// TODO ') == 4
    assert hashlib.sha256(sample).hexdigest() == SAMPLE_SHA
    assert (pack / 'solution/shortcut.in').read_bytes().replace(b'\r\n', b'\n') == sample
    assert (pack / 'solution/shortcut.out').read_text() == '40\n'
    for role in ['starter', 'solution']:
        guide = ' '.join((pack / role / 'README.md').read_text().split())
        for contract in ['1..10000', 'N-1..50000', '0..10000', '1..25000', 'shortcut.in',
                         'shortcut.out', 'long', '40', 'PowerShell', 'usual route']:
            assert contract in guide, (role, contract)

    cases = []

    def tiny(name, n, roads, cows, shortcut):
        answer, state = oracle(n, roads, cows, shortcut)
        cases.append((name, encode(n, roads, cows, shortcut), answer, state))

    tiny('official-sample', 5, [(0,1,5),(0,2,3),(1,3,3),(2,3,5),(3,4,2),(2,4,7)], [1,2,3,4,5], 2)
    assert cases[0][1].encode() == sample and cases[0][2] == 40
    assert cases[0][3] == [(0,-1),(5,0),(3,0),(8,1),(10,2)]
    tiny('only-barn', 1, [], [10000], 10000)
    tiny('zero-cows', 4, [(0,1,2),(1,2,3),(2,3,4)], [0]*4, 1)
    tiny('no-benefit', 4, [(0,1,2),(1,2,3),(2,3,4)], [10000]*4, 10000)
    tiny('toward-barn-tie', 5, [(0,1,4),(0,2,3),(1,3,2),(2,3,3),(3,4,2)], [1,11,17,23,31], 2)
    tiny('parallel-and-loop', 3, [(0,1,5),(0,1,2),(1,2,3),(2,2,1)], [0,7,11], 1)
    tiny('usual-route-only', 5, [(0,1,8),(0,2,7),(1,3,2),(2,4,2),(3,4,20)], [0,1,1,30,40], 1)
    rng = random.Random(899)
    for index in range(24):
        n = rng.randint(2, 7)
        roads = [(v, rng.randrange(v), rng.randint(1,10)) for v in range(1,n)]
        pairs = {tuple(sorted((a,b))) for a,b,_ in roads}
        for a in range(n):
            for b in range(a+1,n):
                if (a,b) not in pairs and rng.random() < .45:
                    roads.append((a,b,rng.randint(1,10)))
        rng.shuffle(roads)
        tiny(f'independent-routes-{index}', n, roads,
             [rng.randint(0,10000) for _ in range(n)], rng.randint(1,8))
    independent = len(cases)
    n = 10000
    cows = [10000]*n
    roads = [(v-1,v,25000) for v in range(1,n)]
    answer = max((n-v)*10000*max(0,v*25000-1) for v in range(n))
    assert answer > 2**31
    cases.append(('maximum-chain-and-long-answer', encode(n,roads,cows,1), answer,
                  [(v*25000,v-1) for v in range(n)]))
    roads = [(0,v,25000) for v in range(1,n)]
    for a in range(1,n):
        for b in range(a+1,n):
            if len(roads) == 50000:
                break
            roads.append((a,b,25000))
        if len(roads) == 50000:
            break
    assert len(roads) == 50000
    cases.append(('maximum-fields-roads-cows-time', encode(n,roads,cows,10000), 15000*10000,
                  [(0,-1)] + [(25000,0)]*(n-1)))
    cases.append(('one-field-maximum-positive-loops', encode(1,[(0,0,25000)]*50000,[10000],10000), 0, [(0,-1)]))

    invalid = ['0 0 1\n', '10001 10000 1\n', '3 1 1\n', '1 50001 1\n',
               '1 0 0\n', '1 0 10001\n', '1 0\n', 'one 0 1\n', '1 0 1 9\n',
               '2 1 1\n0\n', '1 0 1\n-1\n', '1 0 1\n10001\n', '1 0 1\nzero\n',
               '2 1 1\n0 0\n1 2\n', '2 1 1\n0 0\n1 2 5 6\n',
               '2 1 1\n0 0\n0 2 5\n', '2 1 1\n0 0\n1 3 5\n',
               '2 1 1\n0 0\n-2147483648 2 5\n', '2 1 1\n0 0\n2147483647 2 5\n',
               '2 1 1\n0 0\n1 2 0\n', '2 1 1\n0 0\n1 2 25001\n',
               '3 2 1\n0 0 0\n1 2 5\n1 2 6\n', '2 1 1\n0 0\n',
               '1 0 1\n0\nextra\n']
    sentinel = b'earlier answer\n'
    with tempfile.TemporaryDirectory(prefix='shortcut-pack-acceptance-') as temporary:
        roles = {}
        for role in ['starter', 'solution', 'probe']:
            cwd = Path(temporary) / role
            cwd.mkdir()
            source = learner if role in ['starter', 'probe'] else reference
            files = ['Main.java']
            if role == 'probe':
                marker = b'throw new UnsupportedOperationException("Complete the four Shortcut traffic tasks");'
                assert source.count(marker) == 1
                source = source.replace(marker, b'return ShortcutDriverProbe.solve(problem);')
                (cwd / 'ShortcutDriverProbe.java').write_text(PROBE)
                files.append('ShortcutDriverProbe.java')
            (cwd / 'Main.java').write_bytes(source)
            run([javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-Werror', *files], cwd, timeout=45)
            roles[role] = cwd
        for name, data, answer, state in cases:
            cwd = roles['solution']
            (cwd / 'shortcut.in').write_text(data)
            (cwd / 'shortcut.out').write_bytes(sentinel)
            assert run([java, '-ea', '-Xmx256m', 'Main'], cwd, timeout=60) == (b'', b'')
            assert (cwd / 'shortcut.out').read_text() == f'{answer}\n', name
            assert (cwd / 'shortcut.in').read_text() == data
            cwd = roles['probe']
            (cwd / 'shortcut.in').write_text(data)
            (cwd / 'expected-routes.txt').write_text(''.join(f'{distance} {parent}\n' for distance,parent in state))
            assert run([java, '-ea', '-Xmx256m', 'ShortcutHelperProbe'], cwd) == (b'', b'')
            assert not (cwd / 'shortcut.out').exists() and (cwd / 'shortcut.in').read_text() == data
        unfinished = 0
        for data in [r[1] for r in cases[:7] + cases[-3:]] + [sample.decode() + '\n\n']:
            cwd = roles['starter']
            (cwd / 'shortcut.in').write_text(data)
            for previous in [False, True]:
                output = cwd / 'shortcut.out'
                if previous:
                    output.write_bytes(sentinel)
                else:
                    output.unlink(missing_ok=True)
                out, err = run([java, '-ea', '-Xmx256m', 'Main'], cwd, expected=2)
                assert not out and b'Complete the four Shortcut traffic tasks' in err
                assert (output.read_bytes() == sentinel) if previous else not output.exists()
                assert (cwd / 'shortcut.in').read_text() == data
                unfinished += 1
        refused = 0
        for data, args in [(item, []) for item in invalid] + [(None, []), (sample.decode(), ['extra'])]:
            cwd = roles['starter']
            if data is None:
                (cwd / 'shortcut.in').unlink(missing_ok=True)
            else:
                (cwd / 'shortcut.in').write_text(data)
            for previous in [False, True]:
                output = cwd / 'shortcut.out'
                if previous:
                    output.write_bytes(sentinel)
                else:
                    output.unlink(missing_ok=True)
                out, err = run([java, '-ea', '-Xmx256m', 'Main', *args], cwd, expected=2)
                assert not out and b'Cannot solve Shortcut:' in err and b'Complete the four' not in err
                assert (output.read_bytes() == sentinel) if previous else not output.exists()
                refused += 1
        cwd = roles['probe']
        for name, data, answer, _ in cases[:7]:
            (cwd / 'shortcut.in').write_text(data)
            (cwd / 'shortcut.out').write_bytes(sentinel)
            assert run([java, '-ea', '-Xmx256m', 'ShortcutDriverProbe', 'normal'], cwd) == (b'', b'')
            assert (cwd / 'shortcut.out').read_text() == f'{answer}\n', name
        guards = 0
        for mode in ['negative', 'too-large']:
            (cwd / 'shortcut.in').write_bytes(sample)
            for previous in [False, True]:
                output = cwd / 'shortcut.out'
                if previous:
                    output.write_bytes(sentinel)
                else:
                    output.unlink(missing_ok=True)
                out, err = run([java, '-ea', '-Xmx256m', 'ShortcutDriverProbe', mode], cwd, expected=2)
                assert not out and b'Return total savings in 0..' in err
                assert (output.read_bytes() == sentinel) if previous else not output.exists()
                guards += 1
    after = {str(f.relative_to(pack)): hashlib.sha256(f.read_bytes()).hexdigest()
             for f in pack.rglob('*') if f.is_file()}
    assert before == after
    print(json.dumps(dict(event='gold-shortcut-pack-accepted', referenceFileCases=len(cases),
                          independentSimpleRouteGraphs=independent, suppliedHelperFileCases=len(cases),
                          suppliedHelperIndependentParents=True, towardBarnLexicographicTies=True,
                          fixedUsualRoutes=True, maximumFieldChain=True, maximumRoadCases=2,
                          maximumFields=10000, maximumRoads=50000, maximumCows=10000,
                          maximumWeight=25000, maximumShortcutTime=10000, longSavings=True,
                          tinyIndependentDriverCases=7, unfinishedLearnerCases=unfinished,
                          refusedInputCases=refused, invalidResultGuards=guards,
                          previousAnswerPreserved=True, learnerAlgorithmUnfinished=True,
                          originalRawReferenceSha256=ORIGINAL_SHA, referenceChangedLines=6,
                          historicalReferenceInvalidInputClaims=False, historicalJudgeRuntimeClaim=False,
                          sourceFilesUnchanged=True, roleSourceSha256={role: hashlib.sha256(
                              (pack / role / 'Main.java').read_bytes().replace(b'\r\n', b'\n')).hexdigest()
                              for role in ['starter', 'solution']})), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--javac', default='javac')
    parser.add_argument('--java', default='java')
    args = parser.parse_args()
    verify(Path(__file__).resolve().parents[1] / 'UG11-Shortcut', args.javac, args.java)
