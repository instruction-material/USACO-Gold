// http://usaco.org/index.php?page=viewproblem2&cpid=669

import java.io.*;
import java.util.*;

class Main {
  static int N;
  static int[] x, y;
  static int[] dist;
  static boolean[] visited;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("moocast.in"));
    
    N = Integer.parseInt(br.readLine());
    
    x = new int[N];
    y = new int[N];

    for (int i = 0; i < N; i++) {
      StringTokenizer st = new StringTokenizer(br.readLine());
      x[i] = Integer.parseInt(st.nextToken());
      y[i] = Integer.parseInt(st.nextToken());
    }

    br.close();

    // initialize dist, visited
    dist = new int[N];
    visited = new boolean[N];

    // run Prim's, keeping track of the longest edge in the MST as we go (keep track of the squared distances since that is the amount we have to spend)
    long maxEdge = prim(0);

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("moocast.out")));
    pw.println(maxEdge);
    pw.close();
  }

  public static int prim(int start) {
    int maxEdge = 0;
    
    // initialize dist, visited
    for (int i = 0; i < N; i++) {
      dist[i] = Integer.MAX_VALUE;
      visited[i] = false;
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

      // if dist[closest] has never been updated, then MST cannot be completed
      if (dist[closest] == Long.MAX_VALUE) {
        return -1;
      }

      // mark this node as visited
      visited[closest] = true;

      // update minCost with the weight of closest
      maxEdge = Math.max(maxEdge, dist[closest]);

      // update the distances for all nodes connected to closest, but make sure the distance is at least C
      for (int i = 0; i < N; i++) {
        if (!visited[i]) {
          int newDist = (x[closest]-x[i]) * (x[closest]-x[i]) + (y[closest]-y[i]) * (y[closest]-y[i]);
          if (newDist < dist[i]) {
            dist[i] = newDist;
          }
        }
      }
    }

    return maxEdge;
  }
}