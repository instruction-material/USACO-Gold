"""Accept three native references and the supplied unfinished learner infrastructure."""
import argparse
import datetime
import difflib
import hashlib
import itertools
import json
import math
import os
from pathlib import Path
import random
import signal
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ['UG1-Dynamic-Programming-Practice', 'UG14-MST-II', 'UG19-Disjoint-Sets-and-Kruskals']
ORIGINALS = ['b123b64668574f319000a0b51a3046b89fd19f9d606f09ac91afcdfa62c586e1',
             '26261b69d4cfb08aae319d76a89516ee97f7f3c1e049f043ddb96deb6a545dd5',
             '2115b4bb148c8810a6ddf06bb52c2e050c946146fa665f6b6deba4f9ce7e3000']
parser = argparse.ArgumentParser()
parser.add_argument('--javac', default='javac')
parser.add_argument('--java', default='java')
args = parser.parse_args()
counts = dict(referenceCases=0, learnerUnfinished=0, refusedLearnerInput=0, suppliedDriverProbes=0,
              invalidReturnedResults=0, independentTinyTrees=0, dpIndependentCases=0,
              referenceRefusedDisconnected=0, maximumPrimVertices=2000,
              maximumKruskalVertices=200000, maximumEdgeCases=0)
source_hashes = {}
raw_source_hashes = {}


def cancelled(signum, frame):
    raise KeyboardInterrupt(f'Acceptance cancelled by signal {signum}')


signal.signal(signal.SIGTERM, cancelled)


def run(command, cwd, success=True, timeout=40):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    record = dict(event='implementation-lab-command', parentTaskId=os.environ.get('CLASSES_FAMILY_TASK_ID', 'gold-implementation-lab-acceptance'),
                  cwd=str(cwd), command=command, pid=child.pid, startTime=started, timeoutSeconds=timeout, childProcessGroupCleanup=False)
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
        record.update(endTime=datetime.datetime.now(datetime.timezone.utc).isoformat(), exitCode=child.returncode)
        print(json.dumps(record), flush=True)
    result = subprocess.CompletedProcess(command, child.returncode, stdout, stderr)
    if stdout or stderr:
        print(json.dumps(dict(event='implementation-lab-output', pid=child.pid, stdout=stdout, stderr=stderr)), flush=True)
    if success and result.returncode:
        raise AssertionError((command, result.returncode, result.stdout[-3000:], result.stderr[-3000:]))
    return result


