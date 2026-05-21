// http://usaco.org/index.php?page=viewproblem2&cpid=694

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("hps.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int K = Integer.parseInt(st.nextToken());

    int[] moves = new int[N];
    for (int i = 0; i < N; i++) {
      String move = br.readLine();
      if (move.equals("H")) {
        moves[i] = 0;
      } else if (move.equals("P")) {
        moves[i] = 1;
      } else {
        moves[i] = 2;
      }
    }
    br.close();

    // use DP to memoize all the possible maximum number of games Bessie could have won across NxKx3. dp[i][j][k] is the maximum number of games Bessie could have won after playing i games with j switches using the kth gesture
    int dp[][][] = new int[N+1][K+1][3];

    // note that we start with i=1 because 0 games yields 0 wins
    for (int i = 1; i <= N; i++) {
      for (int j = 0; j <= K; j++) {
        for (int gesture = 0; gesture < 3; gesture++) {
          int increment = 0;
          if (moves[i-1] == gesture) {
            increment = 1;
          }

          // if j = 0, there is just one gesture throughout, so just calculate wins based on this one gesture
          if (j == 0) {
            dp[i][j][gesture] = dp[i-1][j][gesture] + increment;
          }
          
          // otherwise, we look at the best outcome if we either stick with the current gesture (so looking at the jth switch using the kth gesture) or we switch gestures (so looking at the j-1th switch using one of the other two gestures)
          // in other words, at every new game, we can either preserve the switch we made last time or consider what would happen if we switched this time instead
          else {
            int otherGesture1 = (gesture + 1) % 3;
            int otherGesture2 = (gesture + 2) % 3;

            dp[i][j][gesture] = Math.max(Math.max(dp[i-1][j][gesture], dp[i-1][j-1][otherGesture1]),dp[i-1][j-1][otherGesture2]) + increment;
          }
        }
      }
    }

    // the answer is the max of the possibilities after N games and K switches
    int answer = Math.max(Math.max(dp[N][K][0], dp[N][K][1]), dp[N][K][2]);
    System.out.println(answer);

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("hps.out")));
    pw.println(answer);
    pw.close();
  }
}

/*

P = 1
P = 1
H = 0
P = 1
S = 2

       0 switch | 1 switch
         H,P,S  |  H,P,S
Game 0: [0,0,0]   [0,0,0]
Game 1: [0,1,0]   [0,1,0]
Game 2: [0,2,0]   [1,2,1]
Game 3: [1,2,0]   [3,2,2]
Game 4: [1,3,0]   [3,3,2]
Game 5: [1,3,1]   [3,3,4]

the number in the DP array is the max number of current wins where the current gesture is now H, P, or S (but previously could have been something else)

*/