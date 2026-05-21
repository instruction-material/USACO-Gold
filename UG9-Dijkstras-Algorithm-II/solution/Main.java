/*

Dijkstra's, using a priority queue to find the unvisited node in the graph labeled with the smallest distance. This runs in O(NlogN).

*/

import java.io.*;
import java.util.*;
import java.awt.Point;

class Main {
  static int N;
  static int M;
  static int[] dist;
  static int[] prev;
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

    // run Djikstra's starting at node 0 to fill dist, prev
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
    // initialize dist, prev
    for (int i = 0; i < N; i++) {
      dist[i] = Integer.MAX_VALUE;
      prev[i] = -1;
    }

    // initialize dist[start] to 0 so that the algorithm will pick this node first
    dist[start] = 0;

    // initialize PriorityQueue, which will hold pairs of (nodeValue, nodeId)
    PriorityQueue<Point> pq = new PriorityQueue<>(new Comparator<Point>() {
      public int compare(Point a, Point b) {
        return a.x == b.x ? a.y - b.y : a.x - b.x;
      }
    });
    pq.add(new Point(0, start));

    while(!pq.isEmpty()) {
      // find the unvisited node in the graph labeled with the smallest distance
      int currDist = pq.peek().x;
      int currNode = pq.peek().y;
      pq.poll();

      // since values in priority queues cannot be modified when relaxing edges, we need to make sure it is still the minimum distance so that we do not waste time looping through edges (which can time out on certain problems/test cases)
      if(dist[currNode] < currDist) continue; 

      // update the distances for all nodes connected to closest
      for (int i = 0; i < N; i++) {
        //make sure an edge exists
        if (edge[currNode][i] != -1) {
          int newDist = dist[currNode] + edge[currNode][i];
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