import java.util.Arrays;

// Bellman-Ford plus independent edge/path checks, not another Dijkstra implementation.
class DijkstraOracleProbe {
    static int graphs;
    static void check(int n, long[][] edges) {
        Main.Graph graph = new Main.Graph(n);
        long[][] weights = new long[n][n];
        for (long[] row : weights) Arrays.fill(row, Main.INF);
        for (int i = 0; i < n; i++) weights[i][i] = 0;
        for (long[] edge : edges) {
            int a = (int) edge[0], b = (int) edge[1];
            long w = edge[2];
            graph.addEdge(a, b, w);
            weights[a][b] = weights[b][a] = Math.min(weights[a][b], w);
        }
        long[] expected = new long[n];
        Arrays.fill(expected, Main.INF);
        expected[0] = 0;
        for (int pass = 1; pass < n; pass++) {
            boolean changed = false;
            for (long[] edge : edges) {
                int a = (int) edge[0], b = (int) edge[1];
                long w = edge[2];
                if (expected[a] != Main.INF && expected[a] + w < expected[b]) {
                    expected[b] = expected[a] + w;
                    changed = true;
                }
                if (expected[b] != Main.INF && expected[b] + w < expected[a]) {
                    expected[a] = expected[b] + w;
                    changed = true;
                }
            }
            if (!changed) break;
        }
        Main.Result actual = Main.shortestPaths(graph);
        if (!Arrays.equals(actual.distance, expected) || actual.previous[0] != -1) {
            throw new AssertionError("Distance mismatch in graph " + graphs);
        }
        for (int destination = 1; destination < n; destination++) {
            if (expected[destination] == Main.INF) {
                if (actual.previous[destination] != -1) throw new AssertionError("Unreachable predecessor");
                continue;
            }
            boolean[] seen = new boolean[n];
            int current = destination;
            long total = 0;
            while (current != 0) {
                if (current < 0 || current >= n || seen[current]) throw new AssertionError("Cyclic/missing path");
                seen[current] = true;
                int previous = actual.previous[current];
                if (previous < 0 || previous >= n || weights[previous][current] == Main.INF) {
                    throw new AssertionError("Path uses a nonexistent edge");
                }
                total += weights[previous][current];
                current = previous;
            }
            if (total != expected[destination]) throw new AssertionError("Path cost mismatch");
        }
        graphs++;
    }

    public static void main(String[] args) {
        for (int n = 1; n <= 4; n++) {
            int pairs = n * (n - 1) / 2;
            int variants = 1;
            for (int i = 0; i < pairs; i++) variants *= 4;
            for (int mask = 0; mask < variants; mask++) {
                long[][] edges = new long[pairs][3];
                int used = 0, code = mask;
                for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
                    int digit = code % 4;
                    code /= 4;
                    if (digit != 0) edges[used++] = new long[]{a, b, digit == 3 ? 4 : digit - 1};
                }
                check(n, Arrays.copyOf(edges, used));
            }
        }
        check(3, new long[][]{{1, 2, 1}}); // The original reference overflowed in this disconnected component.
        check(3, new long[][]{{0, 1, 1}, {0, 1, 9}, {1, 1, 0}, {1, 2, 0}});
        check(4, new long[][]{{0, 1, 1000000000L}, {1, 2, 1000000000L}, {2, 3, 1000000000L}});
        if (graphs != 4168) throw new AssertionError("Unexpected oracle fixture coverage");
        System.out.println("BELLMAN_FORD_PATH_ORACLE_PASS " + graphs);
    }
}
