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
        String next() {
            if (!tokens.hasMoreTokens()) throw new IllegalArgumentException("Missing input token");
            return tokens.nextToken();
        }
        int integer(int minimum, int maximum) {
            long value = Long.parseLong(next());
            if (value < minimum || value > maximum) throw new IllegalArgumentException("Input token outside documented bounds");
            return (int) value;
        }
        void finish() {
            if (tokens.hasMoreTokens()) throw new IllegalArgumentException("Unexpected extra input token");
        }
    }
    static final class Input {
        final int budget;
        final int[] opponent;
        Input(int budget, int[] opponent) { this.budget = budget; this.opponent = opponent; }
    }
    static Input readInput() throws IOException {
        InputReader reader = new InputReader("hps.in");
        int n = reader.integer(1, 100000), budget = reader.integer(0, 20);
        int[] opponent = new int[n];
        for (int i = 0; i < n; i++) {
            String gesture = reader.next();
            if (gesture.equals("H")) opponent[i] = 0;
            else if (gesture.equals("P")) opponent[i] = 1;
            else if (gesture.equals("S")) opponent[i] = 2;
            else throw new IllegalArgumentException("Gesture must be H, P or S");
        }
        reader.finish();
        return new Input(budget, opponent);
    }
    static int maximumWins(Input input) {
        // TODO 1: Define prefix/budget/literal-Bessie-gesture states and initialize zero games.
        // TODO 2: Carry a gesture forward without spending another switch.
        // TODO 3: Consider a different previous gesture when switch budget is available.
        // TODO 4: Add an actual cyclic win and select the best final gesture within the budget.
        throw new UnsupportedOperationException("Complete the switch-budget DP before producing an answer");
    }
    static String output(Input input, int wins) {
        if (wins < 0 || wins > input.opponent.length) throw new IllegalArgumentException("Win count outside feasible bounds");
        return wins + "\n";
    }
    public static void main(String[] args) {
        try {
            Input input = readInput();
            String answer = output(input, maximumWins(input));
            Files.writeString(Path.of("hps.out"), answer, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve hps.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
