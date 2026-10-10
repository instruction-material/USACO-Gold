import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.StringTokenizer;

// Native Java: keep prim.in and prim.out in this role's working folder.
public class Main {
    static final int MAX_N = 2000;
    static final int MAX_M = 200000;
    static final int MAX_WEIGHT = 1000000000;
    static final long INF = Long.MAX_VALUE;

    static final class Graph {
        final int n;
        final int[][] edge;
        Graph(int n) {
            this.n = n;
            edge = new int[n][n];
            for (int[] row : edge) Arrays.fill(row, -1);
        }
        void addEdge(int a, int b, int weight) {
            if (edge[a][b] == -1 || weight < edge[a][b]) {
                edge[a][b] = weight;
                edge[b][a] = weight;
            }
        }
    }

    static final class Result {
        final int[] previous;
        final long total;
        Result(int[] previous, long total) {
            this.previous = previous;
            this.total = total;
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
                int a = Integer.parseInt(tokens.nextToken());
                int b = Integer.parseInt(tokens.nextToken());
                int weight = Integer.parseInt(tokens.nextToken());
                if (a < 0 || a >= n || b < 0 || b >= n || weight < 0 || weight > MAX_WEIGHT) {
                    throw new IllegalArgumentException("Invalid endpoint or nonnegative weight bound");
                }
                graph.addEdge(a, b, weight);
            }
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) throw new IllegalArgumentException("Extra edge or token");
            }
            return graph;
        }
    }

    static Result minimumTree(Graph graph) {
        // TODO 1: Initialize best to INF, previous to -1 and visited to false; root 0 starts at 0.
        // TODO 2: Select the cheapest unvisited vertex, rejecting an infinite candidate.
        // TODO 3: Mark it visited and add its connecting cost to a long total.
        // TODO 4: Relax unvisited neighbors using the edge weight, not a cumulative path cost.
        // Return new Result(previous, total) after every vertex joins the tree.
        throw new UnsupportedOperationException("Complete the four Prim tasks before producing an answer");
    }

    static List<String> outputLines(Graph graph, Result result) {
        if (result.previous.length != graph.n || result.previous[0] != -1) {
            throw new IllegalArgumentException("Invalid root or predecessor count");
        }
        List<String> lines = new ArrayList<>();
        long sum = 0;
        for (int v = 1; v < graph.n; v++) {
            int parent = result.previous[v];
            if (parent < 0 || parent >= graph.n || parent == v || graph.edge[v][parent] == -1) {
                throw new IllegalArgumentException("Missing tree edge for vertex " + v);
            }
            boolean[] seen = new boolean[graph.n];
            for (int current = v; current != 0; current = result.previous[current]) {
                if (current < 0 || current >= graph.n || seen[current]) {
                    throw new IllegalArgumentException("Predecessors do not form a tree rooted at 0");
                }
                seen[current] = true;
            }
            sum += graph.edge[v][parent];
            lines.add(v + " " + parent);
        }
        if (sum != result.total) throw new IllegalArgumentException("Tree total differs from its edges");
        lines.add("Total Distance: " + sum);
        return lines;
    }

    public static void main(String[] args) {
        try {
            Graph graph = readGraph(Path.of("prim.in"));
            Result result = minimumTree(graph);
            List<String> lines = outputLines(graph, result);
            // Parse and validate the whole tree before opening an answer file.
            Files.write(Path.of("prim.out"), lines, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve prim.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
