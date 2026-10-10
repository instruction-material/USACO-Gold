import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.StringTokenizer;

/** Authored Gold setup checkpoint: input contract and 64-bit output. */
class Main {
    static long calculateTotal(int[] values) {
        // TASK: use a 64-bit accumulator and add each value to the total.
        throw new UnsupportedOperationException(
            "Complete the setup total task before producing an answer");
    }

    public static void main(String[] args) {
        try {
            Tokens input = new Tokens();
            int count = (int) input.number("N", 0, 200000);
            int[] values = new int[count];
            for (int i = 0; i < count; i++) {
                values[i] = (int) input.number("value " + i, -1000000000, 1000000000);
            }
            if (input.next() != null) throw new IllegalArgumentException("Extra input");
            System.out.println(calculateTotal(values));
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve setup input: " + error.getMessage());
            System.exit(2);
        }
    }

    static class Tokens {
        final BufferedReader reader = new BufferedReader(
            new InputStreamReader(System.in, StandardCharsets.UTF_8));
        StringTokenizer tokens = new StringTokenizer("");

        String next() throws IOException {
            while (!tokens.hasMoreTokens()) {
                String line = reader.readLine();
                if (line == null) return null;
                tokens = new StringTokenizer(line);
            }
            return tokens.nextToken();
        }

        long number(String label, long minimum, long maximum) throws IOException {
            String token = next();
            if (token == null) throw new IllegalArgumentException("Missing " + label);
            long value;
            try {
                value = Long.parseLong(token);
            } catch (NumberFormatException error) {
                throw new IllegalArgumentException("Invalid integer for " + label);
            }
            if (value < minimum || value > maximum) {
                throw new IllegalArgumentException("Out-of-range " + label);
            }
            return value;
        }
    }
}
