"""Accept four historical algorithms and guarded, deliberately unfinished learners."""
import argparse
import datetime
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import re
import signal
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ['UG13-Cow-Routing', 'UG16-Watering-the-Fields', 'UG18-I-Would-Walk-500-Miles', 'UG2-Talent-Show']
STEMS = ['cowroute', 'irrigation', 'walk', 'talent']
ORIGINALS = ['5d0f9ea447c317af2f718331e3973eeabf7effb866586b1d2d0c37265b90e0a0',
             '2da86f5b9d64e2a54c025d3a8591a477c33ace132b1b2d20a68de3a1d4b9b0cd',
             'dac65c4628a09631d6fbd5287d4d59f8fd89cf5587c6195c01912bd81072afff',
             'ccb6bca2f2b0704e7012f7c07592acd6aafd4713eee261d5f98945224817d53a']
EDITS = [ [('number of cities traveled', 'number of individual flights')], [],
          [('M is simply the Kth largest value of the edges in the MST', 'CHANGED: M is the (K-1)th largest real MST edge; edges also includes the root zero')],
          [('dp[i][j] = using first i cows with weight j, what is the maximum value of', 'CHANGED: dp[i][j] uses cows 0 through i; j=W means total weight at least W'),
           ('sum of 1000 * t[i] - w[i]', 'CHANGED: maximize sum of 1000 * t[cow] - ratio * w[cow]')] ]
METHODS = ['static Result cheapestJourney(Input input)', 'static long minimumCost(Input input)',
           'static long maximumSpacing(Input input)', 'static long bestRatio(Input input)']
parser = argparse.ArgumentParser()
parser.add_argument('--javac', default='javac')
parser.add_argument('--java', default='java')
args = parser.parse_args()
counts = dict(compiledRoles=0, independentTinyCases=0, constructedFullLimitCases=0,
              preservedHistoricalFixtures=0, unfinishedLearnerRuns=0, refusedLearnerInputs=0,
              suppliedDriverProbes=0, invalidReturnedResults=0)
hashes = {}

def cancelled(sig, frame):
    raise KeyboardInterrupt('Historical application acceptance cancelled')

signal.signal(signal.SIGTERM, cancelled)

