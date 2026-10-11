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
        InputReader reader=new InputReader("superbull.in");
        int n = reader.integer(1, 2000);
        int[] teams = new int[n];
        java.util.HashSet<Integer> seen = new java.util.HashSet<>();
        for (int i = 0; i < n; i++) {
            teams[i] = reader.integer(1, 1073741823);
            if (!seen.add(teams[i])) {
                throw new IllegalArgumentException("Team IDs must be distinct");
            }
        }
        reader.finish();
        return teams;
    }
    static long maximumScore(int[] teams) {
        // TODO 1: Explain why a sequence of elimination games forms a spanning tree.
        // TODO 2: Choose maximum XOR crossing edges, or negate weights consistently for a minimum-key formulation.
        // TODO 3: Include each team once and update its best connection to the chosen set.
        // TODO 4: Accumulate all selected game scores in long; a single team needs zero games.
        throw new UnsupportedOperationException("Complete the four algorithm tasks before producing an answer");
    }
    static String output(int[] input, long value) {
        if(value < 0 || value > (long)(input.length-1)*1073741823L) throw new IllegalArgumentException("Result outside documented feasible bounds");
        return value+"\n";
    }
    public static void main(String[] args) {
        try {
            int[] input = readInput();
            String answer = output(input,maximumScore(input));
            Files.writeString(Path.of("superbull.out"),answer,StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve superbull.in: "+error.getMessage());
            System.exit(2);
        }
    }
}
