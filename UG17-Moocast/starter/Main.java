import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;

public class Main {
    static final class InputReader {
        final StringTokenizer tokens;
        InputReader(String file) throws IOException {
            tokens = new StringTokenizer(Files.readString(
                Path.of(file), StandardCharsets.UTF_8));
        }
        int integer(int minimum, int maximum) {
            if (!tokens.hasMoreTokens()) {
                throw new IllegalArgumentException("Missing input token");
            }
            long value = Long.parseLong(tokens.nextToken());
            if (value < minimum || value > maximum) {
                throw new IllegalArgumentException(
                    "Input token outside documented bounds");
            }
            return (int) value;
        }
        void finish() {
            if (tokens.hasMoreTokens()) {
                throw new IllegalArgumentException("Unexpected extra input token");
            }
        }
    }
    static int[][] readInput() throws IOException {
        InputReader reader=new InputReader("moocast.in");
        int n = reader.integer(1, 1000);
        int[][] cows = new int[n][2];
        for (int i = 0; i < n; i++) {
            cows[i][0] = reader.integer(0, 25000);
            cows[i][1] = reader.integer(0, 25000);
        }
        reader.finish();
        return cows;
    }
    static long minimumPower(int[][] cows) {
        // TODO 1: Model an undirected edge by squared coordinate distance; no square root is needed.
        // TODO 2: Connect every cow with minimum spanning-tree crossing-edge choices.
        // TODO 3: Update the cheapest edge linking each unchosen cow to the chosen set.
        // TODO 4: Return the greatest selected edge, rather than the sum; one cow needs zero power.
        throw new UnsupportedOperationException("Complete the four algorithm tasks before producing an answer");
    }
    static String output(int[][] input, long value) {
        if(value < 0 || value > 1250000000L) throw new IllegalArgumentException("Result outside documented feasible bounds");
        return value+"\n";
    }
    public static void main(String[] args) {
        try {
            int[][] input = readInput();
            String answer = output(input,minimumPower(input));
            Files.writeString(Path.of("moocast.out"),answer,StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve moocast.in: "+error.getMessage());
            System.exit(2);
        }
    }
}