def run(command, cwd, success=True, timeout=60):
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True, start_new_session=True)
    record = dict(event='historical-application-command', parentTaskId=os.environ.get('CLASSES_FAMILY_TASK_ID', 'gold-historical-application-acceptance'),
                  command=command, cwd=str(cwd), pid=child.pid,
                  startTime=datetime.datetime.now(datetime.timezone.utc).isoformat(), timeoutSeconds=timeout,
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
        record.update(endTime=datetime.datetime.now(datetime.timezone.utc).isoformat(), exitCode=child.returncode)
        print(json.dumps(record), flush=True)
    result = subprocess.CompletedProcess(command, child.returncode, stdout, stderr)
    if success and child.returncode:
        raise AssertionError((command, child.returncode, stdout[-2000:], stderr[-2000:]))
    return result

def compile_role(directory):
    run([args.javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-Werror', 'Main.java'], directory)

def execute(directory, success=True):
    return run([args.java, '-ea', '-Xmx256m', 'Main'], directory, success=success)

def cowroute(a, b, routes):
    # Independent bounded relaxation by number of ticket boardings, not Dijkstra.
    distances = {a: (0, 0)}
    cities = {city for _, stops in routes for city in stops} | {a, b}
    for _ in cities:
        following = dict(distances)
        for price, stops in routes:
            for i, origin in enumerate(stops):
                if origin not in distances:
                    continue
                money, flights = distances[origin]
                for j in range(i + 1, len(stops)):
                    candidate = money + price, flights + j - i
                    if candidate < following.get(stops[j], (float('inf'), float('inf'))):
                        following[stops[j]] = candidate
        distances = following
    data = [f'{a} {b} {len(routes)}']
    for price, stops in routes:
        data.extend([f'{price} {len(stops)}', ' '.join(map(str, stops))])
    return '\n'.join(data)+'\n', ' '.join(map(str, distances.get(b, (-1, -1))))+'\n'

def irrigation(points, cutoff):
    edges = [(a, b, sum((x-y)**2 for x, y in zip(points[a], points[b])))
             for a, b in itertools.combinations(range(len(points)), 2)]
    edges = [edge for edge in edges if edge[2] >= cutoff]
    best = None
    for chosen in itertools.combinations(edges, len(points)-1):
        reached = {0}
        for _ in points:
            for a, b, _ in chosen:
                if a in reached: reached.add(b)
                if b in reached: reached.add(a)
        if len(reached) == len(points):
            value = sum(edge[2] for edge in chosen)
            best = value if best is None else min(best, value)
    return f'{len(points)} {cutoff}\n'+''.join(f'{x} {y}\n' for x, y in points), f'{-1 if best is None else best}\n'

def walk(n, k):
    # All unlabelled partitions, independent of spanning trees and order statistics.
    best = -1
    def visit(groups):
        nonlocal best
        count = max(groups)+1
        if count > k or count+n-len(groups) < k:
            return
        if len(groups) == n:
            if count == k:
                spacing = min((2019201913*(a+1)+2019201949*(b+1)) % 2019201997
                              for a, b in itertools.combinations(range(n), 2) if groups[a] != groups[b])
                best = max(best, spacing)
            return
        for group in range(count+1):
            visit(groups+[group])
    visit([0])
    assert best >= 0
    return f'{n} {k}\n', f'{best}\n'

def talent(cows, threshold):
    # Exact enumeration of subsets; no ratio search, clamping or DP.
    best = -1
    for mask in range(1, 1 << len(cows)):
        weight = sum(w for i, (w, _) in enumerate(cows) if mask & (1 << i))
        if weight >= threshold:
            total = sum(t for i, (_, t) in enumerate(cows) if mask & (1 << i))
            best = max(best, 1000*total//weight)
    assert best >= 0
    return f'{len(cows)} {threshold}\n'+''.join(f'{w} {t}\n' for w, t in cows), f'{best}\n'

rng = random.Random(11102026)
tiny = [
 [cowroute(3,4,[(3,[1,2,3,4,5]),(2,[3,5,4]),(1,[1,5])]),
  cowroute(1,4,[(2,[1,4]),(2,[1,2,3,4])]),
  cowroute(1,4,[(1000000000,[1,2]),(1000000000,[2,3]),(1000000000,[3,4])]),
  cowroute(1,4,[(1,[4,1])]), cowroute(3,2,[(1,[1,2,3,4]),(1,[4,1])]),
  cowroute(1,1,[(1,[1,2])])],
 [irrigation([(0,2),(5,0),(4,3)],11), irrigation([(0,0)],1),
  irrigation([(0,0),(3,4)],25), irrigation([(0,0),(3,4)],26),
  irrigation([(0,0),(1000,0),(1000,1000),(0,1000)],1000000)],
 [walk(n,k) for n in range(2,7) for k in range(2,n+1)],
 [talent([(20,21),(10,11),(30,31)],15), talent([(1,1000)],1),
  talent([(1000000,1)],1000), talent([(1,1),(2,1)],1),
  talent([(5,3),(3,2),(7,6),(10,9)],8), talent([(3,7),(2,4),(1,1)],6)]
]
for _ in range(8):
    routes = [(rng.randint(1,10), rng.sample(range(1,7), rng.randint(1,5))) for _ in range(rng.randint(1,5))]
    tiny[0].append(cowroute(rng.randint(1,6), rng.randint(1,6), routes))
    points = rng.sample(list(itertools.product(range(7), repeat=2)), rng.randint(1,5))
    tiny[1].append(irrigation(points, rng.randint(1,30)))
    cows = [(rng.randint(1,20),rng.randint(1,30)) for _ in range(rng.randint(1,8))]
    tiny[3].append(talent(cows, rng.randint(1,sum(w for w,_ in cows))))

# Independent constructed full limits, with exact rather than timing-only acceptance.
route_stops = [list(range(start,min(start+100,1001))) for start in range(1,1000,99)]
assert len(route_stops) == 11 and route_stops[-1][-1] == 1000
route_stops += [list(range(1,101)) for _ in range(1000-len(route_stops))]
cow_full = ['1 1000 1000']
for stops in route_stops:
    cow_full.extend([f'1000000000 {len(stops)}',' '.join(map(str,stops))])
water_full = ['2000 1000000']+[f'{x} {y}' for y in [0,1000] for x in range(1000)]
# Two small opposite-corner clusters have no eligible internal edges.
# B's (969,969) uniquely minimizes each A vertex's incident edge. A's
# (30,31) uniquely minimizes each B vertex's incident edge: it dominates
# all other A points except (31,0..7), whose cost is larger by at least
# 48*969-2*1000-851. The singleton-cut edges form one tree with a long total.
cluster_a = [(x,y) for x in range(32) for y in range(32)][:1000]
cluster_b = [(x+969,y+969) for x,y in cluster_a]
a_root, b_root = (30,31), (969,969)
square = lambda a,b: sum((x-y)**2 for x,y in zip(a,b))
corner_total = sum(square(a,b_root) for a in cluster_a) + sum(square(a_root,b) for b in cluster_b[1:])
assert corner_total > 2147483647
water_long = '2000 1000000\n'+''.join(f'{x} {y}\n' for x,y in cluster_a+cluster_b)
# For x<y<=7500, weights=P-84*x-48*y. Each vertex x<N has its unique
# cheapest incident edge to N, proving the star MST by the singleton cut property.
for n in range(2,7):
    for k in range(2,n+1):
        assert walk(n,k)[1] == f'{2019201997-48*n-84*(k-1)}\n'
full = [
 [('\n'.join(cow_full)+'\n','11000000000 999\n')],
 [('\n'.join(water_full)+'\n','1999000999\n'), (water_long,f'{corner_total}\n')],
 [('7500 2\n',f'{2019201997-48*7500-84}\n'), ('7500 7500\n',f'{2019201997-48*7500-84*7499}\n')],
 [('250 1000\n'+'4 1000\n'*250,'250000\n'), ('250 1000\n'+'1000000 1000\n'*250,'1\n')]
]
invalid_inputs = [
 ['0 2 1\n1 2\n1 2\n','1 1001 1\n1 2\n1 2\n','1 2 0\n','1 2 1001\n',
  '1 2 1\n0 2\n1 2\n','1 2 1\n1000000001 2\n1 2\n','1 2 1\n1 101\n',
  '1 2 1\n1 2\n1 1\n','1 2 1\n1 2\n1\n','1 2 1\n1 2\n1 2\nextra\n'],
 ['0 1\n','2001 1\n','1 0\n0 0\n','1 1000001\n0 0\n','1 1\n1001 0\n',
  '1 1\n0 -1\n','2 1\n0 0\n0 0\n','1 1\n0\n','1 1\n0 0\nextra\n'],
 ['1 2\n','7501 2\n','3 1\n','3 4\n','3\n','3 2 extra\n','x 2\n'],
 ['0 1\n','251 1\n','1 0\n','1 1001\n1 1\n','1 1\n0 1\n','1 1\n1000001 1\n',
  '1 1\n1 1001\n','1 2\n1 1\n','1 1\n1\n','1 1\n1 1\nextra\n']
]
sample_answers = ['return new Result(2,2);','return 46;','return 2019201769L;','return 1066;']
sample_outputs = ['2 2\n','46\n','2019201769\n','1066\n']
full_probes = [
 'if(input.start!=1||input.destination!=1000||input.prices.length!=1000||input.prices[999]!=1000000000||input.stops[999].length!=100) throw new AssertionError("route parse"); return new Result(11000000000L,999);',
 'if(input.x.length!=2000||input.cutoff!=1000000||input.x[1999]!=999||input.y[1999]!=1000) throw new AssertionError("point parse"); return 1999000999L;',
 'if(input.n!=7500||input.groups!=7500) throw new AssertionError("group parse"); return 2018212081L;',
 'if(input.weights.length!=250||input.threshold!=1000||input.weights[249]!=1000000||input.talents[249]!=1000) throw new AssertionError("cow parse"); return 1;'
]
bad_results = [['return null;','return new Result(0,0);','return new Result(-1,2);','return new Result(1000000000000L,1);','return new Result(1,1000);'],
               ['return -2;','return 0;','return 4000001L;'], ['return 0;','return 2019201997L;'],
               ['return -1;','return 1000001;']]

def injected(source, signature, body):
    pattern = re.escape(signature)+r' \{.*?\n    \}'
    result, count = re.subn(pattern, signature+' {\n        '+body+'\n    }', source, count=1, flags=re.S)
    assert count == 1
    return result

for folder, stem, expected, changes in zip(FOLDERS,STEMS,ORIGINALS,EDITS):
    base = ROOT/folder
    raw = (base/'legacy/Main.java').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected
    maintained = raw.decode().replace('\r\n','\n')
    for before, after in changes:
        assert maintained.count(before) == 1
        maintained = maintained.replace(before, after)
    assert (base/'solution/Main.java').read_text() == maintained, folder
    for role in ['starter','solution']:
        guide = (base/role/'README.md').read_text()
        assert all(text in guide for text in ['## Contract','## Prediction','## Tasks and walkthrough','## State and reasoning','## Build and run','## Independent checks','JDK 17','PowerShell',stem+'.in',stem+'.out'])
        file = base/role/'Main.java'
        hashes[f'{folder}/{role}'] = hashlib.sha256(file.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    assert (base/'starter/Main.java').read_text().count('// TODO ') == 4
    assert (base/'starter/Main.java').read_text() != maintained

with tempfile.TemporaryDirectory(prefix='gold-historical-applications-') as temporary:
    work = Path(temporary)
    for index, (folder,stem) in enumerate(zip(FOLDERS,STEMS)):
        directories = {}
        for role in ['starter','solution']:
            directory = work/folder/role
            directory.mkdir(parents=True)
            (directory/'Main.java').write_bytes((ROOT/folder/role/'Main.java').read_bytes())
            compile_role(directory)
            counts['compiledRoles'] += 1
            directories[role] = directory
        directory = directories['solution']
        for data, expected in tiny[index]:
            (directory/(stem+'.in')).write_text(data)
            execute(directory)
            assert (directory/(stem+'.out')).read_text() == expected, (folder,data,expected)
            counts['independentTinyCases'] += 1
        for data, expected in full[index]:
            (directory/(stem+'.in')).write_text(data)
            execute(directory)
            assert (directory/(stem+'.out')).read_text() == expected, (folder,expected)
            counts['constructedFullLimitCases'] += 1
        if index == 3:
            (directory/'talent.in').write_bytes((ROOT/folder/'solution/talent.in').read_bytes())
            execute(directory)
            assert (directory/'talent.out').read_text() == (ROOT/folder/'solution/talent.out').read_text() == '26706\n'
            counts['preservedHistoricalFixtures'] += 1
        directory = directories['starter']
        sample = (ROOT/folder/'starter'/(stem+'.in')).read_text()
        answer_file = directory/(stem+'.out')
        input_file = directory/(stem+'.in')
        input_file.write_text(sample)
        previous = b'keep the saved earlier answer\n'
        for has_answer in [True,False]:
            if has_answer: answer_file.write_bytes(previous)
            else: answer_file.unlink()
            result = execute(directory,success=False)
            assert result.returncode == 2 and not result.stdout and 'Complete' in result.stderr
            assert (answer_file.read_bytes() == previous) if has_answer else not answer_file.exists()
            counts['unfinishedLearnerRuns'] += 1
        for data in invalid_inputs[index]+[None]:
            answer_file.write_bytes(previous)
            if data is None: input_file.unlink()
            else: input_file.write_text(data)
            result = execute(directory,success=False)
            assert result.returncode == 2 and not result.stdout and 'Complete' not in result.stderr
            assert answer_file.read_bytes() == previous
            counts['refusedLearnerInputs'] += 1
        # These constant-answer copies probe parsing/output only, never a learner algorithm.
        original = (ROOT/folder/'starter/Main.java').read_text()
        input_file.write_text(sample)
        (directory/'Main.java').write_text(injected(original,METHODS[index],sample_answers[index]))
        compile_role(directory)
        execute(directory)
        assert answer_file.read_text() == sample_outputs[index]
        counts['suppliedDriverProbes'] += 1
        data, expected = full[index][0 if index == 1 else -1]
        input_file.write_text(data)
        (directory/'Main.java').write_text(injected(original,METHODS[index],full_probes[index]))
        compile_role(directory)
        execute(directory)
        assert answer_file.read_text() == expected
        counts['suppliedDriverProbes'] += 1
        input_file.write_text(sample)
        for body in bad_results[index]:
            (directory/'Main.java').write_text(injected(original,METHODS[index],body))
            compile_role(directory)
            answer_file.write_bytes(previous)
            result = execute(directory,success=False)
            assert result.returncode == 2 and not result.stdout
            assert answer_file.read_bytes() == previous
            counts['invalidReturnedResults'] += 1
        # The start is reachable from itself and a single point costs zero.
        if index in [0,1]:
            input_file.write_text('1 1 1\n1 2\n1 2\n' if index == 0 else '1 1\n0 0\n')
            bad = 'return new Result(-1,-1);' if index == 0 else 'return -1;'
            (directory/'Main.java').write_text(injected(original,METHODS[index],bad))
            compile_role(directory)
            answer_file.write_bytes(previous)
            assert execute(directory,success=False).returncode == 2
            assert answer_file.read_bytes() == previous
            counts['invalidReturnedResults'] += 1

for key, expected in hashes.items():
    folder, role = key.split('/')
    assert hashlib.sha256((ROOT/folder/role/'Main.java').read_bytes().replace(b'\r\n',b'\n')).hexdigest() == expected
print(json.dumps(dict(event='verified-historical-algorithm-packs',passed=True,counts=counts,
                     sourceHashes=hashes,temporaryCopiesRemoved=True,learnerAlgorithmsRemainUnfinished=True)),flush=True)
