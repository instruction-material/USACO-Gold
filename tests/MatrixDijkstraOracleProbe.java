// Independent Bellman-Ford distances and predecessor-edge checks for the matrix reference.
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

class MatrixDijkstraOracleProbe {
    static void check(int n, List<int[]> records) {
        Main.N = n;
        Main.M = records.size();
        Main.edge = new int[n][n];
        for (int[] row : Main.edge) Arrays.fill(row, -1);
        for (int[] edge : records) {
            int a = edge[0], b = edge[1], w = edge[2];
            if (Main.edge[a][b] == -1 || w < Main.edge[a][b]) {
                Main.edge[a][b] = w;
                Main.edge[b][a] = w;
            }
        }
        long[] expected = new long[n];
        Arrays.fill(expected, Long.MAX_VALUE);
        expected[0] = 0;
        for (int pass = 1; pass < n; pass++) {
            boolean changed = false;
            for (int[] edge : records) {
                for (int direction = 0; direction < 2; direction++) {
                    int a = edge[direction], b = edge[1 - direction];
                    if (expected[a] == Long.MAX_VALUE) continue;
                    long candidate = expected[a] + edge[2];
                    if (candidate < expected[b]) {
                        expected[b] = candidate;
                        changed = true;
                    }
                }
            }
            if (!changed) break;
        }
        Main.dist = new long[n];
        Main.prev = new int[n];
        Main.dijkstra(0);
        if (!Arrays.equals(Main.dist, expected) || Main.prev[0] != -1) {
            throw new AssertionError("Bellman-Ford distance mismatch");
        }
        for (int target = 1; target < n; target++) {
            if (expected[target] == Long.MAX_VALUE) {
                if (Main.prev[target] != -1) throw new AssertionError("Unreachable predecessor");
                continue;
            }
            boolean[] seen = new boolean[n];
            long sum = 0;
            int node = target;
            while (node != 0) {
                if (node < 0 || node >= n || seen[node]) throw new AssertionError("Invalid path");
                seen[node] = true;
                int parent = Main.prev[node];
                if (parent < 0 || parent >= n || Main.edge[parent][node] < 0) {
                    throw new AssertionError("Missing path edge");
                }
                sum += Main.edge[parent][node];
                node = parent;
            }
            if (sum != expected[target]) throw new AssertionError("Path cost mismatch");
        }
    }

    public static void main(String[] args) {
        Random random = new Random(20261010L);
        int graphs = 0;
        for (int n = 1; n <= 8; n++) {
            for (int trial = 0; trial < 40; trial++) {
                List<int[]> edges = new ArrayList<>();
                int m = trial % (n * n + 1);
                for (int i = 0; i < m; i++) {
                    int weight = trial % 3 == 0 ? random.nextInt(3)
                            : trial % 3 == 1 ? random.nextInt(20) : Integer.MAX_VALUE;
                    edges.add(new int[] {random.nextInt(n), random.nextInt(n), weight});
                }
                check(n, edges);
                graphs++;
            }
        }
        List<int[]> chain = new ArrayList<>();
        for (int i = 0; i < 1999; i++) chain.add(new int[] {i, i + 1, Integer.MAX_VALUE});
        check(2000, chain);
        if (Main.dist[1999] != 4292819810353L) throw new AssertionError("Maximum path total");
        if (new Main.State(Long.MAX_VALUE, 1).compareTo(new Main.State(0, 0)) <= 0
                || new Main.State(0, 0).compareTo(new Main.State(Long.MAX_VALUE, 1)) >= 0) {
            throw new AssertionError("Queue comparator overflow");
        }
        System.out.println("MATRIX_BELLMAN_FORD_PATH_ORACLE_PASS " + (graphs + 1));
    }
}
