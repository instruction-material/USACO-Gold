// Learner exercise: shortest-path sensitivity and restoration of trial state.
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

class Main {
    static final int MAX_WEIGHT = 1_000_000;
    static final long INF = Long.MAX_VALUE / 4;

    static final class Problem {
        final int[][] lengths;
        final int[][] roads;

        Problem(int[][] lengths, int[][] roads) {
            this.lengths = lengths;
            this.roads = roads;
        }
    }

    static final class ShortestPath {
        final long distance;
        final int[] parent;

        ShortestPath(long distance, int[] parent) {
            this.distance = distance;
            this.parent = parent;
        }
    }

    public static void main(String[] args) {
        try {
            if (args.length != 0) {
                throw new IllegalArgumentException("No command-line arguments: use rblock.in");
            }
            Problem problem = readProblem(Path.of("rblock.in"));
            long answer = solve(problem);
            long bound = (long) (problem.lengths.length - 1) * MAX_WEIGHT;
            if (answer < 0 || answer > bound) {
                throw new IllegalArgumentException("Return an increase in 0.." + bound);
            }
            Files.writeString(Path.of("rblock.out"), answer + "\n", StandardCharsets.UTF_8);
        } catch (IOException | RuntimeException failure) {
            System.err.println("Cannot solve Roadblock: " + failure.getMessage());
            System.exit(2);
        }
    }

    static long solve(Problem problem) {
        // TODO 1: Obtain the baseline with shortestPath(problem.lengths).
        // Preserve its chosen predecessor path before any changed-weight run.

        // TODO 2: Restrict trials to that path. Explain why a road outside it
        // cannot increase the optimum, including graphs with tied best routes.

        // TODO 3: Double one road in both matrix directions, run shortestPath
        // again, and maximize the increase relative to the original baseline.

        // TODO 4: Restore the old weight before another trial, also when a
        // trial fails. Explain how try/finally protects experiment state.
        throw new UnsupportedOperationException("Complete the four Roadblock sensitivity tasks");
    }

    // Supplied from the core weighted-graph lesson. The exercise is sensitivity.
    static ShortestPath shortestPath(int[][] lengths) {
        int n = lengths.length;
        long[] distance = new long[n];
        int[] parent = new int[n];
        boolean[] settled = new boolean[n];
        Arrays.fill(distance, INF);
        Arrays.fill(parent, -1);
        distance[0] = 0;
        for (int count = 0; count < n; count++) {
            int node = -1;
            for (int candidate = 0; candidate < n; candidate++) {
                if (!settled[candidate] && distance[candidate] < INF
                        && (node == -1 || distance[candidate] < distance[node])) {
                    node = candidate;
                }
            }
            if (node == -1) break;
            settled[node] = true;
            for (int next = 0; next < n; next++) {
                if (!settled[next] && lengths[node][next] > 0) {
                    long candidate = distance[node] + lengths[node][next];
                    if (candidate < distance[next]) {
                        distance[next] = candidate;
                        parent[next] = node;
                    }
                }
            }
        }
        return new ShortestPath(distance[n - 1], parent);
    }

    static Problem readProblem(Path input) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
            int[] header = readRecord(reader, 2, "header");
            int n = header[0];
            int m = header[1];
            if (n < 1 || n > 250 || m < 1 || m > 25_000) {
                throw new IllegalArgumentException("Use 1..250 fields and 1..25000 roads");
            }
            int[][] lengths = new int[n][n];
            for (int[] row : lengths) Arrays.fill(row, -1);
            int[][] roads = new int[m][3];
            Set<Long> pairs = new HashSet<>();
            for (int index = 0; index < m; index++) {
                int[] record = readRecord(reader, 3, "road " + (index + 1));
                int a = record[0] - 1;
                int b = record[1] - 1;
                int weight = record[2];
                if (a < 0 || a >= n || b < 0 || b >= n || weight < 1 || weight > MAX_WEIGHT) {
                    throw new IllegalArgumentException("Road endpoints or length outside the contract");
                }
                long pair = (long) Math.min(a, b) * 250 + Math.max(a, b);
                if (!pairs.add(pair)) {
                    throw new IllegalArgumentException("Duplicate undirected road");
                }
                roads[index] = new int[] {a, b, weight};
                lengths[a][b] = weight;
                lengths[b][a] = weight;
            }
            String extra;
            while ((extra = reader.readLine()) != null) {
                if (!extra.trim().isEmpty()) {
                    throw new IllegalArgumentException("Unexpected extra record");
                }
            }
            boolean[] reached = new boolean[n];
            ArrayDeque<Integer> queue = new ArrayDeque<>();
            reached[0] = true;
            queue.add(0);
            while (!queue.isEmpty()) {
                int node = queue.remove();
                for (int next = 0; next < n; next++) {
                    if (lengths[node][next] > 0 && !reached[next]) {
                        reached[next] = true;
                        queue.add(next);
                    }
                }
            }
            for (boolean connected : reached) {
                if (!connected) throw new IllegalArgumentException("Every field must be reachable");
            }
            return new Problem(lengths, roads);
        }
    }

    static int[] readRecord(BufferedReader reader, int count, String name) throws IOException {
        String line = reader.readLine();
        if (line == null) throw new IllegalArgumentException("Missing " + name + " record");
        String[] words = line.trim().split("\\s+");
        if (words.length != count) throw new IllegalArgumentException("Wrong " + name + " record width");
        int[] values = new int[count];
        for (int index = 0; index < count; index++) values[index] = Integer.parseInt(words[index]);
        return values;
    }
}
