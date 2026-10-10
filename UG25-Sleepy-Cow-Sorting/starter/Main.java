import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;

// Native Java. Run beside sleepy.in; the browser preview does not execute this algorithm.
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
            int[] values = readLine(reader, n, "permutation");
            boolean[] seen = new boolean[n];
            for (int i = 0; i < n; i++) {
                int value = values[i];
                if (value < 1 || value > n || seen[value - 1]) throw new IllegalArgumentException("The row must be a permutation of 1..N");
                seen[value - 1] = true;
                values[i]--;
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

    record Plan(int[] steps) {}

    static Plan solve(Input input) {
        // TASK 1: Locate the longest strictly increasing suffix.
        // TASK 4: Mark suffix values, retaining the original prefix order.
        // TASK 5: Record unprocessed-prefix count plus smaller inserted values; then mark each moved value.
        throw new UnsupportedOperationException("Complete the five Sleepy Cow Sorting tasks before producing an answer");
    }

    public static void main(String[] args) {
        try {
            Input input = readInput(Path.of("sleepy.in"));
            Plan plan = solve(input);
            if (plan == null || plan.steps == null || plan.steps.length >= input.n) throw new IllegalArgumentException("Invalid move count");
            StringBuilder answer = new StringBuilder().append(plan.steps.length).append('\n');
            for (int i = 0; i < plan.steps.length; i++) {
                int step = plan.steps[i];
                if (step < 1 || step >= input.n) throw new IllegalArgumentException("Each move must lie between 1 and N-1");
                if (i > 0) answer.append(' ');
                answer.append(step);
            }
            answer.append('\n');
            // Bounds and serialization only; independent checks must verify sorting and optimality.
            Files.writeString(Path.of("sleepy.out"), answer, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve sleepy.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
