// http://usaco.org/index.php?page=viewproblem2&cpid=946

import java.io.*;
import java.util.*;

class Main {
  static int N, K;
  static long[] dist;
  static boolean[] visited;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("walk.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    
    N = Integer.parseInt(st.nextToken());
    K = Integer.parseInt(st.nextToken());

    br.close();

    // initialize dist, visited
    dist = new long[N];
    visited = new boolean[N];

    // run Prim's, getting a list of the edges in the MST back
    ArrayList<Long> edges = prim(0);

    // M is simply the Kth largest value of the edges in the MST
    Collections.sort(edges);

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("walk.out")));
    pw.println(edges.get(N-(K-1)));
    pw.close();
  }

  public static ArrayList<Long> prim(int start) {
    // initialize dist, visited
    for (int i = 0; i < N; i++) {
      dist[i] = Long.MAX_VALUE;
      visited[i] = false;
    }

    ArrayList<Long> edges = new ArrayList<Long>(N);

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

      // update ArrayList of edges
      edges.add(dist[closest]);

      // update the distances for all nodes connected to closest
      for (int i = 0; i < N; i++) {
        if (!visited[i] && i != closest) {
          long x = Math.min(i, closest) + 1;
          long y = Math.max(i, closest) + 1;
          long newDist = (2019201913 * x + 2019201949 * y) % 2019201997;
          if (newDist < dist[i]) {
              dist[i] = newDist;
          }
        }
      }
    }

    return edges;
  }

}