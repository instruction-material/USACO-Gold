/*
A Dijkstra's demonstration.

The first line of the input contains two integers N and M, where N is the number of nodes and M is the number of edges.

The next M lines contain three integers each P, Q, and W, representing a bidirectional edge from P to Q of weight W.

The output should have N-1 lines, where the ith line is the shortest path from node 0 to node i, expressed as a list of indices. The last number should be the total weight/distance traveled.
*/

import java.io.*;
import java.util.*;

class Main {
  static int N;
  static int M;
  static int[] dist;
  static int[] prev;
  static boolean[] visited;
  static int[][] edge;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("dijkstra.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    N = Integer.parseInt(st.nextToken());
    M = Integer.parseInt(st.nextToken());

    // dist[i] is the minimum distance traveled from the start to node i
    dist = new int[N];

    // prev[i] is the index of the node that leads to node i in the optimal path
    prev = new int[N];

    // visited[i] tracks whether node i has been visited
    visited = new boolean[N];

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
      edge[a][b] = weight;
      edge[b][a] = weight;
    }

    // run Djikstra's starting at node 0 to fill dist, prev, visited
    dijkstra(0);

    // use dist and prev to traceback to find the optimal path and distance to each node
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("dijkstra.out")));

    for (int i = 1; i < N; i++) {
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
    // initialize dist, prev, visited
    for (int i = 0; i < N; i++) {
      dist[i] = Integer.MAX_VALUE;
      visited[i] = false;
      prev[i] = -1;
    }

    // initialize dist[start] to 0 so that the algorithm will pick this node first
    dist[start] = 0;

    while(true) {
      // find the unvisited node in the graph labeled with the smallest distance
      int closest = -1;
      for (int i = 0; i < N; i++) {
        if (!visited[i] && (closest == -1 || dist[i] < dist[closest])) {
          closest = i;
        }
      }

      // if closest == -1, then all nodes have been visited
      if (closest == -1) {
        break;
      }

      // mark this node as visited
      visited[closest] = true;

      // update the distances for all nodes connected to closest
      for (int i = 0; i < N; i++) {
        //make sure an edge exists
        if (edge[closest][i] != -1) {
          int newDist = dist[closest] + edge[closest][i];
          if (newDist < dist[i]) {
            dist[i] = newDist;
            prev[i] = closest;
          }
        }
      }
    }
  }
}