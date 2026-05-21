// http://www.usaco.org/index.php?page=viewproblem2&cpid=622

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("cbarn2.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int K = Integer.parseInt(st.nextToken());

    long[] cows = new long[N];
    for (int i = 0; i < N; i++) {
      cows[i] = Long.parseLong(br.readLine());
    }
    br.close();

    // in this problem, dp[i][j] represents the minimum distance the cows have to walk if we unlock i doors, with the leftmost door at j, and ONLY taking into account cows that need to end up anywhere at door j or to the right
    // this means we have to look at i = k and j = 0 to get the solution
    // furthermore, we also have to build the dp array for every possible linearization of the barn, and compare all of the dp[k][0] values to find the minimum one

    long[][] dp = new long[K+1][N+1];
    long answer = Integer.MAX_VALUE;

    // the outermost loop rotates through the linearizations, so the variable start represents the index that is the leftmost door in this linearization
    for (int start = 0; start < N; start++) {

      // reset DP array to Integer.MAX_VALUEs, but dp[0][N] = 0
      for (int i = 0; i <= K; i++) {
        for (int j = 0; j <= N; j++) {
          dp[i][j] = Integer.MAX_VALUE;
        }
      }
      dp[0][N] = 0;

      // loop through the number of doors placed
      for (int i = 1; i <= K; i++) {

        // loop through the placement of the leftmost door
        for (int j = 0; j < N; j++) {

          long sum = 0;

          // at each leftmost door, we have to consider a previous state where i is one less, and j is any of the positions to its right. picking one of these previous states (let's say it's at door d), the additional distance we have to add is the total distance all of the cows that start between j and d-1
          // this additional distance is stored as a running sum in sum

          // loop through each of the doors to the right of j
          for (int d = j+1; d <= N; d++) {

            // update sum by the number of cows at door d, times the distance they have to travel to get to j
            sum += cows[(d-1+start) % N] * (d-j-1);

            // so sum + dp[i-1][j] represents the total distance if we add this new leftmost door at j, and all of the cows up to door d go into that door, and the rest of the cows are handled by the dp[i-1][d] state
            dp[i][j] = Math.min(dp[i][j], sum + dp[i-1][d]);
          }

        }
      }

      // update answer if dp[K][0] is smaller than the existing value. here, dp[K][0] represents the shortest total distance if there is a door placed at index start and no cows cross through start
      answer = Math.min(answer, dp[K][0]);
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("cbarn2.out")));
    pw.println(answer);
    pw.close();
  }
}