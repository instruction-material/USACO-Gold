// http://usaco.org/index.php?page=viewproblem2&cpid=899

import java.io.*;
import java.util.*;
import java.awt.Point;

class Main {
  static int N;
  static int M;
  static int T;
  static int[] dist;
  static int[] prev;
  static ArrayList<Point>[] adj;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("shortcut.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    N = Integer.parseInt(st.nextToken());
    M = Integer.parseInt(st.nextToken());
    T = Integer.parseInt(st.nextToken());

    int[] numCows = new int[N];
    st = new StringTokenizer(br.readLine());

    for (int i = 0; i < N; i++) {
      numCows[i] = Integer.parseInt(st.nextToken());
    }

    // adjacency list: adj[p] contains and ArrayList of (q,w) pairs (i.e. p is connected to q with weight w)
    adj = new ArrayList[N];

    for (int i = 0; i < N; i++) {
      adj[i] = new ArrayList<Point>();
    }

    for (int i = 0; i < M; i++) {
      st = new StringTokenizer(br.readLine());
      int p = Integer.parseInt(st.nextToken())-1;
      int q = Integer.parseInt(st.nextToken())-1;
      int w = Integer.parseInt(st.nextToken());

      //add edge to adjacency list
      adj[p].add(new Point(w, q));
      adj[q].add(new Point(w, p));
    }

    br.close();

    // dist[i] is the minimum distance traveled from the start to node i
    dist = new int[N];

    // prev[i] is the index of the node that leads to node i in the optimal path
    prev = new int[N];

    // run Djikstra's starting at node 0 to fill dist, prev
    dijkstra(0);

    // the key to this problem is to find the number of cows that ever pass through each node. then, we can test creating a shortcut from each node straight to the barn with weight T. we can do this by tracing back every optimal path and incrementing for each field we pass through (we have to look at numCows to see how many cows are actually traveling).

    long[] numCowsThroughField = new long[N];
    for (int i = 0; i < N; i++) {
      for (int j = i; j != -1; j = prev[j]) {
        numCowsThroughField[j] += numCows[i];
      }
    }

    // now that we know how many cows passed through each node, the distance we could save is: the difference between the total distance the cows passing through this node would have had to travel and T, multiplied by the number of cows that passed through the node

    long maxSaved = 0;
    for (int i = 0; i < N; i++) {
      long distSaved = numCowsThroughField[i] * ((long)dist[i] - (long)T);
      maxSaved = Math.max(maxSaved, distSaved);
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("shortcut.out")));
    pw.println(maxSaved);
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

      // update the distances for all nodes connected to closest
      for (Point p : adj[currNode]) {
        int newNode = p.y;
        int newDist = currDist + p.x;
        if (newDist < dist[newNode]) {
          dist[newNode] = newDist;
          prev[newNode] = currNode;
          pq.add(new Point(newDist, newNode));
        }
        // account for case of a tie, as described by problem
        else if (newDist == dist[newNode]) {
          if (currNode < prev[newNode]) {
              dist[newNode] = newDist;
              prev[newNode] = currNode;
              pq.add(new Point(newDist, newNode));
          }
        }
      }
    }
  }
}