import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.StringTokenizer;

// ADDED: native Java; read feast.in and create feast.out only after the unfinished solver succeeds.
public class Main {
    record Input(int limit, int firstFruit, int secondFruit) {}

    static Input readInput(Path path) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
            String line = reader.readLine();
            if (line == null) throw new IllegalArgumentException("Missing T A B header");
            StringTokenizer tokens = new StringTokenizer(line);
            if (tokens.countTokens() != 3) throw new IllegalArgumentException("The header needs exactly three integers");
            int limit = Integer.parseInt(tokens.nextToken());
            int firstFruit = Integer.parseInt(tokens.nextToken());
            int secondFruit = Integer.parseInt(tokens.nextToken());
            if (limit < 1 || limit > 5000000) throw new IllegalArgumentException("1 <= T <= 5000000");
            if (firstFruit < 1 || secondFruit < 1 || firstFruit > limit || secondFruit > limit) {
                throw new IllegalArgumentException("Both fruit sizes must be between 1 and T");
            }
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) throw new IllegalArgumentException("Extra input after T A B");
            }
            return new Input(limit, firstFruit, secondFruit);
        }
    }

    static boolean[] reachableBeforeWater(Input input) {
        // TASK 1: Allocate one state per fullness from 0 through T and mark empty fullness reachable.
        // TASK 2: Process increasing fullness and add either fruit without exceeding T.
        throw new UnsupportedOperationException("Complete the before-water tasks");
    }

    static boolean[] seedAfterWater(boolean[] beforeWater) {
        // TASK 3: Seed after-water states with floor(fullness / 2) from every reachable before-water state.
        throw new UnsupportedOperationException("Complete the one-water transition task");
    }

    static int solve(Input input) {
        // TASK 4: Extend seeded after-water states by eating, without allowing a second water transition.
        // TASK 5: Find the greatest reachable fullness across both states because water is optional.
        throw new UnsupportedOperationException("Complete all five Fruit Feast tasks before producing an answer");
    }

    public static void main(String[] args) {
        try {
            if (args.length != 0) throw new IllegalArgumentException("The learner takes no arguments");
            Input input = readInput(Path.of("feast.in"));
            int answer = solve(input);
            if (answer < 0 || answer > input.limit()) throw new IllegalArgumentException("Answer is outside 0 through T");
            Files.writeString(Path.of("feast.out"), answer + "\n", StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve feast.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
