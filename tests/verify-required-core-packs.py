"""Verify three required Gold references, supplied helpers and unfinished roles.

Tiny oracles enumerate word sequences, point-graph paths and movement schedules.
Temporary driver probes return fixed values; they never solve learner algorithms.
"""

import argparse
import collections
import datetime
import hashlib
import json
import os
import random
import signal
import subprocess
import tempfile
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--javac", default="javac")
parser.add_argument("--java", default="java")
parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
args = parser.parse_args()
ROOT = args.root.resolve()
TASK = os.environ.get("CLASSES_FAMILY_TASK_ID", "required-gold-core")
folders = {
    "poetry": "UG28-Cow-Poetry",
    "lasers": "UG33-Lasers-and-Mirrors",
    "radio": "UG34-Radio-Contact",
}
cases = {key: [] for key in folders}
rng = random.Random(171134)
MOD = 1_000_000_007
ORIGINALS = {
    "poetry": "5e61ed95c860c09a58052937ac17a0cbd65dda947e53dfbc92e3f893cec74a87",
    "lasers": "7da14ed35bcee87ae51d88e37fca215f10b3545b768c1cb9c9c215f6feb6ab48",
    "radio": "deb82ffbcf6a55dba61367cb59fa113ed98da9226933a5dda05aa5e71c1d60a7",
}


def cancelled(sig, frame):
    raise KeyboardInterrupt("Required Gold core acceptance cancelled")


signal.signal(signal.SIGTERM, cancelled)


