import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;

public class Main {
    static final class InputReader {
        final StringTokenizer tokens;
        InputReader(String file) throws IOException {
            tokens = new StringTokenizer(Files.readString(Path.of(file), StandardCharsets.UTF_8));
        }
        int take(int minimum, int maximum) {
            if (!tokens.hasMoreTokens()) throw new IllegalArgumentException("Missing input token");
            long value = Long.parseLong(tokens.nextToken());
            if (value < minimum || value > maximum) throw new IllegalArgumentException("Input token outside documented bounds");
            return (int) value;
        }
        void finish() {
            if (tokens.hasMoreTokens()) throw new IllegalArgumentException("Unexpected extra input token");
        }
    }
    static final class Input {
        final int threshold;
        final int[] weights, talents;
        Input(int threshold, int[] weights, int[] talents) {
            this.threshold = threshold; this.weights = weights; this.talents = talents;
        }
    }
    static Input readInput() throws IOException {
        InputReader reader = new InputReader("talent.in");
        int n = reader.take(1, 250), threshold = reader.take(1, 1000);
        int[] weights = new int[n], talents = new int[n];
        long available = 0;
        for (int i = 0; i < n; i++) {
            weights[i] = reader.take(1, 1000000); talents[i] = reader.take(1, 1000);
            available += weights[i];
        }
        reader.finish();
        if (available < threshold) throw new IllegalArgumentException("Total available weight is below W");
        return new Input(threshold, weights, talents);
    }
    static boolean feasible(Input input, long ratio) {
        // TODO 1: Initialize the empty choice and unreachable transformed-score states.
        // TODO 2: Process one-use skip/take choices, clamping reached weights to W.
        // TODO 3: Return whether the threshold state has nonnegative transformed score.
        throw new UnsupportedOperationException("Complete the ratio feasibility DP");
    }
    static long bestRatio(Input input) {
        // TODO 4: Binary-search the greatest feasible integer ratio with explicit bound invariants.
        throw new UnsupportedOperationException("Complete ratio binary search before producing an answer");
    }
    static String output(long ratio) {
        if (ratio < 0 || ratio > 1000000L) throw new IllegalArgumentException("Scaled ratio outside feasible bounds");
        return ratio + "\n";
    }
    public static void main(String[] args) {
        try {
            Input input = readInput();
            String answer = output(bestRatio(input));
            Files.writeString(Path.of("talent.out"), answer, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve talent.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
