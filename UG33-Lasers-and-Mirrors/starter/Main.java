import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Set;
import java.util.StringTokenizer;

public final class Main {
    static final class Input {
        final int laserX;
        final int laserY;
        final int barnX;
        final int barnY;
        final int[][] posts;

        Input(int laserX, int laserY, int barnX, int barnY, int[][] posts) {
            this.laserX = laserX;
            this.laserY = laserY;
            this.barnX = barnX;
            this.barnY = barnY;
            this.posts = posts;
        }
    }

    static int minimumMirrors(Input input) {
        // TASK 1: Model horizontal and vertical lines with separate identities.
        // TASK 2: Add each post as an edge between its two line identities.
        // TASK 3: Seed both laser lines at distance zero and run breadth-first search.
        // TASK 4: Return the first reachable barn-line distance, or -1 after exhaustion.
        throw new UnsupportedOperationException("The mirror search is unfinished.");
    }

    static int xLine(int x) {
        return -x - 1;
    }

    static int yLine(int y) {
        return y;
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

    private static long pointKey(int x, int y) {
        return ((long) x << 32) | y;
    }

    static Input readInput(String text) {
        StringTokenizer tokens = new StringTokenizer(text);
        int count = integer(tokens, 1, 100_000);
        int laserX = integer(tokens, 0, 1_000_000_000);
        int laserY = integer(tokens, 0, 1_000_000_000);
        int barnX = integer(tokens, 0, 1_000_000_000);
        int barnY = integer(tokens, 0, 1_000_000_000);
        Set<Long> seen = new HashSet<>();
        seen.add(pointKey(laserX, laserY));
        seen.add(pointKey(barnX, barnY));
        int[][] posts = new int[count][2];
        for (int i = 0; i < count; i++) {
            posts[i][0] = integer(tokens, 0, 1_000_000_000);
            posts[i][1] = integer(tokens, 0, 1_000_000_000);
            if (!seen.add(pointKey(posts[i][0], posts[i][1]))) {
                throw new IllegalArgumentException("Posts must have distinct locations.");
            }
        }
        if (tokens.hasMoreTokens()) {
            throw new IllegalArgumentException("Unexpected trailing input.");
        }
        return new Input(laserX, laserY, barnX, barnY, posts);
    }

    public static void main(String[] args) {
        try {
            Input input = readInput(Files.readString(Path.of("lasers.in"), StandardCharsets.UTF_8));
            int answer = minimumMirrors(input);
            if (answer < -1 || answer > input.posts.length) {
                throw new IllegalArgumentException("The answer must be -1 or a possible mirror count.");
            }
            Files.writeString(Path.of("lasers.out"), answer + "\n", StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println(error.getMessage());
            System.exit(2);
        }
    }
}
