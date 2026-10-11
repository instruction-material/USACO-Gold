"""Accept actual cyclic-gesture answers and the unfinished learner file boundary."""
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
PACK = ROOT / 'UG1-Hoof-Paper-Scissors'
ORIGINAL_SHA256 = '3438856bc7e19bc3e75f531e9958f04015976f14197479129828c39d8c950dd0'
parser = argparse.ArgumentParser()
parser.add_argument('--javac', default='javac')
parser.add_argument('--java', default='java')
args = parser.parse_args()


def cancel(sig, frame):
    raise KeyboardInterrupt('Hoof Paper Scissors acceptance cancelled')


signal.signal(signal.SIGTERM, cancel)


def run(command, cwd, success=True, timeout=60):
    child = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True, start_new_session=True)
    record = dict(event='hps-acceptance-command', parentTaskId=os.environ.get('CLASSES_FAMILY_TASK_ID', 'gold-hps-acceptance'),
                  cwd=str(cwd), command=command, pid=child.pid,
                  startTime=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  timeoutSeconds=timeout, childProcessGroupCleanup=False)
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
    if success and child.returncode:
        raise AssertionError((command, child.returncode, stdout[-1000:], stderr[-1000:]))
    return subprocess.CompletedProcess(command, child.returncode, stdout, stderr)


def compile_role(directory):
    run([args.javac, '--release', '17', '-encoding', 'UTF-8', '-Xlint:all', '-Werror', 'Main.java'], directory)


def execute(directory, success=True):
    return run([args.java, '-ea', '-Xmx256m', 'Main'], directory, success=success)


def case(moves, budget):
    # Enumerate actual Bessie gestures, not beaten-opponent labels or a DP table.
    answer = 0
    wins = {('H', 'S'), ('S', 'P'), ('P', 'H')}
    for choice in itertools.product('HPS', repeat=len(moves)):
        switches = sum(a != b for a, b in zip(choice, choice[1:]))
        if switches <= budget:
            answer = max(answer, sum((a, b) in wins for a, b in zip(choice, moves)))
    return f'{len(moves)} {budget}\n' + '\n'.join(moves) + '\n', answer


sample = case(list('PPHPS'), 1)
assert sample[1] == 4
tiny = [sample]
tiny += [case([gesture], budget) for gesture in 'HPS' for budget in [0, 1, 20]]
tiny += [case(list('HPSHPS'), 0), case(list('HPSHPS'), 20)]
rng = random.Random(1110202603)
for _ in range(20):
    tiny.append(case([rng.choice('HPS') for _ in range(rng.randint(1, 8))], rng.randint(0, 20)))
blocks = (['H']*4762 + ['P']*4762 + ['S']*4762)*7
blocks = blocks[:100000]
assert sum(a != b for a,b in zip(blocks, blocks[1:])) == 20
full = [
    ('100000 20\n' + 'H\n'*100000, 100000),
    ('100000 0\n' + '\n'.join(('HPS'*33334)[:100000])+'\n', 33334),
    ('100000 20\n' + '\n'.join(blocks)+'\n', 100000),
]
original = (PACK/'legacy/Main.java').read_bytes()
assert hashlib.sha256(original).hexdigest() == ORIGINAL_SHA256
reference = (PACK/'solution/Main.java').read_text()
learner = (PACK/'starter/Main.java').read_text()


def statements(text):
    # These sources have no comment delimiters inside strings. Retain every
    # non-comment token so instructional comment edits cannot hide a code edit.
    return re.sub(r'\s+', '', re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S))


assert statements(original.decode().replace('\r\n', '\n')) == statements(reference)
assert reference.count('CHANGED:') == 6
assert learner.count('// TODO ') == 4 and learner != reference
assert (PACK/'starter/hps.in').read_bytes() == (PACK/'solution/hps.in').read_bytes()
assert (PACK/'solution/hps.in').read_text().strip() == sample[0].strip()
assert (PACK/'solution/hps.out').read_text().strip() == '4'
tracked = [PACK/'legacy/Main.java', PACK/'solution/Main.java', PACK/'starter/Main.java',
           PACK/'solution/hps.in', PACK/'solution/hps.out', PACK/'starter/hps.in']
before = {str(path.relative_to(ROOT)): path.read_bytes() for path in tracked}
for role in ['starter', 'solution']:
    guide = (PACK/role/'README.md').read_text()
    assert all(text in guide for text in ['## Contract', '## Prediction', '## Tasks and walkthrough',
                                         '## State and reasoning', '## Build and run', '## Independent checks',
                                         'at most', 'JDK 17', 'PowerShell', 'hps.in', 'hps.out'])
counts = dict(compiledRoles=0, independentTinyCases=0, constructedFullLimitCases=0,
              unfinishedLearnerRuns=0, refusedLearnerInputs=0, tinyDriverProbes=0,
              fullParserProbes=0, invalidReturnedResults=0)


def injected(source, body):
    signature = 'static int maximumWins(Input input)'
    value, substitutions = re.subn(re.escape(signature)+r' \{.*?\n    \}',
                                  signature+' {\n        '+body+'\n    }', source, count=1, flags=re.S)
    assert substitutions == 1
    return value


