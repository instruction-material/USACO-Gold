import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Random;

// Independent Kruskal and exhaustive spanning-tree checks of the actual Prim method.
class MstOracleProbe {
    static final class Edge {
        final int a, b, w;
        Edge(int a, int b, int w) { this.a = a; this.b = b; this.w = w; }
    }
    static final class Dsu {
        final int[] parent;
        Dsu(int n) { parent = new int[n]; for (int i = 0; i < n; i++) parent[i] = i; }
        int find(int v) { while (parent[v] != v) v = parent[v]; return v; }
        boolean join(int a, int b) {
            a = find(a); b = find(b);
            if (a == b) return false;
            parent[a] = b;
            return true;
        }
    }
    static Long kruskal(int n, List<Edge> input) {
        List<Edge> edges = new ArrayList<>(input);
        edges.sort(Comparator.comparingInt(e -> e.w));
        Dsu dsu = new Dsu(n);
        int count = 0;
        long total = 0;
        for (Edge e : edges) if (dsu.join(e.a, e.b)) { count++; total += e.w; }
        return count == n - 1 ? Long.valueOf(total) : null;
    }
    static Long enumerateTrees(int n, List<Edge> edges) {
        long answer = Long.MAX_VALUE;
        for (int mask = 0; mask < (1 << edges.size()); mask++) {
            if (Integer.bitCount(mask) != n - 1) continue;
            Dsu dsu = new Dsu(n);
            long sum = 0;
            boolean tree = true;
            for (int i = 0; i < edges.size(); i++) if ((mask & (1 << i)) != 0) {
                Edge e = edges.get(i);
                if (!dsu.join(e.a, e.b)) { tree = false; break; }
                sum += e.w;
            }
            if (tree) answer = Math.min(answer, sum);
        }
        return answer == Long.MAX_VALUE ? null : Long.valueOf(answer);
    }
    static void check(int n, List<Edge> edges, boolean exhaustive) {
        Long expected = kruskal(n, edges);
        if (exhaustive && !java.util.Objects.equals(expected, enumerateTrees(n, edges))) {
            throw new AssertionError("Kruskal differs from exhaustive spanning-tree oracle");
        }
        Main.Graph graph = new Main.Graph(n);
        for (Edge e : edges) graph.addEdge(e.a, e.b, e.w);
        if (expected == null) {
            try { Main.minimumTree(graph); }
            catch (IllegalArgumentException error) {
                if (error.getMessage().contains("disconnected")) return;
                throw error;
            }
            throw new AssertionError("Disconnected graph accepted");
        }
        Main.Result result = Main.minimumTree(graph);
        if (result.total != expected.longValue()) throw new AssertionError("Wrong minimum total");
        if (Main.outputLines(graph, result).size() != n) throw new AssertionError("Wrong edge count");
        Dsu dsu = new Dsu(n);
        long sum = 0;
        for (int v = 1; v < n; v++) {
            int parent = result.previous[v];
            if (!dsu.join(v, parent)) throw new AssertionError("Cyclic selected edges");
            int cheapest = Integer.MAX_VALUE;
            for (Edge e : edges) {
                if ((e.a == v && e.b == parent) || (e.a == parent && e.b == v)) {
                    cheapest = Math.min(cheapest, e.w);
                }
            }
            if (cheapest == Integer.MAX_VALUE) throw new AssertionError("Invented edge");
            sum += cheapest;
        }
        if (sum != expected.longValue()) throw new AssertionError("Returned tree is not minimal");
    }
    public static void main(String[] args) {
        int count = 0;
        int[][] pairs = {{0,1}, {0,2}, {0,3}, {1,2}, {1,3}, {2,3}};
        for (int code = 0; code < 729; code++) {
            int digits = code;
            List<Edge> edges = new ArrayList<>();
            for (int[] pair : pairs) {
                int choice = digits % 3; digits /= 3;
                if (choice != 0) edges.add(new Edge(pair[0], pair[1], choice - 1));
            }
            check(4, edges, true); count++;
        }
        Random random = new Random(14020261010L);
        for (int trial = 0; trial < 2048; trial++) {
            int n = 1 + random.nextInt(10);
            List<Edge> edges = new ArrayList<>();
            int m = random.nextInt(40);
            for (int i = 0; i < m; i++) {
                int weight = i % 7 == 0 ? 1000000000 : random.nextInt(12);
                edges.add(new Edge(random.nextInt(n), random.nextInt(n), weight));
            }
            check(n, edges, false); count++;
        }
        check(1, List.of(), true); count++;
        check(2, List.of(new Edge(0,1,1), new Edge(0,1,9)), true); count++;
        check(2, List.of(new Edge(0,1,9), new Edge(0,1,1)), true); count++;
        check(4, List.of(new Edge(0,1,1000000000), new Edge(1,2,1000000000),
                        new Edge(2,3,1000000000)), true); count++;
        check(3, List.of(new Edge(0,0,0), new Edge(0,1,0), new Edge(1,2,0)), true); count++;
        check(3, List.of(new Edge(1,2,1)), true); count++;
        check(3, List.of(new Edge(0,1,10), new Edge(0,2,6), new Edge(1,2,5)), true); count++;
        System.out.println("KRUSKAL_AND_TREE_ORACLE_PASS " + count);
    }
}
