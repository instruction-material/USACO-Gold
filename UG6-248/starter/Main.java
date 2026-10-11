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
    static int[] readInput() throws IOException {
        InputReader reader=new InputReader("248.in");
        int n = reader.integer(2, 248);
        int[] values = new int[n];
        for (int i = 0; i < n; i++) {
            values[i] = reader.integer(1, 40);
        }
        reader.finish();
        return values;
    }
    static long largestTile(int[] values) {
        // TODO 1: Define which contiguous intervals can collapse to one tile and a sentinel for impossible intervals.
        // TODO 2: Initialize every singleton interval from its original tile.
        // TODO 3: Visit increasing interval lengths and test every split with equal, possible child tiles.
        // TODO 4: Track the greatest tile from any interval; the entire sequence need not collapse.
        throw new UnsupportedOperationException("Complete the four algorithm tasks before producing an answer");
    }
    static String output(int[] input, long value) {
        if(value < 1 || value > 47) throw new IllegalArgumentException("Result outside documented feasible bounds");
        return value+"\n";
    }
    public static void main(String[] args) {
        try {
            int[] input = readInput();
            String answer = output(input,largestTile(input));
            Files.writeString(Path.of("248.out"),answer,StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve 248.in: "+error.getMessage());
            System.exit(2);
        }
    }
}
