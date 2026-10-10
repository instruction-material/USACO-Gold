import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

/** Native practice driver. Complete the BinaryIndexedTree helpers below. */
public class Main {
    private static final int LIMIT = 200_000;
    private static final long VALUE_LIMIT = 1_000_000_000L;
    private enum Operation { ADD, PREFIX, RANGE }
    private record Command(Operation operation, int left, int right, long delta) {}
    private record Input(long[] values, Command[] commands) {}

    public static void main(String[] args) {
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(System.in, StandardCharsets.UTF_8))) {
            if (args.length != 0) {
                throw new IllegalArgumentException("Read the practice input from standard input");
            }
            Input input = readInput(reader);
            BinaryIndexedTree bit = new BinaryIndexedTree(input.values().length);
            bit.load(input.values());
            StringBuilder answer = new StringBuilder();
            for (Command command : input.commands()) {
                switch (command.operation()) {
                    case ADD -> bit.add(command.delta(), command.left());
                    case PREFIX -> answer.append(bit.sum(command.left())).append('\n');
                    case RANGE -> answer.append(bit.rangeSum(command.left(), command.right())).append('\n');
                }
            }
            // Print only after all input and operations have succeeded.
            System.out.print(answer);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException exception) {
            System.err.println("Cannot solve Fenwick input: " + exception.getMessage());
            System.exit(2);
        }
    }

    private static Input readInput(BufferedReader reader) throws IOException {
        String[] header = tokens(reader, "N Q");
        requireCount(header, 2, "N Q");
        int n = (int) bounded(header[0], 1, LIMIT, "N");
        int q = (int) bounded(header[1], 0, LIMIT, "Q");
        String[] initial = tokens(reader, "initial values");
        requireCount(initial, n, "initial values");
        long[] values = new long[n];
        for (int i = 0; i < n; i++) {
            values[i] = bounded(initial[i], -VALUE_LIMIT, VALUE_LIMIT, "initial value");
        }
        Command[] commands = new Command[q];
        for (int i = 0; i < q; i++) {
            String[] fields = tokens(reader, "operation " + (i + 1));
            switch (fields[0]) {
                case "ADD" -> {
                    requireCount(fields, 3, "ADD index delta");
                    int index = (int) bounded(fields[1], 0, n - 1, "ADD index");
                    long delta = bounded(fields[2], -VALUE_LIMIT, VALUE_LIMIT, "ADD delta");
                    commands[i] = new Command(Operation.ADD, index, index, delta);
                }
                case "PREFIX" -> {
                    requireCount(fields, 2, "PREFIX index");
                    int index = (int) bounded(fields[1], -1, n - 1, "PREFIX index");
                    commands[i] = new Command(Operation.PREFIX, index, index, 0);
                }
                case "RANGE" -> {
                    requireCount(fields, 3, "RANGE left right");
                    int left = (int) bounded(fields[1], 0, n - 1, "RANGE left");
                    int right = (int) bounded(fields[2], 0, n - 1, "RANGE right");
                    if (left > right) {
                        throw new IllegalArgumentException("RANGE requires left <= right");
                    }
                    commands[i] = new Command(Operation.RANGE, left, right, 0);
                }
                default -> throw new IllegalArgumentException("Unknown operation: " + fields[0]);
            }
        }
        String extra;
        while ((extra = reader.readLine()) != null) {
            if (!extra.isBlank()) {
                throw new IllegalArgumentException("Extra input after Q operations");
            }
        }
        return new Input(values, commands);
    }

    private static String[] tokens(BufferedReader reader, String name) throws IOException {
        String line = reader.readLine();
        if (line == null || line.isBlank()) {
            throw new IllegalArgumentException("Missing " + name);
        }
        return line.trim().split("\\s+");
    }

    private static void requireCount(String[] fields, int expected, String name) {
        if (fields.length != expected) {
            throw new IllegalArgumentException("Expected " + expected + " fields for " + name);
        }
    }

    private static long bounded(String token, long minimum, long maximum, String name) {
        final long value;
        try {
            value = Long.parseLong(token);
        } catch (NumberFormatException exception) {
            throw new IllegalArgumentException("Expected an integer for " + name);
        }
        if (value < minimum || value > maximum) {
            throw new IllegalArgumentException(name + " is outside the practice bounds");
        }
        return value;
    }
}

/** Complete the four tasks while retaining the supplied input driver and guards. */
class BinaryIndexedTree {
    private final long[] A;

    public BinaryIndexedTree(int n) {
        if (n < 1) throw new IllegalArgumentException("The tree needs at least one value");
        A = new long[n + 1];
    }

    private int LSB(int i) {
        return i & -i;
    }

    public void load(long[] values) {
        if (values.length != A.length - 1) throw new IllegalArgumentException("Wrong initial length");
        // TASK 1: Clear the tree, then add each original value at its zero-based index.
        throw unfinished();
    }

    public void add(long delta, int i) {
        requireIndex(i);
        // TASK 2: Convert i to an internal slot, add delta, then jump upward with LSB.
        throw unfinished();
    }

    public long sum(int i) {
        if (i < -1 || i >= A.length - 1) throw new IllegalArgumentException("Invalid prefix index");
        // TASK 3: Convert i to an internal slot; accumulate while jumping downward with LSB.
        throw unfinished();
    }

    public long rangeSum(int left, int right) {
        requireIndex(left);
        requireIndex(right);
        if (left > right) throw new IllegalArgumentException("Invalid closed range");
        // TASK 4: Subtract the prefix ending before left from the prefix ending at right.
        throw unfinished();
    }

    private void requireIndex(int i) {
        if (i < 0 || i >= A.length - 1) throw new IllegalArgumentException("Invalid update/range index");
    }

    private UnsupportedOperationException unfinished() {
        return new UnsupportedOperationException("Complete the four Fenwick tasks before producing an answer");
    }
}
