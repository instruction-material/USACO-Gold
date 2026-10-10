import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;

// Native Java. Run from the folder containing snowboots.in.
public class Main {
    static final int MAX_COUNT = 100000;
    static final int MAX_DEPTH = 1000000000;
    record Tile(int depth, int index) {}
    record Boot(int depth, int step, int index) {}
    record Input(int[] depths, Boot[] boots) {}

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
            int[] header = readLine(reader, 2, "N B header");
            int n = header[0], b = header[1];
            // With B >= 1 and 1 <= step <= N-1, no valid boot record exists for N=1.
            if (n < 2 || n > MAX_COUNT || b < 1 || b > MAX_COUNT) {
                throw new IllegalArgumentException("2 <= N <= 100000 and 1 <= B <= 100000");
            }
            int[] depths = readLine(reader, n, "tile depths");
            for (int depth : depths) {
                if (depth < 0 || depth > MAX_DEPTH) throw new IllegalArgumentException("Invalid tile depth");
            }
            if (depths[0] != 0 || depths[n - 1] != 0) {
                throw new IllegalArgumentException("Both endpoint depths must be zero");
            }
            Boot[] boots = new Boot[b];
            for (int i = 0; i < b; i++) {
                int[] row = readLine(reader, 2, "boot " + (i + 1));
                if (row[0] < 0 || row[0] > MAX_DEPTH || row[1] < 1 || row[1] >= n) {
                    throw new IllegalArgumentException("Invalid boot depth or step bound");
                }
                boots[i] = new Boot(row[0], row[1], i);
            }
            requireEnd(reader);
            return new Input(depths, boots);
        }
    }

    static final class ActivePath {
        final int[] previous;
        final int[] next;
        int maximumGap = 1;
        ActivePath(int length) {
            previous = new int[length];
            next = new int[length];
            for (int i = 0; i < length; i++) { previous[i] = i - 1; next[i] = i + 1; }
        }
        void remove(int tile) {
            // TASK 2: Unlink this interior tile by joining its surviving left and right neighbors.
            // TASK 3: Update maximumGap from the distance between those neighbors.
            // The zero-depth endpoints always survive every valid boot.
            throw new UnsupportedOperationException("Complete the path removal and maximum-gap tasks");
        }
    }

    static boolean fits(Boot boot, int requiredStep) {
        // TASK 4: Decide whether this boot can span the widest gap, including equality.
        throw new UnsupportedOperationException("Complete the step comparison task");
    }

    static int[] solve(Input input) {
        // TASK 1: Create Tile records and sort tiles and boots by decreasing depth.
        // TASK 5: Before each boot, remove EVERY tile whose depth is strictly greater than its depth limit.
        // TASK 6: Store 1 or 0 at the boot's original index and return B answers in input order.
        // Keep equal-depth tiles, bound the removal cursor, and explain the maximum-gap invariant.
        throw new UnsupportedOperationException("Complete the six Snow Boots tasks before producing an answer");
    }

    public static void main(String[] args) {
        try {
            Input input = readInput(Path.of("snowboots.in"));
            int[] answers = solve(input);
            if (answers == null || answers.length != input.boots.length) {
                throw new IllegalArgumentException("Return exactly B answers");
            }
            StringBuilder output = new StringBuilder();
            for (int answer : answers) {
                if (answer != 0 && answer != 1) throw new IllegalArgumentException("Each answer must be 0 or 1");
                output.append(answer).append('\n');
            }
            // Do not open the answer file until the full input and learner tasks succeed.
            Files.writeString(Path.of("snowboots.out"), output.toString(), StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve snowboots.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
