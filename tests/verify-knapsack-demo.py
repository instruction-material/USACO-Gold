"""Check changed 0-1 demonstration datasets against independent subset search."""
import argparse
import datetime
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
TASK = os.environ.get('CLASSES_FAMILY_TASK_ID', 'gold-knapsack-demo-reference')


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def run(command, cwd):
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True)
    record = dict(parentTaskId=TASK, cwd=str(cwd), command=command,
                  pid=child.pid, parentPid=os.getpid(), startTime=now(),
                  timeoutSeconds=30)
    print(json.dumps(dict(event='start', **record)), flush=True)
    try:
        out, err = child.communicate(timeout=30)
        assert child.returncode == 0, (command, child.returncode, err.decode())
        assert not err, err.decode()
        return out.decode().replace('\r\n', '\n')
    except BaseException:
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.communicate()
        record['childProcessGroupCleanup'] = True
        raise
    finally:
        print(json.dumps(dict(event='end', **record, endTime=now(),
                              exitCode=child.returncode)), flush=True)


def verify(javac, java):
    path = ROOT / 'UG2-0-1-Knapsack/solution/Main.java'
    original = path.read_bytes()
    source = original.decode().replace('\r\n', '\n')
    cases = [([1,3,4,5],[1,4,5,7],7), ([2],[3],4), ([3],[7],6),
             ([2,3],[3,4],6), ([2,2],[3,3],4), ([1,2],[0,0],3),
             ([9,8],[2,3],3), ([1],[9],0), ([],[],0),
             ([1,3,4,5],[1,4,5,7],6)]
    with tempfile.TemporaryDirectory(prefix='gold-knapsack-demo-') as temp:
        directory = Path(temp)
        for weights, values, capacity in cases:
            candidate = source
            replacements = [
                ('int[] weights = {1, 3, 4, 5};', 'int[] weights = {' + ', '.join(map(str,weights)) + '};'),
                ('int[] values = {1, 4, 5, 7};', 'int[] values = {' + ', '.join(map(str,values)) + '};'),
                ('int numItems = 4;', 'int numItems = ' + str(len(weights)) + ';'),
                ('int maxWeight = 7;', 'int maxWeight = ' + str(capacity) + ';')
            ]
            for before, after in replacements:
                assert candidate.count(before) == 1
                candidate = candidate.replace(before, after)
            (directory / 'Main.java').write_text(candidate)
            run([javac, '--release', '17', '-encoding', 'UTF-8',
                 '-Xlint:all', '-Werror', 'Main.java'], directory)
            output = run([java, 'Main'], directory)
            match = re.fullmatch(r'Max value: (\d+)\nItem indicies in knapsack: \[([\d, ]*)\]\n', output)
            assert match, output
            indices = [int(value.strip()) for value in match[2].split(',') if value.strip()]
            assert len(indices) == len(set(indices)), (weights, values, capacity, indices)
            assert all(0 <= i < len(weights) for i in indices)
            assert sum(weights[i] for i in indices) <= capacity
            optimal = max(sum(values[i] for i, selected in enumerate(bits) if selected)
                          for bits in itertools.product([False, True], repeat=len(weights))
                          if sum(weights[i] for i, selected in enumerate(bits) if selected) <= capacity)
            assert sum(values[i] for i in indices) == optimal == int(match[1]), output
    assert path.read_bytes() == original
    print(json.dumps(dict(event='gold-knapsack-demo-reference-accepted',
                          parentTaskId=TASK, cases=len(cases),
                          independentSubsetOracle=True, anyOptimalSubsetAccepted=True,
                          selectedIndicesUnique=True, sourceUnchanged=True,
                          sourceSha256=hashlib.sha256(original).hexdigest(),
                          hardcodedDemonstrationOnly=True)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--javac', default='javac')
    parser.add_argument('--java', default='java')
    args = parser.parse_args()
    try:
        verify(args.javac, args.java)
    finally:
        print(json.dumps(dict(event='cleanup', parentTaskId=TASK,
                              pid=os.getpid(), time=now())), flush=True)
