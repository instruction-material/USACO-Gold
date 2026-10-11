import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.StringTokenizer;

public class Main {
    static final int MAX_N = 200000, MAX_M = 200000, MAX_WEIGHT = 1000000000;
    static final class Edge implements Comparable<Edge> {
        final int p, q, weight;
        Edge(int p, int q, int weight) { this.p = p; this.q = q; this.weight = weight; }
        public int compareTo(Edge other) { return Integer.compare(weight, other.weight); }
    }
    static final class Graph {
        final int n;
        final List<Edge> edges;
        Graph(int n, List<Edge> edges) { this.n = n; this.edges = edges; }
    }
    static final class DisjointSets {
        final int[] parent, size;
        int count;
        DisjointSets(int n) {
            parent = new int[n]; size = new int[n]; count = n;
            for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        }
        int root(int p) {
            // TODO 1: Follow parents to the representative. Path compression is an optional extension.
            throw new UnsupportedOperationException("Complete find");
        }
        boolean connected(int p, int q) { return root(p) == root(q); }
        void connect(int p, int q) {
            // TODO 2: Join different roots by size, update the winning size and decrement count once.
            throw new UnsupportedOperationException("Complete union by size");
        }
    }
    static Graph readGraph(Path input) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
            String line = reader.readLine();
            if (line == null) throw new IllegalArgumentException("Missing N M header");
            StringTokenizer tokens = new StringTokenizer(line);
            if (tokens.countTokens() != 2) throw new IllegalArgumentException("Header needs exactly N M");
            int n = Integer.parseInt(tokens.nextToken()), m = Integer.parseInt(tokens.nextToken());
            if (n < 1 || n > MAX_N || m < 0 || m > MAX_M) throw new IllegalArgumentException("Graph size exceeds practice bounds");
            List<Edge> edges = new ArrayList<>();
            for (int i = 0; i < m; i++) {
                line = reader.readLine();
                if (line == null) throw new IllegalArgumentException("Missing edge " + i);
                tokens = new StringTokenizer(line);
                if (tokens.countTokens() != 3) throw new IllegalArgumentException("Each edge needs P Q W");
                int a = Integer.parseInt(tokens.nextToken()), b = Integer.parseInt(tokens.nextToken());
                int w = Integer.parseInt(tokens.nextToken());
                if (a < 0 || a >= n || b < 0 || b >= n || w < 0 || w > MAX_WEIGHT) throw new IllegalArgumentException("Invalid endpoint or weight");
                edges.add(new Edge(a, b, w));
            }
            while ((line = reader.readLine()) != null) if (!line.trim().isEmpty()) throw new IllegalArgumentException("Extra edge or token");
            return new Graph(n, edges);
        }
    }
    static List<Edge> minimumTree(Graph graph) {
        // TODO 3: Copy and sort edges by weight; initialize a DSU with one component per vertex.
        // TODO 4: Accept exactly the edges joining different components; return N-1 edges or refuse disconnection.
        throw new UnsupportedOperationException("Complete Kruskal edge selection");
    }
    static List<String> outputLines(Graph graph, List<Edge> tree) {
        if (tree.size() != graph.n - 1) throw new IllegalArgumentException("A tree needs N-1 edges");
        List<List<Integer>> adjacent = new ArrayList<>();
        for (int i = 0; i < graph.n; i++) adjacent.add(new ArrayList<>());
        List<String> lines = new ArrayList<>();
        Set<Edge> inputEdges = new HashSet<>(graph.edges);
        for (Edge edge : tree) {
            // Membership by object identity retains the exact weight of parallel input edges.
            if (!inputEdges.contains(edge)) throw new IllegalArgumentException("Returned edge is absent from input");
            adjacent.get(edge.p).add(edge.q); adjacent.get(edge.q).add(edge.p);
            lines.add(edge.p + " " + edge.q);
        }
        boolean[] seen = new boolean[graph.n]; int[] stack = new int[graph.n];
        int used = 1, reached = 1; stack[0] = 0; seen[0] = true;
        while (used > 0) for (int v : adjacent.get(stack[--used])) if (!seen[v]) {
            seen[v] = true; stack[used++] = v; reached++;
        }
        if (reached != graph.n) throw new IllegalArgumentException("Selected edges do not connect every vertex");
        // Connected N-1-edge output is feasible; minimum weight still needs an independent oracle.
        return lines;
    }
    public static void main(String[] args) {
        try {
            if (args.length != 0) throw new IllegalArgumentException("Use kruskal.in, not command arguments");
            Graph graph = readGraph(Path.of("kruskal.in"));
            List<String> lines = outputLines(graph, minimumTree(graph));
            Files.write(Path.of("kruskal.out"), lines, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve kruskal.in: " + error.getMessage()); System.exit(2);
        }
    }
}