with tempfile.TemporaryDirectory(prefix='gold-hps-acceptance-') as temporary:
    work = Path(temporary)
    dirs = {}
    for role in ['starter', 'solution']:
        directory = work/role
        directory.mkdir()
        (directory/'Main.java').write_bytes((PACK/role/'Main.java').read_bytes())
        compile_role(directory)
        dirs[role] = directory
        counts['compiledRoles'] += 1
    directory = dirs['solution']
    for data, expected in tiny+full:
        (directory/'hps.in').write_text(data)
        process = execute(directory)
        assert (directory/'hps.out').read_text() == str(expected)+'\n'
        assert process.stdout.strip() == str(expected)
    counts['independentTinyCases'] = len(tiny)
    counts['constructedFullLimitCases'] = len(full)
    directory = dirs['starter']
    input_file, output_file = directory/'hps.in', directory/'hps.out'
    previous = b'keep the earlier saved answer\n'
    for data, _ in [sample, full[0]]:
        input_file.write_text(data)
        for keep_answer in [True, False]:
            if keep_answer:
                output_file.write_bytes(previous)
            else:
                output_file.unlink(missing_ok=True)
            process = execute(directory, success=False)
            assert process.returncode == 2 and not process.stdout and 'Complete' in process.stderr
            assert (output_file.read_bytes() == previous) if keep_answer else not output_file.exists()
            counts['unfinishedLearnerRuns'] += 1
    invalid = ['0 0\n', '100001 0\n', '-1 0\n', '1 -1\nH\n', '1 21\nH\n',
               '1 0\nX\n', '1 0\nh\n', '1 0\nHP\n', '2 1\nH\n', '1\n',
               '1 0\nH\nextra\n', 'x 1\nH\n', '1 x\nH\n', '', None]
    for data in invalid:
        output_file.write_bytes(previous)
        if data is None:
            input_file.unlink()
        else:
            input_file.write_text(data)
        process = execute(directory, success=False)
        assert process.returncode == 2 and not process.stdout and 'Complete' not in process.stderr
        assert output_file.read_bytes() == previous
        counts['refusedLearnerInputs'] += 1
    # Tiny native copies probe supplied parsing/output only. No DP is completed
    # in the saved learner and this exponential model refuses larger inputs.
    probe = '''
        int n = input.opponent.length;
        if (n > 8) throw new UnsupportedOperationException("Tiny driver probe limit is 8");
        int choices = 1;
        for (int i = 0; i < n; i++) choices *= 3;
        int best = 0;
        for (int mask = 0; mask < choices; mask++) {
            int code = mask, changes = 0, wins = 0, previousGesture = -1;
            for (int i = 0; i < n; i++) {
                int gesture = code % 3; code /= 3;
                if (i > 0 && gesture != previousGesture) changes++;
                int opponent = input.opponent[i];
                if ((gesture == 0 && opponent == 2) || (gesture == 1 && opponent == 0)
                        || (gesture == 2 && opponent == 1)) wins++;
                previousGesture = gesture;
            }
            if (changes <= input.budget) best = Math.max(best, wins);
        }
        return best;'''
    (directory/'Main.java').write_text(injected(learner, probe))
    compile_role(directory)
    for index in [0,1,4,7,10,11]:
        data, expected = tiny[index]
        input_file.write_text(data)
        assert not execute(directory).stdout
        assert output_file.read_text() == str(expected)+'\n'
        counts['tinyDriverProbes'] += 1
    input_file.write_text(full[0][0])
    output_file.write_bytes(previous)
    assert execute(directory, success=False).returncode == 2 and output_file.read_bytes() == previous
    full_probe = 'if (input.opponent.length != 100000 || input.budget != 20 || input.opponent[99999] != 0) throw new AssertionError("Full parse"); return 100000;'
    (directory/'Main.java').write_text(injected(learner, full_probe))
    compile_role(directory)
    execute(directory)
    assert output_file.read_text() == '100000\n'
    counts['fullParserProbes'] += 1
    input_file.write_text(sample[0])
    for body in ['return -1;', 'return input.opponent.length+1;', 'return Integer.MAX_VALUE;']:
        (directory/'Main.java').write_text(injected(learner, body))
        compile_role(directory)
        output_file.write_bytes(previous)
        process = execute(directory, success=False)
        assert process.returncode == 2 and not process.stdout and output_file.read_bytes() == previous
        counts['invalidReturnedResults'] += 1

for path in tracked:
    assert path.read_bytes() == before[str(path.relative_to(ROOT))]
hashes = {role: hashlib.sha256((PACK/role/'Main.java').read_bytes().replace(b'\r\n', b'\n')).hexdigest()
          for role in ['starter', 'solution']}
print(json.dumps(dict(event='gold-hps-pack-accepted', passed=True, counts=counts,
                     originalRawReferenceSha256=ORIGINAL_SHA256, roleSourceSha256=hashes,
                     referenceExecutableStatementsUnchanged=True, commentCorrections=6,
                     independentActualGestureEnumeration=True, maximumRounds=100000, maximumSwitches=20,
                     previousAnswerPreserved=True, sourceAndSampleFilesUnchanged=True,
                     learnerAlgorithmUnfinished=True, tinyDriverProbeMaximumRounds=8,
                     historicalReferenceInvalidInputClaims=False, temporaryCopiesRemoved=True)), flush=True)
