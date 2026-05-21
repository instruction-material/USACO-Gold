/*
A Prim's demonstration.

The first line of the input contains two integers N and M, where N is the number of nodes and M is the number of edges.

The next M lines contain three integers each P, Q, and W, representing a bidirectional edge from P to Q of weight W.

The output should have N-1 lines, where the ith line is an edge in the resulting MST.
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
      edge[a][b] = weight;
      edge[b][a] = weight;
    }

    // run Prim's starting at node 0 to fill dist, prev, visited
    prim(0);

    // use prev to traceback to find the MST
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("prim.out")));

    int totalDist = 0;

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

      // update the distances for all nodes connected to closest. note that in Prim's, instead of updating each node with the cumulative distance, we label each neighboring unvisited node with simply the weight of the path connected to it.
      for (int i = 0; i < N; i++) {
        //make sure an edge exists
        if (edge[closest][i] != -1 && !visited[i]) {
          int newDist = edge[closest][i];
          if (newDist < dist[i]) {
            dist[i] = newDist;
            prev[i] = closest;
          }
        }
      }
    }
  }
}