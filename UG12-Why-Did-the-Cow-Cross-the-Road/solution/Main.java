// http://usaco.org/index.php?page=viewproblem2&cpid=717

import java.io.*;
import java.util.*;

class Main {
  static int N;
  static int T;
  static int[][] fields;
  static int[][] dist;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("visitfj.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    N = Integer.parseInt(st.nextToken());
    T = Integer.parseInt(st.nextToken());

    fields = new int[N][N];

    for (int i = 0; i < N; i++) {
      st = new StringTokenizer(br.readLine());
      for (int j = 0; j < N; j++) {
        fields[i][j] = Integer.parseInt(st.nextToken());
      }
    }

    br.close();

    // dist[i][j] is the minimum distance traveled from the start to field i,j
    dist = new int[N][N];

    // run Djikstra's starting at top left field to fill dist. the general idea here is that each time we are considering a node (i.e. a field), we only consider its neighbors as the fields that are exactly three steps away. once we are less than three steps away from the bottom right field, we calculate the final distance it would take to travel there.
    int minTime = dijkstra();

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("visitfj.out")));
    pw.println(minTime);
    pw.close();
  }

  public static int dijkstra() {
    // initialize dist
    for (int i = 0; i < N; i++) {
      for (int j = 0; j < N; j++) {
        dist[i][j] = Integer.MAX_VALUE;
      }
    }

    // initialize dist[0][0] to 0 so that the algorithm will pick this node first
    dist[0][0] = 0;

    // initialize PriorityQueue, which will hold int[] of (nodeValue, nodeRowIndex, nowColIndex)
    PriorityQueue<int[]> pq = new PriorityQueue<>(new Comparator<int[]>() {
      public int compare(int[] a, int[] b) {
        return a[0]-b[0];
      }
    });
    int[] temp = {0,0,0};
    pq.add(temp);

    int minDist = Integer.MAX_VALUE;

    while(!pq.isEmpty()) {
      // find the unvisited node in the graph labeled with the smallest distance
      int currDist = pq.peek()[0];
      int currRowIndex = pq.peek()[1];
      int currColIndex = pq.peek()[2];
      pq.poll();

      // if we are less than three steps away from the bottom right field, update minDist
      int distToEnd = (N-1-currRowIndex) + (N-1-currColIndex);

      if (distToEnd < 3) {
        minDist = Math.min(minDist, currDist + distToEnd * T);
      }
      
      // try moving three steps away from the current field in all possible directions. don't forget to include the options where the cow goes forward two steps in one direction and then backward one step in the opposite direction

      int[] optX = {-3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, -1, 1, 0, 0};
      int[] optY = {0, -1, 1, -2, 2, -3, 3, -2, 2, -1, 1, 0, 0, 0, -1, 1};
      for (int i = 0; i < optX.length; i++) {
        int newRowIndex = currRowIndex + optX[i];
        int newColIndex = currColIndex + optY[i];

        // make sure new location is in bounds
        if (newRowIndex >= 0 && newRowIndex < N && newColIndex >= 0 && newColIndex < N) {

          // calculate new distance
          int newDist = currDist + fields[newRowIndex][newColIndex] + 3*T;
          if (newDist < dist[newRowIndex][newColIndex]) {
            dist[newRowIndex][newColIndex] = newDist;
            int[] temp2 = {newDist, newRowIndex, newColIndex};
            pq.add(temp2);
          }
        }
      }
    }

    return minDist;
  }
}


// 2. create the adjacency matrix. from that, pick a root note and run BFS so we construct the tree (i.e. each node has a parent). for each query, find ancestors and find the least common ancestor. then we can traverse the shortest path and answer the query
// ignore multinode case for now (requires compressing single parent nodes into one node, but then how do you only check for cows after a given node?)

// 3. start with length of K, at each transition either add 1 more of that letter, or add another K of a different letter. pre-compute cost to transition from a letter to another using floyd-marshalls

// for large N, for every letter, precompute the cost of changing an interval to that letter with a prefix sum array. this means we can calculate the cost of changing an interval of the string to a certain letter to O(1)