def run(command, directory, expected=0, timeout=30):
    child = subprocess.Popen(
        command,
        cwd=directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    record = {
        "event": "required-core-command",
        "parentTaskId": TASK,
        "cwd": str(directory),
        "command": command,
        "pid": child.pid,
        "startTime": datetime.datetime.now(datetime.timezone.utc).isoformat(),  # noqa: UP017 - Python 3.9 compatibility
        "timeoutSeconds": timeout,
        "childProcessGroupCleanup": False,
    }
    try:
        stdout, stderr = child.communicate(timeout=timeout)
    except BaseException:
        os.killpg(child.pid, signal.SIGTERM)
        try:
            child.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.communicate()
        record["childProcessGroupCleanup"] = True
        raise
    finally:
        record.update(
            endTime=datetime.datetime.now(datetime.timezone.utc).isoformat(),  # noqa: UP017 - Python 3.9 compatibility
            exitCode=child.returncode,
        )
        print(json.dumps(record), flush=True)
    assert child.returncode == expected, (
        command,
        child.returncode,
        stdout[-1500:],
        stderr[-1500:],
    )
    return subprocess.CompletedProcess(command, child.returncode, stdout, stderr)


def compile_role(directory, probe=False):
    run(
        [
            args.javac,
            "--release",
            "17",
            "-encoding",
            "UTF-8",
            "-Xlint:all",
            "-Werror",
            "Main.java",
            *(["Probe.java"] if probe else []),
        ],
        directory,
    )


def execute(directory, expected=0):
    return run([args.java, "-ea", "-Xmx256m", "Main"], directory, expected)


def normalized_bytes(path):
    return path.read_bytes().replace(b"\r\n", b"\n")


def java_expected_parse(key, text):
    tokens = text.split()
    if key == "poetry":
        n, m, k = map(int, tokens[:3])
        words = list(map(int, tokens[3 : 3 + 2 * n]))
        scheme = tokens[3 + 2 * n :]
        frequency = [scheme.count(chr(65 + i)) for i in range(26)]
        assert len(scheme) == m
        return f"{k};{words[::2]};{[c - 1 for c in words[1::2]]};{frequency}"
    if key == "lasers":
        n, lx, ly, bx, by = map(int, tokens[:5])
        coordinates = list(map(int, tokens[5:]))
        posts = [coordinates[i : i + 2] for i in range(0, len(coordinates), 2)]
        assert len(posts) == n
        return f"{lx};{ly};{bx};{by};{posts}"
    n, m, fx, fy, bx, by = map(int, tokens[:6])
    fd, bd = tokens[6:]
    assert len(fd) == n and len(bd) == m
    return f"{[list(p) for p in positions((fx, fy), fd)]};{[list(p) for p in positions((bx, by), bd)]}"


def poetry_expected(words, k, scheme):
    counts = collections.Counter()

    def visit(remaining, last_class):
        if remaining == 0:
            counts[last_class] += 1
            return
        for size, cls in words:
            if size <= remaining:
                visit(remaining - size, cls)

    visit(k, -1)
    result = 1
    mod = 1000000007
    for count in collections.Counter(scheme).values():
        result = result * sum(pow(n, count, mod) for n in counts.values()) % mod
    return str(result) + "\n"


def poetry_case(words, k, scheme, label):
    text = (
        f"{len(words)} {len(scheme)} {k}\n"
        + "".join(f"{s} {c}\n" for s, c in words)
        + "".join(s + "\n" for s in scheme)
    )
    cases["poetry"].append((label, text, poetry_expected(words, k, scheme)))


poetry_case([(3, 1), (4, 1), (3, 2)], 10, "ABA", "official-sample")
for i in range(18):
    n = rng.randint(1, 4)
    k = rng.randint(1, 6)
    words = [(rng.randint(1, k), rng.randint(1, n)) for _ in range(n)]
    scheme = "".join(rng.choice("ABC") for _ in range(rng.randint(1, 5)))
    poetry_case(words, k, scheme, f"exhaustive-word-sequences-{i}")
for mixed in [False, True]:
    n = 5000
    count = 100000
    k = 5000
    words = "".join(f"5000 {5000 if mixed and i % 2 else 1}\n" for i in range(n))
    text = f"{n} {count} {k}\n" + words + "A\n" * count
    expected = (
        2 * pow(2500, count, 1000000007) if mixed else pow(5000, count, 1000000007)
    ) % 1000000007
    cases["poetry"].append(
        (
            "full-limit-mixed-rhymes" if mixed else "full-limit-one-rhyme",
            text,
            str(expected) + "\n",
        )
    )


def laser_expected(start, end, posts):
    vertices = [start, *posts, end]
    dist = [None] * len(vertices)
    dist[0] = 0
    q = collections.deque([0])
    while q:
        i = q.popleft()
        for j in range(len(vertices)):
            if dist[j] is None and (
                vertices[i][0] == vertices[j][0] or vertices[i][1] == vertices[j][1]
            ):
                dist[j] = dist[i] + 1
                q.append(j)
    return str(-1 if dist[-1] is None else dist[-1] - 1) + "\n"


def laser_case(start, end, posts, label):
    text = f"{len(posts)} {start[0]} {start[1]} {end[0]} {end[1]}\n" + "".join(
        f"{x} {y}\n" for x, y in posts
    )
    cases["lasers"].append((label, text, laser_expected(start, end, posts)))


laser_case((0, 0), (7, 2), [(3, 2), (0, 2), (1, 6), (3, 0)], "official-sample")
laser_case((0, 0), (1, 1), [(2, 2)], "unreachable-minimum-posts")
laser_case((0, 0), (0, 1000000000), [(1, 1)], "zero-mirrors-coordinate-boundary")
laser_case(
    (0, 0),
    (1000000000, 1000000000),
    [(0, 1000000000)],
    "one-mirror-coordinate-boundary",
)
for i in range(20):
    pts = rng.sample([(x, y) for x in range(7) for y in range(7)], rng.randint(3, 10))
    laser_case(pts[0], pts[1], pts[2:], f"independent-point-graph-{i}")
posts = [((i + 1) // 2, i // 2) for i in range(1, 100001)]
text = "100000 0 0 50001 50000\n" + "".join(f"{x} {y}\n" for x, y in posts)
cases["lasers"].append(("full-limit-forced-turn-chain", text, "100000\n"))


def positions(start, directions):
    points = [start]
    delta = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
    for c in directions:
        x, y = points[-1]
        dx, dy = delta[c]
        points.append((x + dx, y + dy))
    assert all(0 <= x <= 1000 and 0 <= y <= 1000 for x, y in points)
    return points


def radio_expected(a, b, large=False):
    def cost(i, j):
        return (a[i][0] - b[j][0]) ** 2 + (a[i][1] - b[j][1]) ** 2

    n = len(a) - 1
    k = len(b) - 1
    if not large:

        def exhaustive(i, j):
            if i == n and j == k:
                return 0
            vals = []
            for di, dj in [(1, 0), (0, 1), (1, 1)]:
                if i + di <= n and j + dj <= k:
                    vals.append(cost(i + di, j + dj) + exhaustive(i + di, j + dj))
            return min(vals)

        return str(exhaustive(0, 0)) + "\n"
    previous = [0] * (k + 1)
    for j in range(1, k + 1):
        previous[j] = previous[j - 1] + cost(0, j)
    for i in range(1, n + 1):
        current = [previous[0] + cost(i, 0)] + [0] * k
        for j in range(1, k + 1):
            current[j] = min(current[j - 1], previous[j], previous[j - 1]) + cost(i, j)
        previous = current
    return str(previous[-1]) + "\n"


def radio_case(f, b, fd, bd, label, large=False):
    a = positions(f, fd)
    c = positions(b, bd)
    text = f"{len(fd)} {len(bd)}\n{f[0]} {f[1]}\n{b[0]} {b[1]}\n{fd}\n{bd}\n"
    cases["radio"].append((label, text, radio_expected(a, c, large)))


radio_case((3, 0), (5, 0), "NN", "NWWWWWN", "official-sample")
for i in range(18):
    fd = "".join(rng.choice("NE") for _ in range(rng.randint(1, 5)))
    bd = "".join(rng.choice("SW") for _ in range(rng.randint(1, 5)))
    radio_case((3, 3), (10, 10), fd, bd, f"exhaustive-movement-schedules-{i}")
radio_case(
    (0, 0), (1000, 1000), "E" * 1000, "W" * 1000, "full-valid-coordinate-boundary", True
)

BAD = {
    "poetry": [
        None,
        "x\n",
        "0 1 1\n",
        "5001 1 1\n",
        "1 0 1\n",
        "1 100001 1\n",
        "1 1 0\n",
        "1 1 5001\n",
        "1 1 1\n0 1\nA\n",
        "1 1 1\n2 1\nA\n",
        "1 1 1\n1 0\nA\n",
        "1 1 1\n1 2\nA\n",
        "1 1 1\n1 1\n",
        "1 1 1\n1 1\na\n",
        "1 1 1\n1 1\nAA\n",
        "1 1 1\n1 1\nA extra\n",
        "1 1 1\nx 1\nA\n",
    ],
    "lasers": [
        None,
        "x\n",
        "0 0 0 1 1\n",
        "100001 0 0 1 1\n",
        "1 -1 0 1 1\n2 2\n",
        "1 0 0 1000000001 1\n2 2\n",
        "1 0 0 1 1\n2\n",
        "1 0 0 1 1\n0 0\n",
        "1 0 0 1 1\n1 1\n",
        "2 0 0 1 1\n2 2\n2 2\n",
        "1 0 0 1 1\n-1 2\n",
        "1 0 0 1 1\n2 1000000001\n",
        "1 0 0 1 1\n2 2 extra\n",
        "1 0 0 1 1\nx 2\n",
    ],
    "radio": [
        None,
        "x\n",
        "0 1\n",
        "1001 1\n",
        "1 0\n",
        "1 1001\n",
        "1 1\n-1 0\n0 0\nN\nN\n",
        "1 1\n0 0\n1001 0\nN\nN\n",
        "1 1\n0 0\n0 0\nNN\nN\n",
        "1 1\n0 0\n0 0\nX\nN\n",
        "1 1\n0 0\n0 0\nN\n",
        "1 1\n1000 0\n0 0\nE\nN\n",
        "1 1\n0 0\n0 0\nN\nW\n",
        "1 1\n0 0\n0 0\nN\nN extra\n",
        "1 1\nx 0\n0 0\nN\nN\n",
    ],
}
PROBES = {
    "poetry": r"""import java.nio.file.Files; import java.nio.file.Path; import java.util.Arrays;
class Probe { public static void main(String[] args) throws Exception {
    Main.Input v = Main.readInput(Files.readString(Path.of("poetry.in")));
    assert v.wordSyllables.length == v.rhymeClasses.length;
    System.out.println(v.syllablesPerLine+";"+Arrays.toString(v.wordSyllables)+";"+Arrays.toString(v.rhymeClasses)+";"+Arrays.toString(v.schemeFrequency));
} }
""",
    "lasers": r"""import java.nio.file.Files; import java.nio.file.Path; import java.util.Arrays;
class Probe { public static void main(String[] args) throws Exception {
    Main.Input v = Main.readInput(Files.readString(Path.of("lasers.in")));
    assert Main.xLine(0) == -1 && Main.yLine(0) == 0;
    assert Main.xLine(1000000000) == -1000000001 && Main.yLine(1000000000) == 1000000000;
    assert Main.xLine(v.laserX) != Main.yLine(v.laserY);
    System.out.println(v.laserX+";"+v.laserY+";"+v.barnX+";"+v.barnY+";"+Arrays.deepToString(v.posts));
} }
""",
    "radio": r"""import java.nio.file.Files; import java.nio.file.Path; import java.util.Arrays;
class Probe { public static void main(String[] args) throws Exception {
    Main.Input v = Main.readInput(Files.readString(Path.of("radio.in")));
    Main.Input boundary = new Main.Input(new int[][]{{0,0},{1000,1000}},new int[][]{{1000,1000},{0,0}});
    assert Main.energy(boundary,0,0) == 2000000L && Main.energy(boundary,1,0) == 0L;
    for(int i=0;i<v.firstPath.length;i++) for(int j=0;j<v.secondPath.length;j++) {
        long dx=(long)v.firstPath[i][0]-v.secondPath[j][0],dy=(long)v.firstPath[i][1]-v.secondPath[j][1];
        assert Main.energy(v,i,j)==dx*dx+dy*dy;
    }
    System.out.println(Arrays.deepToString(v.firstPath)+";"+Arrays.deepToString(v.secondPath));
} }
""",
}
# Explicitly cover the unused-letter skip, unequal-letter freedom, impossible
# syllable total, simultaneous ticks and excluded initial energy from the guides.
poetry_case([(1, 1), (1, 2)], 1, "AB", "distinct-letters-may-share-class")
poetry_case([(1, 1), (1, 2)], 1, "AA", "repeated-letter-same-class")
poetry_case([(1, 1), (1, 1)], 1, "AA", "same-class-distinct-word-identities")
poetry_case([(2, 1), (2, 2)], 3, "A", "unattainable-total")
poetry_case([(1, 1)], 1, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "all-scheme-letters")
radio_case((0, 0), (0, 0), "E", "E", "identical-paths-zero")
radio_case((0, 0), (2, 0), "E", "W", "simultaneous-arrival-zero")
radio_case((0, 0), (0, 2), "E", "E", "exclude-initial-energy")


FIXTURE_ARCHIVES = {
    "UG28-Cow-Poetry/legacy/solution/poetry.in": "f9a0184fa8e792fcfcd1be744bc3f22a6aa8ae959d843e7605b3919be73891c9",
    "UG28-Cow-Poetry/legacy/solution/poetry.out": "2418ab6dd0242696e01623b54cff8f2837af6a18190d876479dc58e16ec0ba46",
    "UG33-Lasers-and-Mirrors/legacy/solution/lasers.out": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
}
for relative, expected in FIXTURE_ARCHIVES.items():
    assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected

GUIDE_ORIGINALS = {
    "UG28-Cow-Poetry/legacy/README.md": "e2d3caea1eee4ec15eec7b163066255104eb48dfab4c408a86bdd37fc00bea2f",
    "UG28-Cow-Poetry/legacy/starter/README.md": "d330f5572d8288929dca394998e878b5d75f02f383bbabddce218773fe30ea7c",
    "UG33-Lasers-and-Mirrors/legacy/README.md": "9aeba181beb0958fec2ce4d93339edeba9e948cec65bc23970491f50cd124fe9",
    "UG33-Lasers-and-Mirrors/legacy/starter/README.md": "8dc10c7dd50bcdbd18a93c5feeb913fdf4c514e861da148f3a97ea25e1c6eeb9",
    "UG34-Radio-Contact/legacy/README.md": "9cd66c9d3437379adbe9cb661fee73e9a41af6a5b4a21f71e61df59f4c4b4a50",
    "UG34-Radio-Contact/legacy/starter/README.md": "99bf5b591639c9395382ff4919b99578502d3a8f469ebc766793b9d702e8b306",
}
for relative, expected in GUIDE_ORIGINALS.items():
    assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected

tracked = {
    p: p.read_bytes()
    for folder in folders.values()
    for p in (ROOT / folder).rglob("*")
    if p.is_file() and p.suffix in [".java", ".md", ".in", ".out"]
}
for key, folder in folders.items():
    pack = ROOT / folder
    reference = normalized_bytes(pack / "solution/Main.java")
    starter = normalized_bytes(pack / "starter/Main.java")
    assert starter != reference and starter.count(b"// TASK ") == (
        4 if key == "lasers" else 3
    )
    assert starter.count(b"throw new UnsupportedOperationException(") == 1
    assert (pack / f"starter/{key}.in").read_bytes() == (
        pack / f"solution/{key}.in"
    ).read_bytes()
    assert (pack / f"solution/{key}.out").read_text().strip() == cases[key][0][
        2
    ].strip()
    assert (pack / f"solution/{key}.in").read_text().strip() == cases[key][0][1].strip()
    for role in ["starter", "solution"]:
        guide = (pack / role / "README.md").read_text()
        assert all(
            label in guide
            for label in [
                "## Contract",
                "## Prediction",
                "## State and reasoning",
                "## Tasks and walkthrough",
                "## Independent checks",
                "## Build and run",
                "JDK 17",
                "PowerShell",
                key + ".in",
                key + ".out",
            ]
        )
    if key == "lasers":
        original = (pack / "legacy/solution/Main.java").read_bytes()
        assert hashlib.sha256(original).hexdigest() == ORIGINALS[key]
        changed = original.replace(b"int answer = 0;", b"int answer = -1;").replace(
            b"// read input - note that since x and y are both positive in this problem, we will use a negative number denote a y",
            b"// Encode nonnegative x as -x-1 and keep y nonnegative so their keys are disjoint.",
        )
        assert changed == reference
    else:
        assert hashlib.sha256(reference).hexdigest() == ORIGINALS[key]

counts = {
    "compiledRoles": 0,
    "zipRoles": 0,
    "independentReferenceCases": 0,
    "fullLimitReferenceCases": 0,
    "unfinishedLearnerRuns": 0,
    "refusedLearnerInputs": 0,
    "parserAndHelperProbes": 0,
    "successfulFixedDriverProbes": 0,
    "refusedResultDriverProbes": 0,
    "originalLaserCounterexamples": 0,
}
with tempfile.TemporaryDirectory(prefix="gold-required-core-") as temporary:
    work = Path(temporary)
    for key, folder in folders.items():
        role_dirs = {}
        for role in ["starter", "solution"]:
            directory = work / folder / role
            directory.mkdir(parents=True)
            archive = directory / "role.zip"
            source = ROOT / folder / role
            with zipfile.ZipFile(archive, "w") as z:
                for p in sorted(source.iterdir()):
                    if p.is_file() and p.suffix in [".java", ".md", ".in", ".out"]:
                        z.write(p, p.name)
            with zipfile.ZipFile(archive) as z:
                assert all(
                    "/" not in name and name not in [".", ".."] for name in z.namelist()
                )
                z.extractall(directory)
            for p in source.iterdir():
                if p.is_file() and p.suffix in [".java", ".md", ".in", ".out"]:
                    assert p.read_bytes() == (directory / p.name).read_bytes()
            counts["zipRoles"] += 1
            compile_role(directory)
            counts["compiledRoles"] += 1
            role_dirs[role] = directory
        directory = role_dirs["solution"]
        for label, text, expected in cases[key]:
            (directory / (key + ".in")).write_text(text)
            (directory / (key + ".out")).unlink(missing_ok=True)
            process = execute(directory)
            assert not process.stdout and not process.stderr
            assert (directory / (key + ".out")).read_text() == expected, (
                key,
                label,
                expected,
            )
            counts["independentReferenceCases"] += 1
            counts["fullLimitReferenceCases"] += int(label.startswith("full"))
        if key == "lasers":
            original = work / "original-laser"
            original.mkdir()
            (original / "Main.java").write_bytes(
                (ROOT / folder / "legacy/solution/Main.java").read_bytes()
            )
            compile_role(original)
            label, text, expected = next(
                case for case in cases[key] if case[0] == "unreachable-minimum-posts"
            )
            (original / "lasers.in").write_text(text)
            execute(original)
            assert expected == "-1\n" and (original / "lasers.out").read_text() == "0\n"
            counts["originalLaserCounterexamples"] += 1
        directory = role_dirs["starter"]
        input_file, output_file = directory / (key + ".in"), directory / (key + ".out")
        saved = b"preserve the earlier learner answer\n"
        full = [case for case in cases[key] if case[0].startswith("full")]
        for label, text, _ in [cases[key][0], full[0]]:
            input_file.write_text(text)
            for existing in [False, True]:
                if existing:
                    output_file.write_bytes(saved)
                else:
                    output_file.unlink(missing_ok=True)
                process = execute(directory, 2)
                assert not process.stdout and "unfinished" in process.stderr
                assert (
                    output_file.read_bytes() == saved
                    if existing
                    else not output_file.exists()
                )
                counts["unfinishedLearnerRuns"] += 1
        for data in BAD[key]:
            output_file.write_bytes(saved)
            if data is None:
                input_file.unlink(missing_ok=True)
            else:
                input_file.write_text(data)
            process = execute(directory, 2)
            assert (
                not process.stdout
                and process.stderr
                and "unfinished" not in process.stderr
            )
            assert output_file.read_bytes() == saved
            counts["refusedLearnerInputs"] += 1
        (directory / "Probe.java").write_text(PROBES[key])
        compile_role(directory, True)
        for _, text, _ in [
            cases[key][0],
            [case for case in cases[key] if not case[0].startswith("full")][-1],
            *full,
        ]:
            input_file.write_text(text)
            process = run([args.java, "-ea", "-Xmx256m", "Probe"], directory)
            assert (
                process.stdout.strip() == java_expected_parse(key, text)
                and not process.stderr
            )
            counts["parserAndHelperProbes"] += 1
        # These bounded file-driver probes replace only the unfinished throw with
        # a fixed literal. They test writing and result guards, never a solver.
        source = (directory / "Main.java").read_text()
        throw_lines = [
            line
            for line in source.splitlines()
            if "throw new UnsupportedOperationException(" in line
        ]
        assert len(throw_lines) == 1
        values = (
            [960, 0, MOD - 1, -1, MOD]
            if key == "poetry"
            else ([1, 0, -1, -2, 5] if key == "lasers" else [28, 0, -1])
        )
        for value in values:
            (directory / "Main.java").write_text(
                source.replace(
                    throw_lines[0],
                    "        return "
                    + str(value)
                    + ("L" if key != "lasers" else "")
                    + ";",
                )
            )
            compile_role(directory)
            input_file.write_text(cases[key][0][1])
            output_file.write_bytes(saved)
            valid = (
                0 <= value < MOD
                if key == "poetry"
                else -1 <= value <= 4
                if key == "lasers"
                else value >= 0
            )
            process = execute(directory, 0 if valid else 2)
            assert not process.stdout
            if valid:
                assert (
                    not process.stderr and output_file.read_text() == str(value) + "\n"
                )
                counts["successfulFixedDriverProbes"] += 1
            else:
                assert process.stderr and output_file.read_bytes() == saved
                counts["refusedResultDriverProbes"] += 1
for path, before in tracked.items():
    assert path.read_bytes() == before, str(path)
assert counts["zipRoles"] == counts["compiledRoles"] == 6
assert (
    counts["independentReferenceCases"] == 74 and counts["fullLimitReferenceCases"] == 4
)
assert counts["unfinishedLearnerRuns"] == 12 and counts["refusedLearnerInputs"] == 46
assert (
    counts["successfulFixedDriverProbes"] == 8
    and counts["refusedResultDriverProbes"] == 5
)
assert counts["originalLaserCounterexamples"] == 1
assert counts["parserAndHelperProbes"] == 10
print(
    json.dumps(
        dict(
            event="verified-required-gold-core",
            packs=3,
            nativeRuntime=args.java,
            release=17,
            heapMiB=256,
            sourceUnchanged=True,
            independentModels=[
                "Enumerated ordered word sequences",
                "Point graph shortest segments",
                "Enumerated joint movement schedules",
                "Full-limit known constructions and rolling-row schedule oracle",
            ],
            laserExecutableEdits=1,
            **counts,
        )
    ),
    flush=True,
)
