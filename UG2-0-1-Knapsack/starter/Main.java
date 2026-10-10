import java.util.ArrayList;
import java.util.List;

// ADDED: native teaching demonstration; edit the small dataset in main, not an input file.
public class Main {
    record Result(int bestValue, List<Integer> indices) {}

    static void validateInput(int[] weights, int[] values, int capacity) {
        if (weights == null || values == null || weights.length != values.length) {
            throw new IllegalArgumentException("Weights and values must have equal lengths");
        }
        if (capacity < 0 || ((long) weights.length + 1) * ((long) capacity + 1) > 1000000) {
            throw new IllegalArgumentException("Use nonnegative capacity and at most 1000000 table cells");
        }
        long totalValue = 0;
        for (int i = 0; i < weights.length; i++) {
            if (weights[i] <= 0 || values[i] < 0) {
                throw new IllegalArgumentException("Weights must be positive and values nonnegative");
            }
            totalValue += values[i];
        }
        if (totalValue > Integer.MAX_VALUE) {
            throw new IllegalArgumentException("The sum of values must fit a Java int");
        }
    }

    static int[][] buildTable(int[] weights, int[] values, int capacity) {
        // TASK 1: Define dp[i][w], allocate its item/capacity dimensions and establish the zero bases.
        // TASK 2: Fill each row from the preceding item row, choosing skip or one legal take.
        throw new UnsupportedOperationException("Complete the table tasks");
    }

    static List<Integer> reconstruct(int[][] dp, int[] weights, int capacity) {
        // TASK 3: Compare the current optimum with the preceding row to decide whether to take an item.
        // TASK 4: Move to the preceding item after either choice; reduce capacity only when taking it.
        throw new UnsupportedOperationException("Complete the traceback tasks");
    }

    static Result solve(int[] weights, int[] values, int capacity) {
        // TASK 5: Combine the final table value and traceback indices into a Result without changing the inputs.
        throw new UnsupportedOperationException("Complete all five knapsack tasks before returning a result");
    }

    static void validateResult(Result result, int[] weights, int[] values, int capacity) {
        if (result == null || result.indices() == null || result.bestValue() < 0) {
            throw new IllegalArgumentException("Return a value and selected item indices");
        }
        boolean[] selected = new boolean[weights.length];
        long weight = 0;
        long value = 0;
        for (Integer index : result.indices()) {
            if (index == null || index < 0 || index >= weights.length || selected[index]) {
                throw new IllegalArgumentException("Selected indices must be distinct and in range");
            }
            selected[index] = true;
            weight += weights[index];
            value += values[index];
        }
        if (weight > capacity || value != result.bestValue()) {
            throw new IllegalArgumentException("Selected items must fit and attain the reported value");
        }
    }

    public static void main(String[] args) {
        try {
            if (args.length != 0) throw new IllegalArgumentException("This demonstration takes no arguments");
            int[] weights = {1, 3, 4, 5};
            int[] values = {1, 4, 5, 7};
            int capacity = 7;
            validateInput(weights, values, capacity);
            Result result = solve(weights, values, capacity);
            validateResult(result, weights, values, capacity);
            System.out.println("Max value: " + result.bestValue());
            System.out.println("Item indices in knapsack: " + result.indices());
        } catch (IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve the knapsack demonstration: " + error.getMessage());
            System.exit(2);
        }
    }
}
