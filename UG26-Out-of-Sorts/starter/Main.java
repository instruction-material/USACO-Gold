import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;

// Native Java. Run beside sort.in; the browser preview does not execute this algorithm.
public class Main {
    record Input(int n, int[] values) {}

    static int[] readLine(BufferedReader reader, int count, String label) throws IOException {
        String line = reader.readLine();
        if (line == null) throw new IllegalArgumentException("Missing " + label);
        StringTokenizer tokens = new StringTokenizer(line);
        if (tokens.countTokens() != count) throw new IllegalArgumentException(label + " needs exactly " + count + " integers");
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
            if (n < 1 || n > 100000) throw new IllegalArgumentException("1 <= N <= 100000");
            int[] values = new int[n];
            for (int i = 0; i < n; i++) {
                int value = readLine(reader, 1, "value at position " + (i + 1))[0];
                if (value < 0 || value > 1000000000) throw new IllegalArgumentException("Values must be between 0 and 1000000000");
                values[i] = value;
            }
            requireEnd(reader);
            return new Input(n, values);
        }
    }

    static final class Fenwick {
        final int[] tree;
        Fenwick(int length) { tree = new int[length + 1]; }
        void add(int index, int delta) {
            // TASK 2: Convert a zero-based index to one-based storage, then update Fenwick ancestors.
            throw new UnsupportedOperationException("Complete the point update task");
        }
        int prefix(int index) {
            // TASK 3: Sum through this inclusive zero-based index; a negative index has sum zero.
            throw new UnsupportedOperationException("Complete the inclusive prefix task");
        }
    }

    record Number(int value, int position) {}

    static int solve(Input input) {
        // TASK 1: Order Number(value, position) records stably, preserving tie order.
        // TASK 4: Mark the first k sorted values and count marks in the first k original positions.
        // TASK 5: Return the maximum cut deficit, starting at one, for the Gold forward/backward rule.
        throw new UnsupportedOperationException("Complete the five Out of Sorts, Gold bidirectional sweeps tasks before producing an answer");
    }

    public static void main(String[] args) {
        try {
            Input input = readInput(Path.of("sort.in"));
            int answer = solve(input);
            if (answer < 1 || answer > input.n) throw new IllegalArgumentException("Invalid answer range");
            // Open the answer file only after the full input and unfinished tasks succeed.
            Files.writeString(Path.of("sort.out"), answer + "\n", StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve sort.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
