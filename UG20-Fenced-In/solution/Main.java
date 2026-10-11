// http://usaco.org/index.php?page=viewproblem2&cpid=623

import java.io.*;
import java.util.*;

/**
 * @brief Solve the lesson problem using the provided input and output format
 */
class Main {
    static int A, B, N, M;
    static int[] verticalFences, horizontalFences;
    // CHANGED: Store each weight and construction index in one primitive key.
    static long[] edges;

    /**
   * @brief Read input, compute the answer, and write output
   *
   * @param args Command-line arguments
   */
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("fencedin.in"));

        StringTokenizer st = new StringTokenizer(br.readLine());
        A = Integer.parseInt(st.nextToken());
        B = Integer.parseInt(st.nextToken());
        N = Integer.parseInt(st.nextToken());
        M = Integer.parseInt(st.nextToken());

        // note that we pad these arrays with 0 at the beginning and the final index at the end so that we can take the difference between adjacent elements later on in order to calculate the lengths of the fence segments
        verticalFences = new int[N + 2];
        for (int i = 0; i < N; i++) {
            verticalFences[i + 1] = Integer.parseInt(br.readLine());
        }
        verticalFences[N + 1] = A;

        horizontalFences = new int[M + 2];
        for (int i = 0; i < M; i++) {
            horizontalFences[i + 1] = Integer.parseInt(br.readLine());
        }
        horizontalFences[M + 1] = B;

        br.close();

        // in this problem, the nodes are each individual enclosed region and the edges are the fence segments between each region. we keep the same edges in a primitive array. each edge weight is the difference between two adjacent elements in verticalFences or horizontalFences

        // sort these arrays so we can take differences of adjacent elements
        Arrays.sort(verticalFences);
        Arrays.sort(horizontalFences);

        // CHANGED: At most 8,004,000 keys, without millions of Edge objects.
        edges = new long[(N + 1) * M + (M + 1) * N];
        int edgeIndex = 0;

        // get the horizontal edges by looking at verticalFences
        for (int i = 0; i < N + 1; i++) {
            for (int j = 0; j < M; j++) {
                int weight = verticalFences[i + 1] - verticalFences[i];
                edges[edgeIndex] = ((long) weight << 32) | edgeIndex;
                edgeIndex++;
            }
        }

        // get the vertical edges by looking at horizontalFences
        for (int j = 0; j < M + 1; j++) {
            for (int i = 0; i < N; i++) {
                int weight = horizontalFences[j + 1] - horizontalFences[j];
                edges[edgeIndex] = ((long) weight << 32) | edgeIndex;
                edgeIndex++;
            }
        }

        // now, we simply have to construct the MST, and the MST will represent the shortest total distance of fencing we need to remove in order to ensure there is a path to get to all of the enclosed regions

        long minDist = Kruskal();

        // write output
        PrintWriter pw =
            new PrintWriter(new BufferedWriter(new FileWriter("fencedin.out")));
        pw.println(minDist);
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

            if (rootP == rootQ)
                return;

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
    }

    public static long Kruskal() {
        // sort edges in increasing length
        // CHANGED: Positive weights occupy the high 32 bits, so key order is weight order.
        Arrays.sort(edges);

        // initialize DisjointSets with N nodes
        DisjointSets ds = new DisjointSets((N + 1) * (M + 1));

        long minDist = 0;

        // iterate through increasingly large edges, until graph is connected (i.e. it is composed of one connected component)

        int horizontalEdgeCount = (N + 1) * M;
        for (long e : edges) {
            // CHANGED: Recover the original endpoints from the construction index.
            int index = (int) e;
            int p, q;
            if (index < horizontalEdgeCount) {
                // This branch has no edges when M is zero.
                int i = index / M, j = index % M;
                p = i + j * (N + 1);
                q = p + N + 1;
            } else {
                // This branch has no edges when N is zero.
                index -= horizontalEdgeCount;
                int j = index / N, i = index % N;
                p = i + j * (N + 1);
                q = p + 1;
            }

            if (!ds.connected(p, q)) {
                ds.connect(p, q);
                minDist += e >>> 32; // CHANGED: Recover the weight into the existing long total.
            }

            // check if done
            if (ds.count() == 1)
                break;
        }

        return minDist;
    }
}
