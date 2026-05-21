// http://usaco.org/index.php?page=viewproblem2&cpid=861

import java.io.*;
import java.util.*;
import java.awt.Point;

class Main {
  static int N, M, K;
  static int[] dist;
  static List<Map<Integer, Integer>> adj;
  static List<Bale> bales;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("dining.in"));

    StringTokenizer st = new StringTokenizer(br.readLine());
    N = Integer.parseInt(st.nextToken());
    M = Integer.parseInt(st.nextToken());
    K = Integer.parseInt(st.nextToken());

    dist = new int[N+1];

    // fill adjacency list adj, where an ArrayList of HashMaps, where the element index in the ArrayList in the given pasture, and for each HashMap, the key is the pasture that element is connected to, and value is the the time for traversal
    adj = new ArrayList<>();
    for (int i = 0; i <= N; i++) {
      adj.add(new HashMap<>());
    }
    for (int i = 0; i < M; i++) {
      st = new StringTokenizer(br.readLine());
      int a = Integer.parseInt(st.nextToken()) - 1;
      int b = Integer.parseInt(st.nextToken()) - 1;
      int c = Integer.parseInt(st.nextToken());
      
      adj.get(a).put(b, c);
      adj.get(b).put(a, c);
    }

    // fill list of haybales
    bales = new ArrayList<>();
    for (int i = 0; i < K; i++) {
      st = new StringTokenizer(br.readLine());
      int a = Integer.parseInt(st.nextToken()) - 1;
      int b = Integer.parseInt(st.nextToken());
      
      bales.add(new Bale(a, b));
    }
    br.close();

    // in this problem, we first run Run Dijkstra’s with the final pasture (i.e. the barn) as the endpoint. this gives us the optimal path for every pasture to the barn
    dijkstra(N-1);

    // now, we clone the dist array to save for comparison later, and we modify the graph such that for each pasture containing a haybale, we add a new edge between that pasture and a new "fake" final node, where the distance is equal to the previously computed distance to the barn from that pasture, minus its tastiness value
    // the reason we need this "fake" final node N is to account for the case where the cow gets to the end, then goes back to another haybale, then goes back to the end
    int[] initDist = dist.clone();

    for (Bale b : bales) {
      // note that we only add one edge going from the fake final node to each haybale to prevent cycles
      adj.get(N).put(b.loc, dist[b.loc] - b.yum);
    }

    // run Dijkstra's again, this time starting at the fake final node
    dijkstra(N);

    // for each cow, output 1 if the new distance <= initial distance, otherwise 0 (if the cow can't reach the end while passing through a haybale, its dist wil be INF, and if it costs more for it to pass through a haybale than to not, then its dist will be larger than the initDist)
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("dining.out")));

    for (int i = 0; i < N-1; i++) {
      pw.println(dist[i] <= initDist[i] ? 1 : 0);
    }

    pw.close();
  }

  public static void dijkstra(int start) {
    // initialize dist
    for (int i = 0; i < N; i++) {
      dist[i] = Integer.MAX_VALUE;
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

      // calculate new distances
      for (Integer i : adj.get(currNode).keySet()) {
        int newDist = dist[currNode] + adj.get(currNode).get(i);
        if (newDist < dist[i]) {
          dist[i] = newDist;
          pq.add(new Point(newDist, i));
        }
      }
    }
  }

  static class Bale {
    int loc, yum;

    public Bale(int l, int y) {
        loc = l;
        yum = y;
    }
  }
}