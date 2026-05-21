// http://usaco.org/index.php?page=viewproblem2&cpid=512

import java.io.*;
import java.util.*;

class Main {
  static int A;
  static int B;
  static int N;
  static Cost[][] routes;
  static Cost[] dist;
  static boolean[] visited;
  static final int MAX_CITIES = 1001;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("cowroute.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    A = Integer.parseInt(st.nextToken());
    B = Integer.parseInt(st.nextToken());
    N = Integer.parseInt(st.nextToken());

    // initialize dist, visited
    dist = new Cost[MAX_CITIES];
    visited = new boolean[MAX_CITIES];

    // generate routes - routes[i][j] should store the minimum Cost of getting from city i to city j on a single route
    routes = new Cost[MAX_CITIES][MAX_CITIES];

    for (int i = 0; i < MAX_CITIES; i++) {
      for (int j = 0; j < MAX_CITIES; j++) {
        routes[i][j] = new Cost(Long.MAX_VALUE, Integer.MAX_VALUE);
      }
    }

    for (int i = 0; i < N; i++) {
      st = new StringTokenizer(br.readLine());
      int routeCost = Integer.parseInt(st.nextToken());
      int routeLen = Integer.parseInt(st.nextToken());

      int[] route = new int[routeLen];
      st = new StringTokenizer(br.readLine());
      for (int j = 0; j < routeLen; j++) {
        route[j] = Integer.parseInt(st.nextToken());
      }

      // update cost for each pair of cities along route
      for (int j = 0; j < routeLen; j++) {
        for (int k = j + 1; k < routeLen; k++) {
          routes[route[j]][route[k]] = Cost.min(routes[route[j]][route[k]], new Cost(routeCost, k - j));
        }
      }
    }

    br.close();

    // run Dijkstra's starting from city A
    dijkstra(A);

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("cowroute.out")));
    if (dist[B].routeLength > 1000) {
      pw.println("-1 -1");
    } else {
      pw.println(dist[B].cost + " " + dist[B].routeLength);
    }
    pw.close();
  }

  public static void dijkstra(int start) {
    // initialize dist, visited
    for (int i = 0; i < MAX_CITIES; i++) {
      dist[i] = new Cost(Long.MAX_VALUE/2, Integer.MAX_VALUE/2);
      visited[i] = false;
    }

    // initialize dist[start] to 0 so that the algorithm will pick this node first
    dist[start] = new Cost(0,0);

    while(true) {
      // find the smallest unvisited node in the graph
      int closest = -1;
      for (int i = 0; i < MAX_CITIES; i++) {
        if (!visited[i] && (closest == -1 || dist[i].compareTo(dist[closest]) < 1)) {
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
      for (int i = 0; i < MAX_CITIES; i++) {
        if (routes[closest][i].cost != Long.MAX_VALUE) {
          Cost newCost = new Cost(dist[closest].cost + routes[closest][i].cost, dist[closest].routeLength + routes[closest][i].routeLength);
          dist[i] = Cost.min(dist[i], newCost);
        }
      }
    }
  }
}

// the Cost object always stores a pair of the cost and the route length (i.e. number of cities traveled)
class Cost implements Comparable<Cost> {
  public long cost;
  public int routeLength;

  public Cost(long c, int l) {
    cost = c;
    routeLength = l;
  }

  public int compareTo(Cost c) {
    if (cost < c.cost) {
      return -1;
    } if (cost > c.cost) {
      return 1;
    } else {
      return routeLength - c.routeLength;
    }
  }

  public static Cost min(Cost a, Cost b) {
    return a.compareTo(b) < 0 ? a : b;
  }

  public String toString() {
    return "[" + cost + "," + routeLength + "]";
  }
}