// ADDED: Optional Gold tree-path learner pack. Complete the four solve tasks.
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

class Main {
    static final int MAX_SIZE = 100000;

    static class Problem {
        final int[] types;
        final List<List<Integer>> graph;
        final int[][] queries;
        Problem(int[] types, List<List<Integer>> graph, int[][] queries) {
            this.types = types;
            this.graph = graph;
            this.queries = queries;
        }
    }

    static int[] record(BufferedReader reader, int length) throws IOException {
        String line = reader.readLine();
        if (line == null || line.isBlank()) throw new IllegalArgumentException("Missing record");
        String[] words = line.trim().split("\\s+");
        if (words.length != length) throw new IllegalArgumentException("Wrong record length");
        int[] values = new int[length];
        for (int i = 0; i < length; i++) values[i] = Integer.parseInt(words[i]);
        return values;
    }

    static int index(int value, int n) {
        if (value < 1 || value > n) throw new IllegalArgumentException("Value outside 1..N");
        return value - 1;
    }

    static Problem readProblem(Path input) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
            int[] header = record(reader, 2);
            int n = header[0], m = header[1];
            if (n < 1 || n > MAX_SIZE || m < 1 || m > MAX_SIZE) {
                throw new IllegalArgumentException("Use 1 <= N, M <= 100000");
            }
            int[] types = record(reader, n);
            List<List<Integer>> graph = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                types[i] = index(types[i], n);
                graph.add(new ArrayList<>());
            }
            for (int i = 0; i < n - 1; i++) {
                int[] edge = record(reader, 2);
                int a = index(edge[0], n), b = index(edge[1], n);
                if (a == b) throw new IllegalArgumentException("Tree edges need distinct farms");
                graph.get(a).add(b);
                graph.get(b).add(a);
            }
            // Connectivity plus exactly N-1 undirected edges establishes the tree contract.
            boolean[] seen = new boolean[n];
            int[] queue = new int[n];
            int head = 0, tail = 1;
            seen[0] = true;
            while (head < tail) {
                for (int next : graph.get(queue[head++])) {
                    if (!seen[next]) {
                        seen[next] = true;
                        queue[tail++] = next;
                    }
                }
            }
            if (tail != n) throw new IllegalArgumentException("Edges must form one tree");
            int[][] queries = new int[m][3];
            for (int i = 0; i < m; i++) {
                int[] query = record(reader, 3);
                for (int j = 0; j < 3; j++) queries[i][j] = index(query[j], n);
            }
            for (String extra; (extra = reader.readLine()) != null;) {
                if (!extra.isBlank()) throw new IllegalArgumentException("Unexpected extra record");
            }
            return new Problem(types, graph, queries);
        }
    }

    static boolean[] solve(Problem problem) {
        // TODO 1: Build pre/post ancestor intervals with explicit enter/exit frames.
        // TODO 2: Index queries at their endpoints; keep a root path and per-type stacks.
        // TODO 3: On entry, inspect the nearest matching ancestor for each endpoint query.
        // TODO 4: On exit, remove the current farm from both path and type state.
        // Produce one boolean per query in original order. Do not recurse at full depth.
        throw new UnsupportedOperationException("Complete the four Milk Visits tree-path tasks");
    }

    public static void main(String[] args) {
        try {
            if (args.length != 0) throw new IllegalArgumentException("No command-line arguments expected");
            Problem problem = readProblem(Path.of("milkvisits.in"));
            boolean[] answer = solve(problem);
            if (answer == null || answer.length != problem.queries.length) {
                throw new IllegalArgumentException("Return one answer per query");
            }
            StringBuilder output = new StringBuilder();
            for (boolean value : answer) output.append(value ? '1' : '0');
            output.append('\n');
            // Finish input validation and the learner algorithm before opening the answer file.
            Files.writeString(Path.of("milkvisits.out"), output, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve milkvisits.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
