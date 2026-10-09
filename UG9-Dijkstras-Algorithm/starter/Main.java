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
import java.util.StringTokenizer;

// Native Java lesson. Read dijkstra.in and write dijkstra.out in the working folder.
public class Main {
    static final int MAX_N = 2000;
    static final int MAX_M = 200000;
    static final long MAX_WEIGHT = 1000000000L;
    static final long INF = Long.MAX_VALUE;

    static final class Edge {
        final int to;
        final long weight;
        Edge(int to, long weight) { this.to = to; this.weight = weight; }
    }

    static final class Graph {
        final int n;
        final List<List<Edge>> edges = new ArrayList<>();
        Graph(int n) {
            this.n = n;
            for (int i = 0; i < n; i++) edges.add(new ArrayList<>());
        }
        void addEdge(int from, int to, long weight) {
            edges.get(from).add(new Edge(to, weight));
            edges.get(to).add(new Edge(from, weight));
        }
    }

    static final class State implements Comparable<State> {
        final int node;
        final long distance;
        State(int node, long distance) { this.node = node; this.distance = distance; }
        @Override public int compareTo(State other) {
            int order = Long.compare(distance, other.distance);
            return order != 0 ? order : Integer.compare(node, other.node);
        }
    }

    static final class Result {
        final long[] distance;
        final int[] previous;
        Result(long[] distance, int[] previous) {
            this.distance = distance;
            this.previous = previous;
        }
    }

    static Graph readGraph(Path input) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
            String line = reader.readLine();
            if (line == null) throw new IllegalArgumentException("Missing N M header");
            StringTokenizer tokens = new StringTokenizer(line);
            if (tokens.countTokens() != 2) throw new IllegalArgumentException("Header needs exactly N M");
            int n = Integer.parseInt(tokens.nextToken());
            int m = Integer.parseInt(tokens.nextToken());
            if (n < 1 || n > MAX_N || m < 0 || m > MAX_M) {
                throw new IllegalArgumentException("Practice bounds: 1 <= N <= 2000, 0 <= M <= 200000");
            }
            Graph graph = new Graph(n);
            for (int i = 0; i < m; i++) {
                line = reader.readLine();
                if (line == null) throw new IllegalArgumentException("Missing edge " + i);
                tokens = new StringTokenizer(line);
                if (tokens.countTokens() != 3) throw new IllegalArgumentException("Each edge needs P Q W");
                int from = Integer.parseInt(tokens.nextToken());
                int to = Integer.parseInt(tokens.nextToken());
                long weight = Long.parseLong(tokens.nextToken());
                if (from < 0 || from >= n || to < 0 || to >= n || weight < 0 || weight > MAX_WEIGHT) {
                    throw new IllegalArgumentException("Invalid endpoint or nonnegative weight bound");
                }
                graph.addEdge(from, to, weight);
            }
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) throw new IllegalArgumentException("Extra edge or token");
            }
            return graph;
        }
    }

    static Result shortestPaths(Graph graph) {
        // TODO 1: Fill distance with INF and previous with -1; set source 0 to distance 0.
        // TODO 2: Put source 0 into a PriorityQueue<State>; repeatedly remove its cheapest entry.
        // TODO 3: Discard stale entries, then relax each nonnegative edge using long arithmetic.
        // TODO 4: On a strict improvement, save its predecessor and enqueue the new distance.
        // Return new Result(distance, previous); unreachable nodes keep INF and predecessor -1.
        throw new UnsupportedOperationException("Complete the four Dijkstra tasks before producing an answer");
    }

    static List<String> outputLines(Result result) {
        int n = result.distance.length;
        if (result.previous.length != n || result.distance[0] != 0 || result.previous[0] != -1) {
            throw new IllegalArgumentException("Invalid source result");
        }
        List<String> lines = new ArrayList<>();
        for (int target = 1; target < n; target++) {
            if (result.distance[target] == INF) {
                lines.add("Unreachable: " + target);
                continue;
            }
            List<Integer> route = new ArrayList<>();
            boolean[] seen = new boolean[n];
            for (int current = target; current != -1; current = result.previous[current]) {
                if (current < 0 || current >= n || seen[current]) {
                    throw new IllegalArgumentException("Invalid predecessor chain");
                }
                seen[current] = true;
                route.add(current);
            }
            if (route.get(route.size() - 1) != 0) throw new IllegalArgumentException("Path misses source 0");
            Collections.reverse(route);
            StringBuilder line = new StringBuilder();
            for (int node : route) line.append(node).append(' ');
            line.append("Distance: ").append(result.distance[target]);
            lines.add(line.toString());
        }
        return lines;
    }

    public static void main(String[] args) {
        try {
            Graph graph = readGraph(Path.of("dijkstra.in"));
            Result result = shortestPaths(graph);
            List<String> lines = outputLines(result);
            // Validate the entire input and result before opening an answer file.
            Files.write(Path.of("dijkstra.out"), lines, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve dijkstra.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
