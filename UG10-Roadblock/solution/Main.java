// http://usaco.org/index.php?page=viewproblem2&cpid=398

import java.io.*;
import java.util.*;
import java.awt.Point;

class Main {
  static int N;
  static int M;
  static int[] dist;
  static int[] prev;
  static int[][] edges;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("rblock.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    N = Integer.parseInt(st.nextToken());
    M = Integer.parseInt(st.nextToken());

    edges = new int[N][N];

    // initialize with -1 first (indicates unconnected nodes)
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            edges[i][j] = -1;
        }
    }

    for (int i = 0; i < M; i++) {
      st = new StringTokenizer(br.readLine());
      int a = Integer.parseInt(st.nextToken());
      int b = Integer.parseInt(st.nextToken());
      int weight = Integer.parseInt(st.nextToken());
      edges[a-1][b-1] = weight;
      edges[b-1][a-1] = weight;
    }

    br.close();

    // dist[i] is the minimum distance traveled from the start to node i
    dist = new int[N];

    // prev[i] is the index of the node that leads to node i in the optimal path
    prev = new int[N];

    // run Dijkstra's starting at node 0 to fill dist, prev
    int minDist = dijkstra(0, N-1);
    int newDist = minDist;

    // store the current shortest path from node 0 to node N-1
    ArrayList<Integer> path = new ArrayList<>();
    for (int i = N-1; i != -1; i = prev[i]) {
      path.add(i);
    }

    // try to double each edge weight along path and re-run Dijkstra's
    for (int i = 0; i < path.size()-1; i++) {
      int a = path.get(i);
      int b = path.get(i+1);

      edges[a][b] *= 2;
      edges[b][a] *= 2;

      newDist = Math.max(newDist, dijkstra(0,N-1));

      edges[a][b] /= 2;
      edges[b][a] /= 2;
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("rblock.out")));
    pw.println(newDist-minDist);
    pw.close();
  }

  public static int dijkstra(int start, int end) {
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

      // update the distances for all nodes connected to closest
      for (int i = 0; i < N; i++) {
        //make sure an edge exists
        if (edges[currNode][i] != -1) {
          int newDist = dist[currNode] + edges[currNode][i];
          if (newDist < dist[i]) {
            dist[i] = newDist;
            prev[i] = currNode;
            pq.add(new Point(newDist, i));
          }
        }
      }
    }

    // return the shortest distance between start and end
    return dist[end];
  }
}