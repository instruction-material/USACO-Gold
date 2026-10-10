// ADDED: Optional matrix-representation learner pack. Complete only the four TODOs.
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.PriorityQueue;

class Main {
    static final long INF = Long.MAX_VALUE;
    static final int MAX_N = 2000;
    static final int MAX_M = 200000;

    static class Graph {
        final int n;
        final int[][] weight;
        Graph(int n, int[][] weight) { this.n = n; this.weight = weight; }
    }

    static class State implements Comparable<State> {
        final long distance;
        final int node;
        State(long distance, int node) { this.distance = distance; this.node = node; }
        public int compareTo(State other) {
            int order = Long.compare(distance, other.distance);
            return order != 0 ? order : Integer.compare(node, other.node);
        }
    }

    static class Result {
        final long[] distance;
        final int[] previous;
        Result(long[] distance, int[] previous) {
            this.distance = distance;
            this.previous = previous;
        }
    }

    static String[] tokens(String line, int count) {
        if (line == null || line.isBlank()) throw new IllegalArgumentException("Missing record");
        String[] words = line.trim().split("\\s+");
        if (words.length != count) throw new IllegalArgumentException("Wrong record length");
        return words;
    }

    static Graph readGraph(Path input) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
            String[] header = tokens(reader.readLine(), 2);
            int n = Integer.parseInt(header[0]);
            int m = Integer.parseInt(header[1]);
            if (n < 1 || n > MAX_N || m < 0 || m > MAX_M) {
                throw new IllegalArgumentException("Use 1 <= N <= 2000 and 0 <= M <= 200000");
            }
            int[][] weight = new int[n][n];
            for (int[] row : weight) Arrays.fill(row, -1);
            for (int i = 0; i < m; i++) {
                String[] edge = tokens(reader.readLine(), 3);
                int a = Integer.parseInt(edge[0]);
                int b = Integer.parseInt(edge[1]);
                int w = Integer.parseInt(edge[2]);
                if (a < 0 || a >= n || b < 0 || b >= n || w < 0) {
                    throw new IllegalArgumentException("Use in-range vertices and nonnegative int weights");
                }
                if (weight[a][b] == -1 || w < weight[a][b]) {
                    weight[a][b] = w;
                    weight[b][a] = w;
                }
            }
            for (String extra; (extra = reader.readLine()) != null;) {
                if (!extra.isBlank()) throw new IllegalArgumentException("Unexpected extra record");
            }
            return new Graph(n, weight);
        }
    }

    static Result shortestPaths(Graph graph) {
        // TODO 1: Initialize long distances to INF, predecessors to -1 and source 0 to 0.
        // TODO 2: Create a PriorityQueue<State> and add the source state.
        // TODO 3: Poll the smallest state and skip stale entries before scanning its matrix row.
        // TODO 4: Relax existing edges only on strict improvement, update predecessors and enqueue.
        // Zero-weight edges exist; -1 alone means absent. Return both result arrays.
        throw new UnsupportedOperationException("Complete the four matrix Dijkstra tasks");
    }

    static List<String> outputLines(Graph graph, Result result) {
        if (result == null || result.distance == null || result.previous == null
                || result.distance.length != graph.n || result.previous.length != graph.n
                || result.distance[0] != 0 || result.previous[0] != -1) {
            throw new IllegalArgumentException("Invalid source result");
        }
        List<String> lines = new ArrayList<>();
        for (int target = 1; target < graph.n; target++) {
            long distance = result.distance[target];
            if (distance == INF) {
                if (result.previous[target] != -1) throw new IllegalArgumentException("Unreachable predecessor");
                lines.add("Unreachable: " + target);
                continue;
            }
            if (distance < 0 || distance > (long) (graph.n - 1) * Integer.MAX_VALUE) {
                throw new IllegalArgumentException("Invalid finite distance");
            }
            List<Integer> route = new ArrayList<>();
            boolean[] seen = new boolean[graph.n];
            for (int node = target; node != -1; node = result.previous[node]) {
                if (node < 0 || node >= graph.n || seen[node]) {
                    throw new IllegalArgumentException("Invalid predecessor chain");
                }
                seen[node] = true;
                route.add(node);
            }
            if (route.get(route.size() - 1) != 0) throw new IllegalArgumentException("Path misses source 0");
            Collections.reverse(route);
            long sum = 0;
            for (int i = 1; i < route.size(); i++) {
                int w = graph.weight[route.get(i - 1)][route.get(i)];
                if (w == -1) throw new IllegalArgumentException("Path uses an absent edge");
                sum += w;
            }
            if (sum != distance) throw new IllegalArgumentException("Path cost differs from distance");
            StringBuilder line = new StringBuilder();
            for (int node : route) line.append(node).append(' ');
            line.append("Distance: ").append(distance);
            lines.add(line.toString());
        }
        return lines;
    }

    public static void main(String[] args) {
        try {
            if (args.length != 0) throw new IllegalArgumentException("No command-line arguments expected");
            Graph graph = readGraph(Path.of("dijkstra.in"));
            List<String> lines = outputLines(graph, shortestPaths(graph));
            // Validate input and every output path before opening the answer file.
            Files.write(Path.of("dijkstra.out"), lines, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve dijkstra.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
