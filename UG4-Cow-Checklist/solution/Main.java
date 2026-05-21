// http://usaco.org/index.php?page=viewproblem2&cpid=670

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("checklist.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int H = Integer.parseInt(st.nextToken());
    int G = Integer.parseInt(st.nextToken());

    int[][] holsteins = new int[H][2];
    int[][] guernseys = new int[G][2];
    
    for (int i = 0; i < H; i++) {
      st = new StringTokenizer(br.readLine());
      holsteins[i][0] = Integer.parseInt(st.nextToken());
      holsteins[i][1] = Integer.parseInt(st.nextToken());
    }

    for (int i = 0; i < G; i++) {
      st = new StringTokenizer(br.readLine());
      guernseys[i][0] = Integer.parseInt(st.nextToken());
      guernseys[i][1] = Integer.parseInt(st.nextToken());
    }

    br.close();

    // use DP to keep track of the min energy required to have seen the ith Holstein and jth Guernsey cow. in each cell, the first number represents that state ending at a Holstein, and the second number represents that state ending at a Guernsey.
    int[][][] dp = new int[H+1][G+1][2];

    // fill with Integer.MAX_VALUE since we are looking for mins
    for (int i = 0; i <= H; i++) {
      for (int j = 0; j <= G; j++) {
        for (int k = 0; k < 2; k++) {
          dp[i][j][k] = Integer.MAX_VALUE;
        }
      }
    }

    // FJ always starts at the first Holstein
    dp[1][0][0] = 0;

    // fill in first col (j=0)
    for (int i = 2; i <= H; i++) {
      dp[i][0][0] = dp[i-1][0][0] + energy(holsteins[i-2], holsteins[i-1]);
    }

    // ignore first row (i=0) since you cannot visit any Guernseys with 0 Holsteins, since FJ always starts at the first Holstein

    // dp[1][1][1] is the distance from the first Holstein to the first Guernsey
    dp[1][1][1] = energy(holsteins[0], guernseys[0]);

    // fill in second row (i=1)
    for (int j = 2; j <= G; j++) {
      dp[1][j][1] = dp[1][j-1][1] + energy(guernseys[j-2], guernseys[j-1]);
    }

    for (int i = 2; i <= H; i++) {
      for (int j = 1; j <= G; j++) {
        // dp[i][j][0] is the minimum of coming from the previous Holstein or the previous Guernsey, and ending at a Holstein
        int fromHolstein = Integer.MAX_VALUE;
        if (dp[i-1][j][0] != Integer.MAX_VALUE) {
          fromHolstein = dp[i-1][j][0] + energy(holsteins[i-2], holsteins[i-1]);
        }
        int fromGuernsey = Integer.MAX_VALUE;
        if (dp[i-1][j][1] != Integer.MAX_VALUE) {
          fromGuernsey = dp[i-1][j][1] + energy(guernseys[j-1], holsteins[i-1]);
        }
        dp[i][j][0] = Math.min(fromHolstein, fromGuernsey);

        // dp[i][j][1] is the minimum of coming from the previous Holstein or the previous Guernsey, and ending at a Guernsey
        fromGuernsey = Integer.MAX_VALUE;
        if (dp[i][j-1][1] != Integer.MAX_VALUE) {
          fromGuernsey = dp[i][j-1][1] + energy(guernseys[j-2], guernseys[j-1]);
        }
        fromHolstein = Integer.MAX_VALUE;
        if (dp[i][j-1][0] != Integer.MAX_VALUE) {
          fromHolstein = dp[i][j-1][0] + energy(holsteins[i-1], guernseys[j-1]);
        }
        dp[i][j][1] = Math.min(fromHolstein, fromGuernsey);
      }
    }

    for (int[][] row : dp) {
      for (int[] row2 : row) {
        System.out.print("[");
        for (int num : row2) {
          System.out.print(num + " ");
        }
        System.out.print("] ");
      }
      System.out.println();
    }

    // answer is dp[H][G][0], as FJ always ends at a Holstein

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("checklist.out")));
    pw.println(dp[H][G][0]);
    pw.close();
  }

  public static int energy(int[] start, int[] end) {
    return (int)Math.pow(start[0]-end[0],2) + (int)Math.pow(start[1]-end[1],2);
  }
}