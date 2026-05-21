// http://usaco.org/index.php?page=viewproblem2&cpid=718

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("nocross.in"));

    // store the cows by breed ID on the top and on the bottom
    int N = Integer.parseInt(br.readLine());
    int[] top = new int[N];
    for (int i = 0; i < N; i++) {
      top[i] = Integer.parseInt(br.readLine());
    }

    int[] bottom = new int[N];
    for (int i = 0; i < N; i++) {
      bottom[i] = Integer.parseInt(br.readLine());
    }
    br.close();

    // dp[i][j] represents the max number of crosswalks we could draw between the i leftmost fields on top and the j leftmost fields on bottom
    int[][] dp = new int[N][N];

    // initialize dp[0][all] and dp[all][0] first
    dp[0][0] = canDrawCrosswalk(top[0], bottom[0]);

    // move across all of the top fields, while only looking at first bottom field
    for (int i = 1; i < N; i++) {
      dp[i][0] = Math.max(dp[i-1][0], canDrawCrosswalk(top[i], bottom[0]));
    }

    // move across all of the bottom fields, while only looking at first top field
    for (int i = 1; i < N; i++) {
      dp[0][i] = Math.max(dp[0][i-1], canDrawCrosswalk(top[0], bottom[i]));
    }

    // iterate over all pairs i,j (note that iterating through in this order works because the crosswalks cannot cross each other)
    for (int i = 1; i < N; i++) {
      for (int j = 1; j < N; j++) {
        // calculate what dp[i][j] would be if we could make a new connection between i and j
        int val = dp[i-1][j-1] + canDrawCrosswalk(top[i], bottom[j]);

        // take the max of val, dp[i-1][j], and dp[i][j-1]
        dp[i][j] = Math.max(Math.max(dp[i-1][j], dp[i][j-1]), val);
      }
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("nocross.out")));
    pw.println(dp[N-1][N-1]);
    pw.close();
  }

  //returns 1 if a and b are friendly, 0 otherwise
  static int canDrawCrosswalk(int a, int b) {
    if (Math.abs(a - b) <= 4) {
      return 1;
    }
    return 0;
  }
}