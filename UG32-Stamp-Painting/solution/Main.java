// http://usaco.org/index.php?page=viewproblem2&cpid=791

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("spainting.in"));

    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int M = Integer.parseInt(st.nextToken());
    int K = Integer.parseInt(st.nextToken());
    br.close();

    long MOD = 1000000007;

    // in this problem, one key observation is that a valid canvas must have a subsequence of length K that is one color, and the rest of the canvas can literally be any combination of any colors, because we can always stamp over the other stamps, but we need to place a final stamp of length K
    // however, it's hard to calculate the number of valid canvases with combinatorics because of overcounting
    // instead, we will use complementary counting to calculate the number of canvases where there is NO subsequence of length K or larger that is one color, and subtract that from the total number of canvases (which is M^N, as there are N slots and M colors per slot)
    // dp[i] = # canvases with NO subsequence of length K or larger than is one color, where the canvas is i units long
    // note that if i < K, then dp[i] = M^i, as any slot can be any color
    // if i >= K, then we can form a canvas that goes up to i-1 and the last color can be any of M-1 colors (just not the color at i-1), or up to i-2 and the last two colors can be any of M-1 colors, all the way up i-c where c < K
    // so this is dp[i-1] * (M-1) + dp[i-2] * (M-1)...

    long[] dp = new long[N+1];

    /*
    the below works for the first 9 test cases:

    for (int i = 1; i < K; i++) {
      dp[i] = pow(M, i);
    }

    for (int i = K; i <= N; i++) {
      for (int c = 1; c < K; c++) {
        // this is essentially what we are calculating here:
        // dp[i] += dp[i-c] * (M-1)

        // (a*b)%n = ((a%n)*(b%n)) % n
        long newVal = ((dp[i-c] % MOD) * ((M-1) % MOD)) % MOD;

        // (a+b)%n = ((a%n)+(b%n)) % n
        dp[i] = (dp[i] % MOD + newVal % MOD) % MOD;
      }
    }

    */

    /*
    note that to pass the last 3 test cases, we need an O(N) solution instead of an O(NK) solution. to accomplish this, we can essentially remove the need to iterate K times for every pass, by storing the previously computed value and shifting it over, like this:
    */

    dp[1] = M;

    for (int i = 2; i < K; i++) {
      dp[i] = (dp[i-1] * M) % MOD;
    }

    long runningSum = 0;

    // when we're calculating dp[K], we need the runningSum to be initialized to dp[0] + ... + dp[K-2], and then the dp[K-1] term is added in the next loop
    for (int i = 0; i < K-1; i++) {
      runningSum += dp[i];
    }

    for (int i = K; i <= N; i++) {
      runningSum = (runningSum % MOD + dp[i-1] % MOD) % MOD;
      runningSum -= dp[i-K];
      dp[i] = ((M-1) * runningSum) % MOD;
    }

    long totalNumCanvases = pow(M,N);

    // totalNumCanvases - dp[N] may be negative since totalNumCanvases has been modded, so we have to add MOD back
    long answer = (totalNumCanvases - dp[N] + MOD) % MOD;

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("spainting.out")));
    pw.println(answer);
    pw.close();
  }

  static long pow(long a, long b) {
    final long MOD = 1000000007;

    // if (b == 0) return 1;
    // else if (b == 1) return a;
    // else if (b % 2 == 0) return pow(a * a % MOD, b / 2);
    // else return (a * pow(a * a % MOD, b / 2)) % MOD;

    long answer = 1;
    for (int i = 0; i < b; i++) {
      answer = (answer * a) % MOD;
    }

    return answer;
  }
}