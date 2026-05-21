// http://usaco.org/index.php?page=viewproblem2&cpid=789

import java.io.*;
import java.util.*;

class Main {
  static int N, Q;

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new FileReader("mootube.in"));

    StringTokenizer st = new StringTokenizer(br.readLine());
    N = Integer.parseInt(st.nextToken());
    Q = Integer.parseInt(st.nextToken());

    // each edge is a relevance connection between two videos
    // note: make sure the video indices are 0-indexed because N represents the number of videos and the DisjointSets class assumes N nodes
    ArrayList<Edge> edges = new ArrayList<>();
    for (int i = 0; i < N-1; i++) {
      st = new StringTokenizer(br.readLine());
      int p = Integer.parseInt(st.nextToken()) - 1;
      int q = Integer.parseInt(st.nextToken()) - 1;
      int r = Integer.parseInt(st.nextToken());
      edges.add(new Edge(p, q, r));
    }

    // sort the edges from largest to smallest relevance
    Collections.sort(edges);

    // read in each query
    ArrayList<Query> queries = new ArrayList<>();
    for (int i = 0; i < Q; i++) {
      st = new StringTokenizer(br.readLine());
      int k = Integer.parseInt(st.nextToken());
      int v = Integer.parseInt(st.nextToken()) - 1;
      queries.add(new Query(k, v, i));
    }

    // sort the queries from largest to smallest K
    Collections.sort(queries);

    br.close();

    // in this problem, we go through the queries one by one, sorted from largest to smallest K. each time, we add all of the edges to our graph (using the DisjointSets class) which have weight of at least K. then, to answer a given query, we check how many videos are now connected to it in our graph.

    int[] answers = new int[Q];
    int edgeIndex = 0;  // used to iterate through edges list
    DisjointSets ds = new DisjointSets(N);

    for (Query q : queries) {
      // add all edges with weight at least K

      while (edgeIndex < edges.size() && edges.get(edgeIndex).weight >= q.k) {
        ds.connect(edges.get(edgeIndex).p, edges.get(edgeIndex).q);
        edgeIndex++;
      }

      // the answer to this query is the number of videos/nodes now connected to the given video, minus one for the original video
      answers[q.index] = ds.size(q.v) - 1;
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("mootube.out")));

    for (int answer : answers) {
      pw.println(answer);
    }
    pw.close();
  }

  static class DisjointSets {
    // parent[i] represents the parent node of node i
    private int[] parent;

    // weight[i] represents the total number of nodes in the tree below node i
    private int[] weight;

    // count represents the number of distinct components
    private int count;

    public DisjointSets(int n) {
      // all nodes start out as disconnected, so 
      // count = n, parent[i] = i, weight[i] = 1
      count = n;
      parent = new int[n];
      weight = new int[n];
      for (int i = 0; i < n; i++) {
        parent[i] = i;
        weight[i] = 1;
      }
    }

    public int count() {
      return count;
    }

    // find root of given node ("find")
    private int root(int p) {
      while (p != parent[p]) {
        p = parent[p];
      }
      return p;
    }

    // connect two nodes ("union")
    // to do this, we get the roots of both. if the roots are already the same, then they are already connected. otherwise, we add the tree with less weight to the tree with more weight, by updating the parents and the weight
    public void connect(int p, int q) {
      int rootP = root(p);
      int rootQ = root(q);
      
      if (rootP == rootQ) return;

      // add tree with less weight to tree with more weight
      if (weight[rootP] < weight[rootQ]) {
        parent[rootP] = rootQ;
        weight[rootQ] += weight[rootP];
      } else {
        parent[rootQ] = rootP;
        weight[rootP] += weight[rootQ];
      }

      // reduce number of components by one
      count--;
    }

    // check if two nodes are connected
    // to do this, we simply check if the roots of both are the same
    public boolean connected(int p, int q) {
      return root(p) == root(q);
    }

    // return size of component containing given node
    public int size(int p) {
      return weight[root(p)];
    }
  }

  static class Edge implements Comparable<Edge> {
    public int p, q;
    public int weight;
    public Edge(int p, int q, int weight) {
      this.p = p;
      this.q = q;
      this.weight = weight;
    }

    // comparator sorts from largest to smallest relevance (weight)
    public int compareTo(Edge other) {
      return other.weight - weight;
    }
  }

  static class Query implements Comparable<Query> {
    public int k, v, index;

    public Query(int k, int v, int index) {
      this.k = k;
      this.v = v;
      this.index = index;
    }

    // comparator sorts from largest to smallest K
    public int compareTo(Query other) {
      return other.k - k;
    }
  }
}