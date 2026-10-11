import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.StringTokenizer;

public class Main {
    static final class Input {
        final int width, height;
        final int[] vertical, horizontal;
        Input(int width, int height, int[] vertical, int[] horizontal) {
            this.width = width; this.height = height;
            this.vertical = vertical; this.horizontal = horizontal;
        }
    }
    static final class InputReader {
        final StringTokenizer tokens;
        InputReader() throws IOException {
            tokens = new StringTokenizer(Files.readString(
                Path.of("fencedin.in"), StandardCharsets.UTF_8));
        }
        int integer(int minimum, int maximum) {
            if (!tokens.hasMoreTokens()) throw new IllegalArgumentException("Missing input token");
            long value = Long.parseLong(tokens.nextToken());
            if (value < minimum || value > maximum) throw new IllegalArgumentException("Input token outside documented bounds");
            return (int) value;
        }
        int[] fences(int count, int outerBoundary) {
            int[] positions = new int[count];
            HashSet<Integer> seen = new HashSet<>();
            for (int i = 0; i < count; i++) {
                positions[i] = integer(1, outerBoundary - 1);
                if (!seen.add(positions[i])) throw new IllegalArgumentException("Fence positions must be distinct within each orientation");
            }
            return positions;
        }
        void finish() {
            if (tokens.hasMoreTokens()) throw new IllegalArgumentException("Unexpected extra input token");
        }
    }
    static Input readInput() throws IOException {
        InputReader reader = new InputReader();
        int width = reader.integer(1, 1000000000);
        int height = reader.integer(1, 1000000000);
        int n = reader.integer(0, 2000), m = reader.integer(0, 2000);
        int[] vertical = reader.fences(n, width);
        int[] horizontal = reader.fences(m, height);
        reader.finish();
        return new Input(width, height, vertical, horizontal);
    }
    static long minimumRemoval(Input input) {
        // TODO 1: Pad and sort fence coordinates; label each region and adjacent fence segment correctly.
        // TODO 2: Represent edges within the native memory budget, preserving weights and endpoints.
        // TODO 3: Process increasing weights and join only distinct components until all regions connect.
        // TODO 4: Use a long total and handle no fences, one orientation and tied segment lengths.
        throw new UnsupportedOperationException("Complete the four algorithm tasks before producing an answer");
    }
    static String output(Input input, long value) {
        long regions = (long) (input.vertical.length + 1) * (input.horizontal.length + 1);
        long upperBound = (regions - 1) * Math.max(input.width, input.height);
        if (value < 0 || value > upperBound) throw new IllegalArgumentException("Result outside documented feasible bounds");
        return value + "\n";
    }
    public static void main(String[] args) {
        try {
            Input input = readInput();
            String answer = output(input, minimumRemoval(input));
            Files.writeString(Path.of("fencedin.out"), answer, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve fencedin.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
