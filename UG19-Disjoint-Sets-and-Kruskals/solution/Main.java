import java.io.*;
import java.util.*;

class Main {
  static int N, M;
  static ArrayList<Edge> edges;
  static ArrayList<Edge> mst;

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new FileReader("kruskal.in"));

    StringTokenizer st = new StringTokenizer(br.readLine());
    N = Integer.parseInt(st.nextToken());
    M = Integer.parseInt(st.nextToken());

    // create list of edges
    edges = new ArrayList<>();
    for (int i = 0; i < M; i++) {
      st = new StringTokenizer(br.readLine());
      int a = Integer.parseInt(st.nextToken());
      int b = Integer.parseInt(st.nextToken());
      int len = Integer.parseInt(st.nextToken());
      edges.add(new Edge(a, b, len));
    }

    br.close();

    // run Kruskal's
    mst = new ArrayList<Edge>();
    Kruskal();

    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("kruskal.out")));

    // print all edges in MST
    for (Edge e : mst) {
      pw.println(e.p + " " + e.q);
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

    public String toString() {
      String parentStr = "";
      for (int num : parent) {
        parentStr += num + " ";
      }

      String weightStr = "";
      for (int num : weight) {
        weightStr += num + " ";
      }

      return "parent: " + parentStr + "\nweight: " + weightStr + "\ncount: " + count + "\n";
    }
  }

  static class Edge implements Comparable<Edge> {
    public int p, q;
    public int weight;
    public Edge(int p, int q, int w) {
      this.p = p;
      this.q = q;
      this.weight = w;
    }
    public int compareTo(Edge other) {
      return weight - other.weight;
    }
  }

  public static void Kruskal() {
    // sort edges in increasing length
    Collections.sort(edges);

    // initialize DisjointSets with N nodes
    DisjointSets ds = new DisjointSets(N);
    
    // iterate through increasingly large edges, until graph is connected (i.e. it is composed of one connected component)
    System.out.println(ds);
    for (Edge e : edges) {
      if (!ds.connected(e.p, e.q)) {
        ds.connect(e.p, e.q);
        mst.add(e);
        System.out.println("edge: " + e.p + ", " + e.q);
        System.out.println(ds);
      }

      //check if done
      if (ds.count() == 1) break;
    }
  }
}