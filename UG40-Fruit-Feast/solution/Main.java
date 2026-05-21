// http://usaco.org/index.php?page=viewproblem2&cpid=574

import java.io.*;
import java.util.*;

public class Main {
  public static void main(String[] args) throws IOException {

    // read input
    BufferedReader br = new BufferedReader(new FileReader("feast.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int T = Integer.parseInt(st.nextToken());
    int A = Integer.parseInt(st.nextToken());
    int B = Integer.parseInt(st.nextToken());
    br.close();

    // in this problem, we construct a boolean DP array with T rows and 2 columns.
    // col 1 = no water. we iterate through all possible values of fullness up to T. for a given fullness value t, if t-A or t-B was achievable, then this is also achieveable, because we just have to eat one more lemon or orange.
    // col 2 = with water. we again iterate through all possible values of fullnes up to T. however, for a given fullness value t, if the fullness without water at t/2 or t/2-1 was achieveable, then this is also achieveable, because we just have to drink water.

    boolean[][] dp = new boolean[T+1][2];
    dp[0][0] = true;
    
    // iterate through without water and then with water
    for (int i = 0; i < 2; i++) {

      // iterate through fullness values
      for (int t = 0; t <= T; t++) {

        // check t-A
        if (t-A >= 0) {
          if (dp[t-A][i]) {
            dp[t][i] = true;
          }
        }

        // check t-B
        if (t-B >= 0) {
          if (dp[t-B][i]) {
            dp[t][i] = true;
          }
        }

        // if i == 1, try drinking water
        if (i == 1) {
          System.out.println(t);
          if (t*2 <= T) {
            if (dp[t*2][0]) {
              dp[t][i] = true;
            }
          }

          if (t*2+1 <= T) {
            if (dp[t*2+1][0]) {
              dp[t][i] = true;
            }
          }
        }
      }
    }

    // find maximum fullness by iterating backward through t, starting from T
    int answer = 0;
    for (int t = T; t >= 0; t--) {
      if (dp[t][0] || dp[t][1]) {
        answer = t;
        break;
      }
    }

    // write output
    PrintWriter pw = new PrintWriter("feast.out");
    pw.println(answer);
    pw.close();
  }
}