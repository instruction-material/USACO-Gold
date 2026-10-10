import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;

// Native Java. Run from the folder containing circlecross.in.
public class Main {
    static final int MAX_COWS = 50000;
    record Input(int n, int[] labels) {}
    record Cow(int entry, int exit) {}

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

    static void requireEnd(BufferedReader reader) throws IOException {
        String line;
        while ((line = reader.readLine()) != null) {
            if (!line.trim().isEmpty()) throw new IllegalArgumentException("Extra input after the declared records");
        }
    }

    static Input readInput(Path input) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
            int n = readLine(reader, 1, "N header")[0];
            if (n < 1 || n > MAX_COWS) throw new IllegalArgumentException("1 <= N <= 50000");
            int[] labels = new int[2 * n];
            int[] counts = new int[n];
            for (int i = 0; i < labels.length; i++) {
                int label = readLine(reader, 1, "cow at position " + (i + 1))[0];
                if (label < 1 || label > n) throw new IllegalArgumentException("Cow IDs must be between 1 and N");
                labels[i] = label - 1;
                if (++counts[label - 1] > 2) throw new IllegalArgumentException("Each cow must appear exactly twice");
            }
            for (int count : counts) {
                if (count != 2) throw new IllegalArgumentException("Each cow must appear exactly twice");
            }
            requireEnd(reader);
            return new Input(n, labels);
        }
    }

    static final class Fenwick {
        final int[] tree;
        Fenwick(int length) { tree = new int[length + 1]; }
        void add(int index, int delta) {
            // TASK 3: Convert the zero-based endpoint to one-based storage and update its Fenwick ancestors.
            throw new UnsupportedOperationException("Complete the endpoint update task");
        }
        int prefix(int index) {
            // TASK 4: Return the inclusive sum through this zero-based endpoint by visiting Fenwick parents.
            throw new UnsupportedOperationException("Complete the inclusive prefix task");
        }
    }

    static long solve(Input input) {
        // TASK 1: Pair each cow's first and second occurrence into a Cow(entry, exit).
        // TASK 2: Process these intervals by increasing entry position.
        // TASK 5: Count already marked exits strictly inside each interval, then mark its own exit.
        // Explain why this counts each crossing once and excludes nesting or disjoint intervals.
        throw new UnsupportedOperationException("Complete the five CircleCross tasks before producing an answer");
    }

    public static void main(String[] args) {
        try {
            Input input = readInput(Path.of("circlecross.in"));
            long answer = solve(input);
            long maximum = (long) input.n * (input.n - 1) / 2;
            if (answer < 0 || answer > maximum) throw new IllegalArgumentException("Invalid crossing count");
            // Do not open the answer file until the full input and learner tasks succeed.
            Files.writeString(Path.of("circlecross.out"), answer + "\n", StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve circlecross.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
