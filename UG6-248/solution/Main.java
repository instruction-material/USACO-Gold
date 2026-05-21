// http://www.usaco.org/index.php?page=viewproblem2&cpid=647

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("248.in"));
    int N = Integer.parseInt(br.readLine());
    
    int[] nums = new int[N];
    for (int i = 0; i < N; i++) {
      nums[i] = Integer.parseInt(br.readLine());
    }
    br.close();

    // DP approach: dp[i][j] stores the largest number that the interval that starts at index i and ends at index j (inclusive) is collapsable to 
    // if it is not collapsable to a single number, it is marked as 0
    int[][] dp = new int[N][N];
    int maxScore = 0;

    // base case: if you start and end at the same index, the best outcome is simply the number at that index
    for (int i = 0; i < N; i++) {
      dp[i][i] = nums[i];
      maxScore = Math.max(maxScore, dp[i][i]);
    }

    // now loop through the remaining interval lengths, checking each possible starting point
    for (int len = 2; len <= N; len++) {
      for (int start = 0; start <= N-len; start++) {
        int end = start + len - 1;

        // for the interval at start to end inclusive, check all the possible pairs of intervals that could potentially be merged
        // k will represent a pivot point that splits the interval into [start,k] and [k+1,end]
        int max = 0;
        for (int k = start; k < end; k++) {
          if (dp[start][k] == dp[k+1][end] && dp[start][k] != 0) {
            max = Math.max(max, dp[start][k]+1);
          }
        }

        dp[start][end] = max;
        maxScore = Math.max(maxScore, max);
      }
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("248.out")));
    pw.println(maxScore);
    pw.close();
  }
}