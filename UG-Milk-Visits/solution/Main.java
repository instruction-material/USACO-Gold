// http://usaco.org/index.php?page=viewproblem2&cpid=970

import java.io.*;
import java.util.*;

class Main {
  static int[] T;
  static ArrayList<ArrayList<Integer>> adj;
  static int[][] queries;
  static ArrayList<ArrayList<Integer>> queriesAdj;

  static int[] pre, post;
  static HashSet<Integer> visited;
  static int counter;

  static ArrayList<Integer> path;
  static ArrayList<ArrayList<Integer>> farmsByCowType;
  static int[] depth;
  static boolean[] answer;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("milkvisits.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int M = Integer.parseInt(st.nextToken());

    // T[i] type of the cow in the ith farm
    T = new int[N];
    st = new StringTokenizer(br.readLine());
    for (int i = 0; i < N; i++) {
      T[i] = Integer.parseInt(st.nextToken()) - 1;
    }

    // adj is an adjacency list of the farms
    adj = new ArrayList<ArrayList<Integer>>();
    for (int i = 0; i < N; i++) {
      adj.add(new ArrayList<Integer>());
    }

    for (int i = 0; i < N-1; i++) {
      st = new StringTokenizer(br.readLine());
      int x = Integer.parseInt(st.nextToken()) - 1;
      int y = Integer.parseInt(st.nextToken()) - 1;
      adj.get(x).add(y);
      adj.get(y).add(x);
    }

    // queries[i] contains [A,B,C], where A and B are the endpoints of the query and C is the cow type desired
    // queriesAdj[i] is an ArrayList of query index in queries that endpoint i is part of
    queries = new int[M][3];
    queriesAdj = new ArrayList<ArrayList<Integer>>();
    for (int i = 0; i < N; i++) {
      queriesAdj.add(new ArrayList<Integer>());
    }

    for (int i = 0; i < M; i++) {
      st = new StringTokenizer(br.readLine());
      int A = Integer.parseInt(st.nextToken()) - 1;
      int B = Integer.parseInt(st.nextToken()) - 1;
      int C = Integer.parseInt(st.nextToken()) - 1;

      queries[i][0] = A;
      queries[i][1] = B;
      queries[i][2] = C;

      queriesAdj.get(A).add(i);
      queriesAdj.get(B).add(i);
    }
    
    br.close();

    // we run DFS first to generate the pre and post arrays, which help us determine whether one node is an ancestor of another. more here: https://www.geeksforgeeks.org/printing-pre-and-post-visited-times-in-dfs-of-a-graph/

    pre = new int[N];
    post = new int[N];
    visited = new HashSet<Integer>();
    counter = 0;
    
    DFS(0);

    // in this problem, we can actually solve all of the queries by running a rather complex version of DFS once.
    // for each node we visit, we look at all queries that involve this node as an endpoint
    // for each query, we look at the last node (using farmsByCowType) where we saw the cow type desired by this query. we'll call this node lastNodeWithDesiredType
    // we now have currNode, which is the current node in DFS, otherEndpoint, which is the other endpoint of this query, and lastNodeWithDesiredType. logically, starting at currNode, if we go back up the traveled path, if otherEndpoint lies in the graph at or somewhere after we pass lastNodeWithDesiredType, then between currNode and otherEndpoint, we have to see our desired type.
    // thus, starting from the root, go to the node right after lastNodeWithDesiredType. we'll call this node "next." if next is an ancestor of otherEndpoint, then we know otherEndpoint branches off from the graph before we get to lastNodeWithDesiredType, so we may never see our desired type. however, if next is not an ancestor of otherEndpoint, then otherEndpoint must branch off from the current path in a way that guarantees we see our desired type, as described in the previous paragraph.

    // path keeps track of the farm ids on the current path we are on in our traversal
    path = new ArrayList<Integer>();

    // farmsByCowType[i] stores a list of the farm ids on the current path that have cow type i
    farmsByCowType = new ArrayList<ArrayList<Integer>>();
    for (int i = 0; i < N; i++) {
      farmsByCowType.add(new ArrayList<Integer>());
    }

    // depth[i] keeps track of how many nodes deep we are on the current path for node i
    depth = new int[N];

    // clear our visited HashSet to prepare for a new DFS
    visited.clear();

    // answer[i] stores true or false for query i
    answer = new boolean[M];

    DFS2(0);

    // write output
    PrintWriter pw = new PrintWriter("milkvisits.out");
    for (int i = 0; i < M; i++) {
      pw.print(answer[i] ? 1 : 0);
    }
    pw.println();
    pw.close();
  }

  static void DFS(int x) {
    visited.add(x);

    // store the pre number whenever the node comes into recursion stack 
    pre[x] = counter;
    counter++;
    
    for (int y : adj.get(x)) {
      if (!visited.contains(y)) {
        DFS(y);
      }
    }

    // store the post number whenever the node goes out of recursion stack 
    post[x] = counter;
    counter++;
  }

  // checks if x is an ancestor of y
  static boolean isAncestor(int x, int y) {
    return pre[x] <= pre[y] && post[x] >= post[y];
  }

  static void DFS2(int currNode) {
    visited.add(currNode);

    // update path and farmsByCowType
    path.add(currNode);
    farmsByCowType.get(T[currNode]).add(currNode);

    // iterate over all queries that involve this node as an endpoint
    for (int q : queriesAdj.get(currNode)) {
      int target = queries[q][2];

      // only proceed if we have seen at least one farm with this target type
      int count = farmsByCowType.get(target).size();
      if (count > 0) {
        int lastNodeWithDesiredType = farmsByCowType.get(target).get(count-1);

        if (lastNodeWithDesiredType == currNode) {
          answer[q] = true;
        } else {
          int next = path.get(depth[lastNodeWithDesiredType]+1);
          int otherEndpoint;
          if (currNode == queries[q][0]) {
            otherEndpoint = queries[q][1];
          } else {
            otherEndpoint = queries[q][0];
          }

          if (!isAncestor(next, otherEndpoint)) {
            answer[q] = true;
          }
        }
      }
    }

    for (int y : adj.get(currNode)) {
      if (!visited.contains(y)) {
        depth[y] = depth[currNode] + 1;
        DFS2(y);
      }
    }

    // update path and farmsByCowType
    path.remove(path.size()-1);
    farmsByCowType.get(T[currNode]).remove(farmsByCowType.get(T[currNode]).size()-1);
  }
}