// http://www.usaco.org/index.php?page=viewproblem2&cpid=531

import java.io.*;
import java.util.*;

class Main {
  static int N;
  static int[] teams;
  static long[] dist;
  static boolean[] visited;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("superbull.in"));

    N = Integer.parseInt(br.readLine());
    teams = new int[N];

    for (int i = 0; i < N; i++) {
      teams[i] = Integer.parseInt(br.readLine());
    }

    br.close();

    // initialize dist, visited
    dist = new long[N];
    visited = new boolean[N];

    // run Prim's starting from any vertex - the key is to negate the weights since we are looking for the maximum spanning tree instead of the minimum. Prim's fits this problem, because we are simply looking for a way to connect every team (as each team must play in at least one game) that results in the maximum total points
    long maxPoints = prim(0);

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("superbull.out")));
    pw.println(maxPoints);
    pw.close();
  }

  public static long prim(int start) {
    long maxPoints = 0;
    
    // initialize dist, visited
    for (int i = 0; i < N; i++) {
      dist[i] = Long.MAX_VALUE;
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

      // mark this node as visited
      visited[closest] = true;

      // update maxPoints with the weight of closest
      maxPoints -= dist[closest];

      // update the distances for all nodes connected to closest
      for (int i = 0; i < N; i++) {
        if (!visited[i]) {
          long newDist = -(teams[closest] ^ teams[i]);
          if (newDist < dist[i]) {
            dist[i] = newDist;
          }
        }
      }
    }

    return maxPoints;
  }
}