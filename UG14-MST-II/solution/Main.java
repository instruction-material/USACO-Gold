/*
Prim's, using a priority queue to find the unvisited node in the graph labeled with the smallest value.
*/

import java.io.*;
import java.util.*;
import java.awt.Point;

/**
 * @brief Solve the lesson problem using the provided input and output format
 */
class Main {
    static int N;
    static int M;
    static int[] dist;
    static int[] prev;
    static boolean[] visited;
    static int[][] edge;

    /**
   * @brief Read input, compute the answer, and write output
   *
   * @param args Command-line arguments
   */
    public static void main(String[] args) throws IOException {
        // read input
        BufferedReader br = new BufferedReader(new FileReader("prim.in"));
        StringTokenizer st = new StringTokenizer(br.readLine());
        N = Integer.parseInt(st.nextToken());
        M = Integer.parseInt(st.nextToken());

        dist = new int[N];
        prev = new int[N];
        visited = new boolean[N];
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
            if (edge[a][b] == -1 || weight < edge[a][b]) { // CHANGED: keep the cheapest parallel edge.
                edge[a][b] = weight;
                edge[b][a] = weight;
            }
        }

        br.close(); // ADDED: input is complete.

        // run Prim's starting at node 0 to fill dist, prev, visited
        prim(0);
        for (boolean reached : visited) { // ADDED: refuse a disconnected graph before opening output.
            if (!reached) throw new IllegalArgumentException("A connected graph is required");
        }

        // use prev to traceback to find the MST
        PrintWriter pw =
            new PrintWriter(new BufferedWriter(new FileWriter("prim.out")));

        long totalDist = 0; // CHANGED: a tree total can exceed int.

        for (int i = 1; i < N; i++) {
            pw.println(i + " " + prev[i]);
            totalDist += edge[i][prev[i]];
        }

        pw.println("Total Distance: " + totalDist);
        pw.close();
    }

    public static void prim(int start) {
        // initialize dist, prev, visited
        for (int i = 0; i < N; i++) {
            dist[i] = Integer.MAX_VALUE;
            visited[i] = false;
            prev[i] = -1;
        }

        // initialize dist[start] to 0 so that the algorithm will pick this node first
        dist[start] = 0;

        // initialize PriorityQueue, which will hold pairs of (nodeValue, nodeId)
        PriorityQueue<Point> pq = new PriorityQueue<>(new Comparator<Point>() {
            public int compare(Point a, Point b) {
                return a.x == b.x ? Integer.compare(a.y, b.y) : Integer.compare(a.x, b.x); // CHANGED: compare keys directly.
            }
        });
        pq.add(new Point(0, start));

        while (!pq.isEmpty()) {
            // find the unvisited node in the graph labeled with the smallest distance
            int currDist = pq.peek().x;
            int currNode = pq.peek().y;
            pq.poll();
            if (visited[currNode]) continue; // ADDED: stale entries must not rescan a row.

            visited[currNode] = true;

            // update the distances for all nodes connected to closest. note that in Prim's, instead of updating each node with the cumulative distance, we label each neighboring unvisited node with simply the weight of the path connected to it.
            for (int i = 0; i < N; i++) {
                //make sure an edge exists
                if (edge[currNode][i] != -1 && !visited[i]) {
                    int newDist = edge[currNode][i];
                    if (newDist < dist[i]) {
                        dist[i] = newDist;
                        prev[i] = currNode;
                        pq.add(new Point(newDist, i));
                    }
                }
            }
        }
    }
}
