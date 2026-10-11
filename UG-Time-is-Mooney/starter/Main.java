// ADDED: Optional Gold bounded-time graph-DP learner pack. Complete four solve tasks.
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

class Main {
    static class Problem {
        final int[] money;
        final int[][] edges;
        final int cost;
        Problem(int[] money, int[][] edges, int cost) {
            this.money = money;
            this.edges = edges;
            this.cost = cost;
        }
    }

    static int[] record(BufferedReader reader, int length) throws IOException {
        String line = reader.readLine();
        if (line == null || line.isBlank()) throw new IllegalArgumentException("Missing record");
        String[] words = line.trim().split("\\s+");
        if (words.length != length) throw new IllegalArgumentException("Wrong record length");
        int[] values = new int[length];
        for (int i = 0; i < length; i++) values[i] = Integer.parseInt(words[i]);
        return values;
    }

    static Problem readProblem(Path input) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(input, StandardCharsets.UTF_8)) {
            int[] header = record(reader, 3);
            int n = header[0], m = header[1], cost = header[2];
            if (n < 2 || n > 1000 || m < 1 || m > 2000 || cost < 1 || cost > 1000) {
                throw new IllegalArgumentException("Use 2..1000 cities, 1..2000 roads and cost 1..1000");
            }
            int[] money = record(reader, n);
            for (int reward : money) {
                if (reward < 0 || reward > 1000) throw new IllegalArgumentException("City rewards must be 0..1000");
            }
            if (money[0] != 0) throw new IllegalArgumentException("City 1 reward must be zero");
            int[][] edges = new int[m][2];
            for (int i = 0; i < m; i++) {
                int[] edge = record(reader, 2);
                if (edge[0] < 1 || edge[0] > n || edge[1] < 1 || edge[1] > n || edge[0] == edge[1]) {
                    throw new IllegalArgumentException("Road endpoints must be distinct cities in 1..N");
                }
                edges[i][0] = edge[0] - 1;
                edges[i][1] = edge[1] - 1;
            }
            for (String extra; (extra = reader.readLine()) != null;) {
                if (!extra.isBlank()) throw new IllegalArgumentException("Unexpected extra record");
            }
            return new Problem(money, edges, cost);
        }
    }

    static int solve(Problem problem) {
        // TODO 1: Derive a sufficient day limit from reward <= 1000 and cost >= 1.
        // TODO 2: Initialize reachable day/city states; day 0 starts at city 0 with reward 0.
        // TODO 3: Use a new day layer for directed-edge transitions, adding the arrival reward.
        // TODO 4: Consider only returns to city 0; subtract cost * day * day and retain no-trip 0.
        throw new UnsupportedOperationException("Complete the four Time is Mooney graph-DP tasks");
    }

    public static void main(String[] args) {
        try {
            if (args.length != 0) throw new IllegalArgumentException("No command-line arguments expected");
            Problem problem = readProblem(Path.of("time.in"));
            int answer = solve(problem);
            if (answer < 0) throw new IllegalArgumentException("The no-trip option guarantees a nonnegative answer");
            // Finish validation and the learner algorithm before opening the answer file.
            Files.writeString(Path.of("time.out"), answer + "\n", StandardCharsets.UTF_8);
        } catch (IOException | IllegalArgumentException | UnsupportedOperationException error) {
            System.err.println("Cannot solve time.in: " + error.getMessage());
            System.exit(2);
        }
    }
}
