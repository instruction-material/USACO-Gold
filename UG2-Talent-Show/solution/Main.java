// http://usaco.org/index.php?page=viewproblem2&cpid=839

import java.io.*;
import java.util.*;

class Main {
    static int N;
    static int W;
    static long[] w;
    static long[] t;
    static long[][] dp;
    static final long nINF = -1000000000000000L;
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("talent.in"));
        PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("talent.out")));
        StringTokenizer st = new StringTokenizer(br.readLine());
        N = Integer.parseInt(st.nextToken());
        W = Integer.parseInt(st.nextToken());
        w = new long[N];
        t = new long[N];
        for (int i = 0; i < N; i++) {
            st = new StringTokenizer(br.readLine());
            w[i] = Long.parseLong(st.nextToken());
            t[i] = Long.parseLong(st.nextToken());
        }
        br.close();
        //binary search on the ratio 
        long lo = 0;
        long hi = 250 * 1000 * 1000 + 1;
        dp = new long[N][W+1];
        while (lo + 1 < hi) {
            long mid = (lo + hi) / 2;
            if (checkPossible(mid))
                lo = mid;
            else
                hi = mid;
        }
        out.println(lo);
        out.close();
    }
    public static boolean checkPossible(long ratio) {
        // check whether a given ratio is possible 
        // dp[i][j] = using first i cows with weight j, what is the maximum value of 
        // sum of 1000 * t[i] - w[i]
        for (int i = 0; i < N; i++) {
            for(int j = 0; j <= W; j++) {
                dp[i][j] = nINF;
            }
        }
        dp[0][0] = 0;
        dp[0][Math.min(W,(int)w[0])] = 1000*t[0] - w[0]*ratio;
        for(int i = 0; i < N-1; i++) {
            for(int j = 0; j <= W; j++) {
                int nextW = Math.min(j + (int)w[i+1], W);
                if(dp[i][j] == nINF) continue;
                dp[i+1][j] = Math.max(dp[i+1][j], dp[i][j]);
                dp[i+1][nextW] = Math.max(dp[i+1][nextW], dp[i][j] + 1000*t[i+1] - w[i+1]*ratio);
            }
        }
        return dp[N-1][W] >= 0;
    }

}