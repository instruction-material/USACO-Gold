// http://usaco.org/index.php?page=viewproblem2&cpid=598

import java.io.*;
import java.util.*;

class Main {
  static int[][] fjPath;
  static int[][] bPath;
  
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("radio.in"));

    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int M = Integer.parseInt(st.nextToken());

    fjPath = new int[N+1][2];
    bPath = new int[M+1][2];

    st = new StringTokenizer(br.readLine());
    fjPath[0][0] = Integer.parseInt(st.nextToken());
    fjPath[0][1] = Integer.parseInt(st.nextToken());

    st = new StringTokenizer(br.readLine());
    bPath[0][0] = Integer.parseInt(st.nextToken());
    bPath[0][1] = Integer.parseInt(st.nextToken());

    String fjDirections = br.readLine();
    for (int i = 0; i < N; i++) {
      if (fjDirections.charAt(i) == 'N') {
        fjPath[i+1][0] = fjPath[i][0];
        fjPath[i+1][1] = fjPath[i][1] + 1;
      } else if (fjDirections.charAt(i) == 'S') {
        fjPath[i+1][0] = fjPath[i][0];
        fjPath[i+1][1] = fjPath[i][1] - 1;
      } else if (fjDirections.charAt(i) == 'E') {
        fjPath[i+1][0] = fjPath[i][0] + 1;
        fjPath[i+1][1] = fjPath[i][1];
      } else if (fjDirections.charAt(i) == 'W') {
        fjPath[i+1][0] = fjPath[i][0] - 1;
        fjPath[i+1][1] = fjPath[i][1];
      }
    }

    String bDirections = br.readLine();

    for (int i = 0; i < M; i++) {
      if (bDirections.charAt(i) == 'N') {
        bPath[i+1][0] = bPath[i][0];
        bPath[i+1][1] = bPath[i][1] + 1;
      } else if (bDirections.charAt(i) == 'S') {
        bPath[i+1][0] = bPath[i][0];
        bPath[i+1][1] = bPath[i][1] - 1;
      } else if (bDirections.charAt(i) == 'E') {
        bPath[i+1][0] = bPath[i][0] + 1;
        bPath[i+1][1] = bPath[i][1];
      } else if (bDirections.charAt(i) == 'W') {
        bPath[i+1][0] = bPath[i][0] - 1;
        bPath[i+1][1] = bPath[i][1];
      }
    }
    
    br.close();

    // in this problem, we use DP to calculate the min cost after FJ has walked i steps and Bessie has walked j steps
    int[][] dp = new int[N+1][M+1];

    for (int i = 1; i <= N; i++) {
      // FJ is moving, but Bessie is still at beginning
      dp[i][0] = dp[i-1][0] + cost(i, 0);
    }

    for (int j = 1; j <= M; j++) {
      // Bessie is moving, but FJ is still at beginning
      dp[0][j] = dp[0][j-1] + cost(0, j);
    }

    for (int i = 1; i <= N; i++) {
      for (int j = 1; j <= M; j++) {
        dp[i][j] = Math.min(dp[i-1][j], Math.min(dp[i][j-1], dp[i-1][j-1]));
        dp[i][j] += cost(i,j);
      }
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("radio.out")));
    pw.println(dp[N][M]);
    pw.close();
  }

  public static int cost(int fi, int bi) {
    return (fjPath[fi][0] - bPath[bi][0]) * (fjPath[fi][0] - bPath[bi][0]) + (fjPath[fi][1] - bPath[bi][1]) * (fjPath[fi][1] - bPath[bi][1]);
  }
}