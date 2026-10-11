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
        final int n, groups;
        Input(int n, int groups) { this.n = n; this.groups = groups; }
    }
    static Input readInput() throws IOException {
        InputReader reader = new InputReader("walk.in");
        int n = reader.take(2, 7500), groups = reader.take(2, n);
        reader.finish();
        return new Input(n, groups);
    }
    static long maximumSpacing(Input input) {
        // TODO 1: Generate symmetric weights with one-based labels and long products.
        // TODO 2: Build an implicit dense MST with connecting keys and visited state.
        // TODO 3: Collect exactly N-1 real connecting weights; exclude the root zero.
        // TODO 4: Use the cut/order-statistic argument to find the spacing for K groups.
        throw new UnsupportedOperationException("Complete maximum-spacing clustering before producing an answer");
    }
    static String output(long spacing) {
        if (spacing <= 0 || spacing >= 2019201997L) throw new IllegalArgumentException("Spacing outside the edge bounds");
        return spacing + "\n";
    }
    public static void main(String[] args) {
        try {
            Input input = readInput();
            String answer = output(maximumSpacing(input));
            Files.writeString(Path.of("walk.out"), answer, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve walk.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
