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
        final int cutoff;
        final int[] x, y;
        Input(int cutoff, int[] x, int[] y) { this.cutoff = cutoff; this.x = x; this.y = y; }
    }
    static Input readInput() throws IOException {
        InputReader reader = new InputReader("irrigation.in");
        int n = reader.take(1, 2000), cutoff = reader.take(1, 1000000);
        int[] x = new int[n], y = new int[n];
        java.util.HashSet<Integer> points = new java.util.HashSet<>();
        for (int i = 0; i < n; i++) {
            x[i] = reader.take(0, 1000); y[i] = reader.take(0, 1000);
            if (!points.add(x[i] * 1001 + y[i])) throw new IllegalArgumentException("Point coordinates must be distinct");
        }
        reader.finish();
        return new Input(cutoff, x, y);
    }
    static long minimumCost(Input input) {
        // TODO 1: Initialize connecting keys, visited flags and the root key.
        // TODO 2: Select the cheapest unvisited point; an infinite key means disconnection.
        // TODO 3: Attach the point and add its connecting key to a long total.
        // TODO 4: Compute squared lengths and relax eligible unvisited neighbors (length >= cutoff).
        throw new UnsupportedOperationException("Complete the eligible-edge MST before producing an answer");
    }
    static String output(Input input, long total) {
        if (total < -1 || total > (input.x.length - 1) * 2000000L
                || (total >= 0 && total < (input.x.length - 1L) * input.cutoff)
                || (input.x.length == 1 && total != 0)) {
            throw new IllegalArgumentException("Tree total outside feasible bounds");
        }
        return total + "\n";
    }
    public static void main(String[] args) {
        try {
            Input input = readInput();
            String answer = output(input, minimumCost(input));
            Files.writeString(Path.of("irrigation.out"), answer, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve irrigation.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
