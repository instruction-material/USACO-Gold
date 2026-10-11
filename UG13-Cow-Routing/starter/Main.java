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
        final int start, destination;
        final int[] prices;
        final int[][] stops;
        Input(int start, int destination, int[] prices, int[][] stops) {
            this.start = start; this.destination = destination;
            this.prices = prices; this.stops = stops;
        }
    }
    static final class Result {
        final long money;
        final int flights;
        Result(long money, int flights) { this.money = money; this.flights = flights; }
    }
    static Input readInput() throws IOException {
        InputReader reader = new InputReader("cowroute.in");
        int a = reader.take(1, 1000), b = reader.take(1, 1000);
        int n = reader.take(1, 1000);
        int[] prices = new int[n];
        int[][] stops = new int[n][];
        for (int route = 0; route < n; route++) {
            prices[route] = reader.take(1, 1000000000);
            int length = reader.take(1, 100);
            stops[route] = new int[length];
            boolean[] seen = new boolean[1001];
            for (int i = 0; i < length; i++) {
                int city = reader.take(1, 1000);
                if (seen[city]) throw new IllegalArgumentException("A route repeats a city");
                seen[city] = true; stops[route][i] = city;
            }
        }
        reader.finish();
        return new Input(a, b, prices, stops);
    }
    static Result cheapestJourney(Input input) {
        // TODO 1: Encode every forward ticket portion and retain its best pair.
        // TODO 2: Compare and add money/flights pairs; never add an unreachable sentinel.
        // TODO 3: Initialize all distances and settle state, including a zero start pair.
        // TODO 4: Settle and relax with the pair ordering; distinguish an unreachable destination.
        throw new UnsupportedOperationException("Complete ordered-route shortest paths before producing an answer");
    }
    static String output(Input input, Result result) {
        if (result == null) throw new IllegalArgumentException("Missing result pair");
        if (result.money == -1 && result.flights == -1) {
            if (input.start == input.destination) throw new IllegalArgumentException("The start is reachable from itself");
            return "-1 -1\n";
        }
        if (result.money < 0 || result.money > 999000000000L || result.flights < 0 || result.flights > 999) {
            throw new IllegalArgumentException("Result pair outside feasible bounds");
        }
        if (input.start == input.destination && (result.money != 0 || result.flights != 0)) {
            throw new IllegalArgumentException("A journey to the start needs the zero pair");
        }
        if (input.start != input.destination && (result.money == 0 || result.flights == 0)) {
            throw new IllegalArgumentException("A reachable distinct destination needs positive money and flights");
        }
        return result.money + " " + result.flights + "\n";
    }
    public static void main(String[] args) {
        try {
            Input input = readInput();
            String answer = output(input, cheapestJourney(input));
            Files.writeString(Path.of("cowroute.out"), answer, StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve cowroute.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
