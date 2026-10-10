/*

// CHANGED: Matrix Dijkstra with a lazy queue. For N vertices and M input records,
// time is O(M + N^2 log N + P), where P is the number of printed path vertices.
// See README.md for the nonnegative-weight teaching contract and representation comparison.

*/

import java.io.*;
import java.util.*;


/**
 * @brief Solve the lesson problem using the provided input and output format
 */
class Main {
    static int N;
    static int M;
    static long[] dist; // CHANGED: path totals can exceed int.
    static int[] prev;
    static int[][] edge;

    // ADDED: Queue keys retain 64-bit distances and compare without subtraction.
    static class State implements Comparable<State> {
        final long distance;
        final int node;
        State(long distance, int node) {
            this.distance = distance;
            this.node = node;
        }
        public int compareTo(State other) {
            int order = Long.compare(distance, other.distance);
            return order != 0 ? order : Integer.compare(node, other.node);
        }
    }

    /**
   * @brief Read input, compute the answer, and write output
   *
   * @param args Command-line arguments
   */
    public static void main(String[] args) throws IOException {
        // read input
        BufferedReader br = new BufferedReader(new FileReader("dijkstra.in"));
        StringTokenizer st = new StringTokenizer(br.readLine());
        N = Integer.parseInt(st.nextToken());
        M = Integer.parseInt(st.nextToken());

        // dist[i] is the minimum distance traveled from the start to node i
        dist = new long[N]; // CHANGED

        // prev[i] is the index of the node that leads to node i in the optimal path
        prev = new int[N];

        // edge[a][b] is the weight from node a to node b
        // initialize with -1 first (indicates unconnected nodes)
        edge = new int[N][N];

        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                edge[i][j] = -1;
            }
        }

        for (int i = 0; i < M; i++) {
            st = new StringTokenizer(br.readLine());
            int a = Integer.parseInt(st.nextToken());
            int b = Integer.parseInt(st.nextToken());
            int weight = Integer.parseInt(st.nextToken());
            // CHANGED: Preserve the cheapest parallel edge, regardless of record order.
            if (edge[a][b] == -1 || weight < edge[a][b]) {
                edge[a][b] = weight;
                edge[b][a] = weight;
            }
        }

        br.close(); // ADDED: input is fully read before writing the answer.

        // run Dijkstra's starting at node 0 to fill dist, prev
        dijkstra(0);

        // use dist and prev to traceback to find the optimal path and distance to each node
        PrintWriter pw =
            new PrintWriter(new BufferedWriter(new FileWriter("dijkstra.out")));

        for (int i = 1; i < N; i++) {
            // ADDED: An unreachable vertex has no path to trace.
            if (dist[i] == Long.MAX_VALUE) {
                pw.println("Unreachable: " + i);
                continue;
            }
            ArrayList<Integer> path = new ArrayList<>();

            // retrace path
            for (int curr = i; curr != -1; curr = prev[curr]) {
                path.add(curr);
            }

            // write path to output
            for (int j = path.size() - 1; j >= 0; j--) {
                pw.print(path.get(j) + " ");
            }

            // write distance to output
            pw.print("Distance: " + dist[i]);

            pw.println();
        }

        pw.close();
    }

    public static void dijkstra(int start) {
        // initialize dist, prev
        for (int i = 0; i < N; i++) {
            dist[i] = Long.MAX_VALUE; // CHANGED
            prev[i] = -1;
        }

        // initialize dist[start] to 0 so that the algorithm will pick this node first
        dist[start] = 0;

        // initialize PriorityQueue, which will hold pairs of (nodeValue, nodeId)
        PriorityQueue<State> pq = new PriorityQueue<>(); // CHANGED
        pq.add(new State(0, start)); // CHANGED

        while (!pq.isEmpty()) {
            // find the unvisited node in the graph labeled with the smallest distance
            long currDist = pq.peek().distance; // CHANGED
            int currNode = pq.peek().node; // CHANGED
            pq.poll();

            // since values in priority queues cannot be modified when relaxing edges, we need to make sure it is still the minimum distance so that we do not waste time looping through edges (which can time out on certain problems/test cases)
            if (dist[currNode] < currDist)
                continue;

            // update the distances for all nodes connected to closest
            for (int i = 0; i < N; i++) {
                //make sure an edge exists
                if (edge[currNode][i] != -1) {
                    long newDist = dist[currNode] + edge[currNode][i]; // CHANGED
                    if (newDist < dist[i]) {
                        dist[i] = newDist;
                        prev[i] = currNode;
                        pq.add(new State(newDist, i)); // CHANGED
                    }
                }
            }
        }
    }
}
