// Learner exercise: traffic on a selected shortest-path tree.
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

class Main {
    static final int MAX_WEIGHT = 25_000;
    static final long INF = Long.MAX_VALUE / 4;

    static final class Edge {
        final int to;
        final int weight;

        Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }
    }

    static final class Problem {
        final List<List<Edge>> roads;
        final int[] cows;
        final int shortcutTime;

        Problem(List<List<Edge>> roads, int[] cows, int shortcutTime) {
            this.roads = roads;
            this.cows = cows;
            this.shortcutTime = shortcutTime;
        }
    }

    static final class ShortestRoutes {
        final long[] distance;
        final int[] parent;

        ShortestRoutes(long[] distance, int[] parent) {
            this.distance = distance;
            this.parent = parent;
        }
    }

    static final class QueueEntry {
        final long distance;
        final int field;

        QueueEntry(long distance, int field) {
            this.distance = distance;
            this.field = field;
        }
    }

    public static void main(String[] args) {
        try {
            if (args.length != 0) {
                throw new IllegalArgumentException("No command-line arguments: use shortcut.in");
            }
            Problem problem = readProblem(Path.of("shortcut.in"));
            long answer = solve(problem);
            long totalCows = 0;
            for (int count : problem.cows) totalCows += count;
            long bound = totalCows * (problem.cows.length - 1L) * MAX_WEIGHT;
            if (answer < 0 || answer > bound) {
                throw new IllegalArgumentException("Return total savings in 0.." + bound);
            }
            Files.writeString(Path.of("shortcut.out"), answer + "\n", StandardCharsets.UTF_8);
        } catch (IOException | RuntimeException failure) {
            System.err.println("Cannot solve Shortcut: " + failure.getMessage());
            System.exit(2);
        }
    }

    static long solve(Problem problem) {
        // TODO 1: Call shortestRoutes(problem.roads) and turn its parent array
        // into child lists. Explain the tie rule and why distances decrease
        // toward the barn, so these selected routes form a rooted tree.

        // TODO 2: Accumulate each field's own cows plus its children's traffic
        // in long totals. Use an iterative postorder to support a deep chain.

        // TODO 3: Evaluate a shortcut only for cows whose usual route visits
        // its field. Compare nonnegative savings using long arithmetic.

        // TODO 4: Return the greatest total saving; justify zero-benefit and
        // tied-route cases without sending cows onto different usual routes.
        throw new UnsupportedOperationException("Complete the four Shortcut traffic tasks");
    }

    // Supplied weighted-graph helper; the learner work is tree traffic.
    static ShortestRoutes shortestRoutes(List<List<Edge>> roads) {
        int n = roads.size();
        long[] distance = new long[n];
        int[] parent = new int[n];
        Arrays.fill(distance, INF);
        Arrays.fill(parent, -1);
        distance[0] = 0;
        PriorityQueue<QueueEntry> queue = new PriorityQueue<>(
                Comparator.comparingLong((QueueEntry item) -> item.distance)
                        .thenComparingInt(item -> item.field));
        queue.add(new QueueEntry(0, 0));
        while (!queue.isEmpty()) {
            QueueEntry current = queue.remove();
            if (current.distance != distance[current.field]) continue;
            for (Edge road : roads.get(current.field)) {
                long candidate = current.distance + road.weight;
                if (candidate < distance[road.to]) {
                    distance[road.to] = candidate;
                    parent[road.to] = current.field;
                    queue.add(new QueueEntry(candidate, road.to));
                } else if (candidate == distance[road.to]
                        && current.field < parent[road.to]) {
                    // Routes are compared from this field toward the barn.
                    parent[road.to] = current.field;
                }
            }
        }
        return new ShortestRoutes(distance, parent);
    }

    static Problem readProblem(Path input) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
            int[] header = readRecord(reader, 3, "header");
            int n = header[0];
            int m = header[1];
            int t = header[2];
            if (n < 1 || n > 10_000 || m < n - 1 || m > 50_000
                    || t < 1 || t > 10_000) {
                throw new IllegalArgumentException("Use 1..10000 fields, N-1..50000 roads and T in 1..10000");
            }
            int[] cows = readRecord(reader, n, "cow counts");
            for (int count : cows) {
                if (count < 0 || count > 10_000) {
                    throw new IllegalArgumentException("Cow counts must be in 0..10000");
                }
            }
            List<List<Edge>> roads = new ArrayList<>(n);
            for (int field = 0; field < n; field++) roads.add(new ArrayList<>());
            for (int index = 0; index < m; index++) {
                int[] row = readRecord(reader, 3, "road " + (index + 1));
                int a = row[0] - 1;
                int b = row[1] - 1;
                int weight = row[2];
                if (a < 0 || a >= n || b < 0 || b >= n
                        || weight < 1 || weight > MAX_WEIGHT) {
                    throw new IllegalArgumentException("Road endpoints or travel time outside the contract");
                }
                // The statement does not forbid parallel roads or positive loops.
                roads.get(a).add(new Edge(b, weight));
                roads.get(b).add(new Edge(a, weight));
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
                int field = queue.remove();
                for (Edge road : roads.get(field)) {
                    if (!reached[road.to]) {
                        reached[road.to] = true;
                        queue.add(road.to);
                    }
                }
            }
            for (boolean connected : reached) {
                if (!connected) throw new IllegalArgumentException("Every field must reach the barn");
            }
            return new Problem(roads, cows, t);
        }
    }

    static int[] readRecord(BufferedReader reader, int count, String name) throws IOException {
        String line = reader.readLine();
        if (line == null) throw new IllegalArgumentException("Missing " + name + " record");
        String[] words = line.trim().split("\\s+");
        if (words.length != count) throw new IllegalArgumentException("Wrong " + name + " record width");
        int[] result = new int[count];
        for (int index = 0; index < count; index++) result[index] = Integer.parseInt(words[index]);
        return result;
    }
}
