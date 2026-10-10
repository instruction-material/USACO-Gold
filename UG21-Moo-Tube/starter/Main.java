import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

// Native Java. Run from the folder containing mootube.in.
public class Main {
    static final int MAX_COUNT = 100000;
    static final int MAX_RELEVANCE = 1000000000;

    record Edge(int p, int q, int weight) {}
    record Query(int k, int v, int index) {}
    record Input(int n, Edge[] edges, Query[] queries) {}

    static int[] readLine(BufferedReader reader, int count, String label) throws IOException {
        String line = reader.readLine();
        if (line == null) throw new IllegalArgumentException("Missing " + label);
        StringTokenizer tokens = new StringTokenizer(line);
        if (tokens.countTokens() != count) {
            throw new IllegalArgumentException(label + " needs exactly " + count + " integers");
        }
        int[] values = new int[count];
        for (int i = 0; i < count; i++) values[i] = Integer.parseInt(tokens.nextToken());
        return values;
    }

    static Input readInput(Path input) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
            int[] header = readLine(reader, 2, "N Q header");
            int n = header[0], q = header[1];
            if (n < 1 || n > MAX_COUNT || q < 1 || q > MAX_COUNT) {
                throw new IllegalArgumentException("1 <= N, Q <= 100000");
            }
            Edge[] edges = new Edge[n - 1];
            for (int i = 0; i < edges.length; i++) {
                int[] row = readLine(reader, 3, "edge " + (i + 1));
                if (row[0] < 1 || row[0] > n || row[1] < 1 || row[1] > n
                        || row[0] == row[1] || row[2] < 1 || row[2] > MAX_RELEVANCE) {
                    throw new IllegalArgumentException("Invalid edge endpoint or relevance");
                }
                edges[i] = new Edge(row[0] - 1, row[1] - 1, row[2]);
            }
            Query[] queries = new Query[q];
            for (int i = 0; i < q; i++) {
                int[] row = readLine(reader, 2, "query " + (i + 1));
                if (row[0] < 1 || row[0] > MAX_RELEVANCE || row[1] < 1 || row[1] > n) {
                    throw new IllegalArgumentException("Invalid query threshold or video");
                }
                queries[i] = new Query(row[0], row[1] - 1, i);
            }
            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    throw new IllegalArgumentException("Extra input after the queries");
                }
            }
            return new Input(n, edges, queries);
        }
    }

    static final class DisjointSets {
        final int[] parent;
        final int[] weight;
        DisjointSets(int n) {
            parent = new int[n];
            weight = new int[n];
            for (int i = 0; i < n; i++) { parent[i] = i; weight[i] = 1; }
        }
        int root(int vertex) {
            // TASK 1: Follow parent links to a root. Optional path compression is a later extension.
            throw new UnsupportedOperationException("Complete the DSU root task");
        }
        void connect(int a, int b) {
            // TASK 2: Find both roots; if distinct, attach the smaller component and update its size.
            throw new UnsupportedOperationException("Complete the weighted union task");
        }
        int size(int vertex) {
            // TASK 3: Read the size stored at the root of this video.
            throw new UnsupportedOperationException("Complete the component size task");
        }
    }

    static int[] solve(Input input) {
        // TASK 4: Sort edges and queries by descending relevance and threshold.
        // TASK 5: Before each query, connect EVERY unused edge whose weight >= its threshold.
        // TASK 6: Store component size minus one at the query's original index.
        // Return all Q answers in the original input order, not the sorted query order.
        throw new UnsupportedOperationException("Complete the six MooTube tasks before producing an answer");
    }

    public static void main(String[] args) {
        try {
            Input input = readInput(Path.of("mootube.in"));
            int[] answers = solve(input);
            if (answers == null || answers.length != input.queries.length) {
                throw new IllegalArgumentException("Return exactly Q answers");
            }
            List<String> lines = new ArrayList<>(answers.length);
            for (int answer : answers) {
                if (answer < 0 || answer >= input.n) {
                    throw new IllegalArgumentException("Answer must be between 0 and N-1");
                }
                lines.add(Integer.toString(answer));
            }
            // Parse the entire input and finish the learner tasks before opening the answer file.
            Files.write(Path.of("mootube.out"), lines, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve mootube.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