def compile_role(directory, extra=None):
    files = ['Main.java']
    if extra is not None:
        (directory / 'Probe.java').write_text(extra)
        files.append('Probe.java')
    run([args.javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-Werror', *files], directory)


def java(directory, target='Main', success=True, properties=()):
    return run([args.java, '-ea', '-Xmx256m', *properties, target], directory, success=success, timeout=60)


def literal(array):
    return 'new int[]{' + ','.join(map(str, array)) + '}'


def items_literal(items):
    return 'new int[][]{' + ','.join('{' + f'{w},{v}' + '}' for w, v in items) + '}'


def mst_oracle(n, edges):
    best, chosen = None, None
    for subset in itertools.combinations(range(len(edges)), n - 1):
        reached = {0}
        while True:
            after = reached | {edges[i][1] for i in subset if edges[i][0] in reached} | {edges[i][0] for i in subset if edges[i][1] in reached}
            if after == reached:
                break
            reached = after
        if len(reached) == n:
            total = sum(edges[i][2] for i in subset)
            if best is None or total < best:
                best, chosen = total, subset
    assert chosen is not None
    return best, chosen


def graph_text(n, edges):
    return f'{n} {len(edges)}\n' + ''.join(f'{a} {b} {w}\n' for a, b, w in edges)


def connected(n, selected):
    reached = {0}
    while True:
        after = reached | {b for a, b, _ in selected if a in reached} | {a for a, b, _ in selected if b in reached}
        if after == reached:
            return len(reached) == n
        reached = after


for folder, original in zip(FOLDERS, ORIGINALS):
    root = ROOT / folder
    assert hashlib.sha256((root / 'legacy/Main.java').read_bytes()).hexdigest() == original
    for role in ['starter', 'solution']:
        file = root / role / 'Main.java'
        raw_source_hashes[f'{folder}/{role}'] = hashlib.sha256(file.read_bytes()).hexdigest()
        source_hashes[f'{folder}/{role}'] = hashlib.sha256(file.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        guide = (root / role / 'README.md').read_text()
        assert all(word in guide for word in ['## Contract', '## Prediction', '## Build and run', '## Independent checks', 'JDK 17', 'PowerShell'])
    assert (root / 'starter/Main.java').read_bytes() != (root / 'solution/Main.java').read_bytes()
    assert (root / 'starter/Main.java').read_text().count('// TODO ') == 4

with tempfile.TemporaryDirectory(prefix='implementation-labs-') as temporary:
    work = Path(temporary)
    directories = {}
    for folder in FOLDERS:
        for role in ['starter', 'solution']:
            directory = work / folder / role
            directory.mkdir(parents=True)
            (directory / 'Main.java').write_bytes((ROOT / folder / role / 'Main.java').read_bytes())
            directories[(folder, role)] = directory
            compile_role(directory)

    # Independent interval, binomial and subset models, including item zero and zero capacity.
    rng = random.Random(1102026)
    arrays = [[], [-3], [-2, -4], [5, -5, 6, 2, 3], [1000000] * 2000]
    arrays += [[rng.randint(-8, 8) for _ in range(rng.randrange(9))] for _ in range(20)]
    dp_lines = []
    for values in arrays:
        expected = 2000000000 if len(values) == 2000 else max([0] + [sum(values[a:b]) for a in range(len(values)) for b in range(a + 1, len(values) + 1)])
        dp_lines.append(f'if (Main.maxSubarraySum({literal(values)}) != {expected}) throw new AssertionError("subarray");')
    for rows, columns in list(itertools.product(range(1, 7), repeat=2)) + [(15, 15)]:
        dp_lines.append(f'if (Main.numPaths({rows},{columns}) != {math.comb(rows + columns - 2, rows - 1)}) throw new AssertionError("grid");')
    knapsacks = [([], 0), ([(1, 5)], 1), ([(0, 3), (0, 5)], 0),
                 ([(1, 5), (2, 3), (4, 5), (2, 3), (5, 2)], 10)]
    knapsacks += [([(rng.randrange(9), rng.randrange(11)) for _ in range(rng.randrange(9))], rng.randrange(21)) for _ in range(20)]
    for items, capacity in knapsacks:
        expected = max(sum(v for i, (_, v) in enumerate(items) if mask & (1 << i)) for mask in range(1 << len(items))
                       if sum(w for i, (w, _) in enumerate(items) if mask & (1 << i)) <= capacity)
        dp_lines.append(f'if (Main.knapsackRecursive({len(items)-1},{capacity},{items_literal(items)}) != {expected}) throw new AssertionError("knapsack");')
    dp_lines.append('if (Main.knapsackRecursive(19,0,' + items_literal([(0, 1000000)] * 20) + ') != 20000000) throw new AssertionError("largest item count");')
    dp_lines.append('int[][] kept={{0,4},{1,5}}; int[][] before={{0,4},{1,5}}; Main.knapsackRecursive(1,1,kept); if(!java.util.Arrays.deepEquals(kept,before)) throw new AssertionError("mutated items");')
    directory = directories[(FOLDERS[0], 'solution')]
    compile_role(directory, 'class Probe { public static void main(String[] args) {' + '\n'.join(dp_lines) + '} }\n')
    java(directory, 'Probe')
    assert java(directory).stdout == '11\n3\n16\n'
    counts['dpIndependentCases'] = len(dp_lines)
    counts['referenceCases'] += len(dp_lines) + 1
    directory = directories[(FOLDERS[0], 'starter')]
    unfinished = java(directory, success=False)
    assert unfinished.returncode == 2 and not unfinished.stdout and 'Complete' in unfinished.stderr
    counts['learnerUnfinished'] += 1
    invalid_parameters = ['Main.validate(new int[]{},0,1,new int[][]{},0);',
                          'Main.validate(new int[]{1000001},1,1,new int[][]{},0);',
                          'Main.validate(new int[]{},1,16,new int[][]{},0);',
                          'Main.validate(new int[]{},1,1,new int[][]{{-1,1}},0);',
                          'Main.validate(new int[]{},1,1,new int[][]{{0,1}},-1);',
                          'Main.validate(new int[]{},1,1,new int[21][2],0);']
    validate_probe = 'class Probe { public static void main(String[] args) { Main.validate(new int[]{},1,1,new int[][]{{0,3}},0);'
    for call in invalid_parameters:
        validate_probe += 'try {' + call + 'throw new AssertionError("accepted invalid dataset");} catch(IllegalArgumentException expected) {}'
    compile_role(directory, validate_probe + '} }\n')
    java(directory, 'Probe')
    counts['refusedLearnerInput'] += len(invalid_parameters)
    counts['suppliedDriverProbes'] += 1

    tokens = (ROOT / FOLDERS[2] / 'solution/kruskal.in').read_text().split()
    sample_n, sample_m = map(int, tokens[:2])
    sample_edges = [tuple(map(int, tokens[i:i+3])) for i in range(2, len(tokens), 3)]
    assert len(sample_edges) == sample_m and mst_oracle(sample_n, sample_edges)[0] == 33
    graphs = [(sample_n, sample_edges), (1, []), (2, [(0, 1, 1), (0, 1, 9)]),
              (4, [(0, 1, 1000000000), (1, 2, 1000000000), (2, 3, 1000000000)]),
              (3, [(0, 0, 0), (0, 1, 0), (1, 2, 0), (0, 2, 0)])]
    for _ in range(18):
        size = rng.randrange(2, 6)
        edges = [(i - 1, i, rng.randrange(12)) for i in range(1, size)]
        edges += [(rng.randrange(size), rng.randrange(size), rng.randrange(12)) for _ in range(4)]
        graphs.append((size, edges))
    counts['independentTinyTrees'] = len(graphs)
    chosen_sample = mst_oracle(sample_n, sample_edges)[1]
    for folder, stem in [(FOLDERS[1], 'prim'), (FOLDERS[2], 'kruskal')]:
        reference = directories[(folder, 'solution')]
        if stem == 'kruskal':
            compile_role(reference, '''class Probe { public static void main(String[] args) throws Exception {
                Main.main(args); long total=0; for(Main.Edge e:Main.mst) total+=e.weight;
                System.out.println("CHECK_TOTAL="+total);
                for(Main.Edge e:Main.mst) System.out.println("CHECK_EDGE="+e.p+" "+e.q+" "+e.weight);
            } }''')
        for n, edges in graphs:
            (reference / (stem + '.in')).write_text(graph_text(n, edges))
            result = java(reference, 'Probe' if stem == 'kruskal' else 'Main')
            output = (reference / (stem + '.out')).read_text()
            expected, _ = mst_oracle(n, edges)
            if stem == 'prim':
                assert not result.stdout
                rows = output.splitlines()
                assert len(rows) == n and rows[-1] == 'Total Distance: ' + str(expected)
                parents = [tuple(map(int, line.split())) for line in rows[:-1]]
                assert [v for v, _ in parents] == list(range(1, n))
                selected = [(v, p, min(w for a, b, w in edges if {a,b} == {v,p})) for v, p in parents]
            else:
                selected = [tuple(map(int, line.partition('=')[2].split())) for line in result.stdout.splitlines() if line.startswith('CHECK_EDGE=')]
                assert f'CHECK_TOTAL={expected}\n' in result.stdout
                assert output == ''.join(f'{a} {b}\n' for a, b, _ in selected)
                assert all(edge in edges for edge in selected)
            assert len(selected) == n - 1 and connected(n, selected) and sum(w for _, _, w in selected) == expected
            counts['referenceCases'] += 1
            learner = directories[(folder, 'starter')]
            (learner / (stem + '.in')).write_text(graph_text(n, edges))
            (learner / (stem + '.out')).write_text('KEEP PREVIOUS ANSWER\n')
            refusal = java(learner, success=False)
            assert refusal.returncode == 2 and not refusal.stdout
            assert 'Complete' in refusal.stderr and (learner / (stem + '.out')).read_text() == 'KEEP PREVIOUS ANSWER\n'
            counts['learnerUnfinished'] += 1
        # Published sample output is an independently checked prediction.
        (reference / (stem + '.in')).write_text(graph_text(sample_n, sample_edges))
        java(reference)
        assert (reference / (stem + '.out')).read_text() == (ROOT / folder / 'solution' / (stem + '.out')).read_text()
        if stem == 'kruskal':
            assert not java(reference).stdout
            trace = java(reference, properties=['-Dcourse.trace=true']).stdout
            assert 'parent:' in trace and 'weight:' in trace and 'count: 1' in trace
            compile_role(reference, '''class Probe { public static void main(String[] args) {
                Main.DisjointSets sets=new Main.DisjointSets(1024);
                for(int step=1;step<1024;step*=2) for(int p=0;p<1024;p+=2*step) sets.connect(p,p+step);
                if(sets.count()!=1 || !sets.connected(0,1023)) throw new AssertionError("DSU invariant");
                sets.connect(0,1023); if(sets.count()!=1) throw new AssertionError("repeated union");
            } }''')
            java(reference, 'Probe')
            counts['referenceCases'] += 2
        (reference / (stem + '.in')).write_text('3 1\n0 1 2\n')
        (reference / (stem + '.out')).write_text('KEEP PREVIOUS ANSWER\n')
        refused = java(reference, success=False)
        assert refused.returncode != 0 and (reference / (stem + '.out')).read_text() == 'KEEP PREVIOUS ANSWER\n'
        counts['referenceRefusedDisconnected'] += 1

        learner = directories[(folder, 'starter')]
        bad_inputs = ['0 0\n', '2 -1\n', '2 1\n0 2 1\n', '2 1\n0 1 -1\n',
                      '2 1\n0 1 1000000001\n', '2 1\n0 1\n', '2 1\n0 1 1\nextra\n']
        for text in bad_inputs:
            (learner / (stem + '.in')).write_text(text)
            refusal = java(learner, success=False)
            assert refusal.returncode == 2 and not refusal.stdout
            assert (learner / (stem + '.out')).read_text() == 'KEEP PREVIOUS ANSWER\n'
            counts['refusedLearnerInput'] += 1
        (learner / (stem + '.in')).write_text(graph_text(sample_n, sample_edges))
        if stem == 'prim':
            parents = [-1] * sample_n
            reached = {0}
            while len(reached) < sample_n:
                for index in chosen_sample:
                    a, b, _ = sample_edges[index]
                    if a in reached and b not in reached: parents[b] = a; reached.add(b)
                    elif b in reached and a not in reached: parents[a] = b; reached.add(a)
            driver = 'class Probe { public static void main(String[] args) throws Exception { Main.Graph g=Main.readGraph(java.nio.file.Path.of("prim.in")); int[] p=' + literal(parents) + '; if(Main.outputLines(g,new Main.Result(p,33)).size()!=6) throw new AssertionError();'
            driver += 'try { Main.outputLines(g,new Main.Result(p,34)); throw new AssertionError("bad total"); } catch(IllegalArgumentException expected) {}'
            driver += 'p[0]=0; try { Main.outputLines(g,new Main.Result(p,33)); throw new AssertionError("bad root"); } catch(IllegalArgumentException expected) {}'
            driver += 'p[0]=-1; p[2]=5; p[5]=2; try { Main.outputLines(g,new Main.Result(p,33)); throw new AssertionError("cycle"); } catch(IllegalArgumentException expected) {}'
            driver += '} }'
        else:
            driver = 'class Probe { public static void main(String[] args) throws Exception { Main.Graph g=Main.readGraph(java.nio.file.Path.of("kruskal.in")); java.util.List<Main.Edge> chosen=new java.util.ArrayList<>();'
            driver += ''.join(f'chosen.add(g.edges.get({index}));' for index in chosen_sample)
            driver += 'if(Main.outputLines(g,chosen).size()!=5) throw new AssertionError();'
            driver += 'chosen.set(0,new Main.Edge(0,5,2)); try { Main.outputLines(g,chosen); throw new AssertionError("foreign edge"); } catch(IllegalArgumentException expected) {}'
            driver += 'chosen.clear(); try { Main.outputLines(g,chosen); throw new AssertionError("missing edges"); } catch(IllegalArgumentException expected) {}'
            driver += 'for(int i=0;i<5;i++) chosen.add(g.edges.get(0)); try { Main.outputLines(g,chosen); throw new AssertionError("disconnected selection"); } catch(IllegalArgumentException expected) {}'
            driver += '} }'
        compile_role(learner, driver)
        java(learner, 'Probe')
        counts['suppliedDriverProbes'] += 1
        counts['invalidReturnedResults'] += 3
        # Maximum native inputs use a known unique chain optimum, outside the tiny enumeration oracle.
        largest_n = 2000 if stem == 'prim' else 200000
        chain = [(i-1, i, 1000000000) for i in range(1, largest_n)]
        if stem == 'kruskal': chain.append((0, 0, 0))
        (reference / (stem + '.in')).write_text(graph_text(largest_n, chain))
        normal = java(reference)
        assert not normal.stdout
        lines = (reference / (stem + '.out')).read_text().splitlines()
        if stem == 'prim':
            assert len(lines) == largest_n and lines[-1] == f'Total Distance: {(largest_n-1)*1000000000}'
        else:
            assert len(lines) == largest_n - 1
            assert all(tuple(map(int, line.split())) == (i-1, i) for i, line in enumerate(lines, 1))
            counts['maximumEdgeCases'] += 1
        counts['referenceCases'] += 1
        (learner / (stem + '.in')).write_text(graph_text(largest_n, chain))
        probe = ('class Probe { public static void main(String[] args) throws Exception { Main.Graph g=Main.readGraph(java.nio.file.Path.of("prim.in")); int[] parents=new int[g.n]; parents[0]=-1; for(int i=1;i<g.n;i++) parents[i]=i-1; if(Main.outputLines(g,new Main.Result(parents,1999000000000L)).size()!=2000) throw new AssertionError(); } }' if stem == 'prim' else
                 'class Probe { public static void main(String[] args) throws Exception { Main.Graph g=Main.readGraph(java.nio.file.Path.of("kruskal.in")); if(g.n!=200000 || Main.outputLines(g,g.edges.subList(0,g.n-1)).size()!=199999) throw new AssertionError(); } }')
        compile_role(learner, probe)
        java(learner, 'Probe')
        counts['suppliedDriverProbes'] += 1
        # Maximum edge-count parsing and supplied feasible-output validation, without solving learner tasks.
        many_edges = [(0, 1, 1)] * 200000
        (reference / (stem + '.in')).write_text(graph_text(2, many_edges))
        java(reference)
        assert len((reference / (stem + '.out')).read_text().splitlines()) == (2 if stem == 'prim' else 1)
        (learner / (stem + '.in')).write_text(graph_text(2, many_edges))
        probe = ('class Probe { public static void main(String[] args) throws Exception { Main.Graph g=Main.readGraph(java.nio.file.Path.of("prim.in")); if(Main.outputLines(g,new Main.Result(new int[]{-1,0},1)).size()!=2) throw new AssertionError(); } }' if stem == 'prim' else
                 'class Probe { public static void main(String[] args) throws Exception { Main.Graph g=Main.readGraph(java.nio.file.Path.of("kruskal.in")); if(g.edges.size()!=200000 || Main.outputLines(g,java.util.List.of(g.edges.get(0))).size()!=1) throw new AssertionError(); } }')
        compile_role(learner, probe)
        java(learner, 'Probe')
        counts['referenceCases'] += 1
        counts['maximumEdgeCases'] += 1
        counts['suppliedDriverProbes'] += 1

for key, digest in raw_source_hashes.items():
    assert hashlib.sha256((ROOT / key / 'Main.java').read_bytes()).hexdigest() == digest
changes = {folder: sum(line.startswith('+') or line.startswith('-') for line in list(difflib.unified_diff((ROOT / folder / 'legacy/Main.java').read_text().splitlines(), (ROOT / folder / 'solution/Main.java').read_text().splitlines()))[2:]) for folder in FOLDERS}
assert changes[FOLDERS[0]] == 2
print(json.dumps(dict(event='gold-implementation-labs-accepted', **counts,
                      sourceFilesUnchanged=True, learnerAlgorithmsUnfinished=True, previousAnswersPreserved=True,
                      originalRawSha256=dict(zip(FOLDERS, ORIGINALS)), roleSourceSha256=source_hashes,
                      referenceDiffAddedRemovedLines=changes, standaloneRoleContracts=6,
                      knapsackIncludesFirstItemAndZeroWeight=True, emptySubarrayAllowed=True,
                      priorityQueueUsesDenseMatrix=True, kruskalUnionBySizeWithoutCompression=True,
                      traceIsExplicit=True, nativeRelease17StrictCompile=True)))
