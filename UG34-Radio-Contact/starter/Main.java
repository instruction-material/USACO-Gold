import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;

public final class Main {
    static final class Input {
        final int[][] firstPath;
        final int[][] secondPath;

        Input(int[][] firstPath, int[][] secondPath) {
            this.firstPath = firstPath;
            this.secondPath = secondPath;
        }
    }

    static long minimumEnergy(Input input) {
        // TASK 1: Define a state using completed steps on the two paths.
        // TASK 2: Compare advancing the first path, the second path, or both.
        // TASK 3: Add the squared distance after each move; exclude the initial state.
        // Complete both paths without permitting a transition that advances neither.
        throw new UnsupportedOperationException("The movement schedule is unfinished.");
    }

    static long energy(Input input, int first, int second) {
        long dx = (long) input.firstPath[first][0] - input.secondPath[second][0];
        long dy = (long) input.firstPath[first][1] - input.secondPath[second][1];
        return dx * dx + dy * dy;
    }

    private static int integer(StringTokenizer tokens, int low, int high) {
        if (!tokens.hasMoreTokens()) {
            throw new IllegalArgumentException("An input integer is missing.");
        }
        int value;
        try {
            value = Integer.parseInt(tokens.nextToken());
        } catch (NumberFormatException error) {
            throw new IllegalArgumentException("An input token is not an integer.", error);
        }
        if (value < low || value > high) {
            throw new IllegalArgumentException("An input integer is outside its bounds.");
        }
        return value;
    }

    private static int[][] path(int x, int y, int count, StringTokenizer tokens) {
        if (!tokens.hasMoreTokens()) {
            throw new IllegalArgumentException("A direction string is missing.");
        }
        String directions = tokens.nextToken();
        if (directions.length() != count) {
            throw new IllegalArgumentException("A direction string has the wrong length.");
        }
        int[][] positions = new int[count + 1][2];
        positions[0][0] = x;
        positions[0][1] = y;
        for (int i = 0; i < count; i++) {
            switch (directions.charAt(i)) {
                case 'N': y++; break;
                case 'E': x++; break;
                case 'S': y--; break;
                case 'W': x--; break;
                default: throw new IllegalArgumentException("Directions must be N, E, S or W.");
            }
            if (x < 0 || x > 1_000 || y < 0 || y > 1_000) {
                throw new IllegalArgumentException("Every path position must remain within 0 through 1000.");
            }
            positions[i + 1][0] = x;
            positions[i + 1][1] = y;
        }
        return positions;
    }

    static Input readInput(String text) {
        StringTokenizer tokens = new StringTokenizer(text);
        int firstCount = integer(tokens, 1, 1_000);
        int secondCount = integer(tokens, 1, 1_000);
        int firstX = integer(tokens, 0, 1_000);
        int firstY = integer(tokens, 0, 1_000);
        int secondX = integer(tokens, 0, 1_000);
        int secondY = integer(tokens, 0, 1_000);
        int[][] first = path(firstX, firstY, firstCount, tokens);
        int[][] second = path(secondX, secondY, secondCount, tokens);
        if (tokens.hasMoreTokens()) {
            throw new IllegalArgumentException("Unexpected trailing input.");
        }
        return new Input(first, second);
    }

    public static void main(String[] args) {
        try {
            Input input = readInput(Files.readString(Path.of("radio.in"), StandardCharsets.UTF_8));
            long answer = minimumEnergy(input);
            if (answer < 0) {
                throw new IllegalArgumentException("The energy must be nonnegative.");
            }
            Files.writeString(Path.of("radio.out"), answer + "\n", StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println(error.getMessage());
            System.exit(2);
        }
    }
}
