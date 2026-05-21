// http://usaco.org/index.php?page=viewproblem2&cpid=741

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("cownomics.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int M = Integer.parseInt(st.nextToken());

    String[] spottyCows = new String[N];
    String[] plainCows = new String[N];

    for (int i = 0; i < N; i++) {
      spottyCows[i] = br.readLine();
    }
    for (int i = 0; i < N; i++) {
      plainCows[i] = br.readLine();
    }

    // in this problem, we want to calculate the length of the smallest subsequence in the genome where none of the subsequences of the spotty cows are found in the plain cows. the brute force approach would be to iterate over all possible lengths and starting positions, which is too slow
    // instead, we binary search over all possible lengths and checking all possible starting positions

    int low = 1;  // min possible value for the length
    int high = M; // max possible value for the length
    int answer = M; // set answer to max possible value for now

    while (low <= high) {
      // update mid (i.e. the length of the subsequence for this iteration of binary search)
      int mid = (low + high) / 2;

      boolean foundSubsequenceExplainingSpottiness = false;

      // iterate over all possible starting positions
      for (int start = 0; start < M-mid; start++) {

        // create set of spotty cow subsequences
        HashSet<String> s = new HashSet<String>();
        for (int i = 0; i < N; i++) {
          s.add(spottyCows[i].substring(start, start + mid));
        }

        // iterate over plain cow subsequences and check if any of these are contained in the set, meaning this subsequence does not explain spottiness
        boolean isValid = true;

        for (int i = 0; i < N; i++) {
          String p = plainCows[i].substring(start, start+mid);
          if (s.contains(p)) {
            isValid = false;
            break;
          }
        }

        // break out of looping over all possible starting positions for this length if we found a subsequence that explains spottiness
        if (isValid) {
          foundSubsequenceExplainingSpottiness = true;
          break;
        }
      }

      // update binary search - if we found a subsequences that explains spottiness, then we look for smaller lengths; otherwise, look fo longer lengths
      if (foundSubsequenceExplainingSpottiness) {
        high = mid-1;
        answer = Math.min(answer, mid); // update answer
      } else {
        low = mid+1;
      }
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("cownomics.out")));
    pw.println(answer);
    pw.close();
  }
}