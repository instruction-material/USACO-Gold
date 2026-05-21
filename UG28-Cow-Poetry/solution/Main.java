// http://usaco.org/index.php?page=viewproblem2&cpid=897

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {

    // read input
    BufferedReader br = new BufferedReader(new FileReader("poetry.in"));

    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int M = Integer.parseInt(st.nextToken());
    int K = Integer.parseInt(st.nextToken());

    int[][] words = new int[N][2];
    for (int i = 0; i < N; i++) {
      st = new StringTokenizer(br.readLine());
      words[i][0] = Integer.parseInt(st.nextToken());
      words[i][1] = Integer.parseInt(st.nextToken()) - 1;
    }

    final long MOD = 1000000007;

    // store the frequencies of the number of lines of each rhyme scheme we need in a HashMap, where the key is the rhyme scheme and the value is the frequency

    HashMap<String, Integer> freq = new HashMap<String, Integer>();
    for (int i = 0; i < M; i++) {
      String rhymeScheme = br.readLine();
      if (freq.containsKey(rhymeScheme)) {
        freq.put(rhymeScheme, freq.get(rhymeScheme) + 1);
      } else {
        freq.put(rhymeScheme, 1);
      }
    }

    br.close();

     // dp[i] stores the number of ways there are to write a line with i syllables, regardless of the rhyming. the general approach is to build the lines by looping over the words and continuously adding each word to i=1, i=2, etc.
    // more specifically, we do this by first looping over all of the words - for each word that has j syllables, we add 1 to dp[j] (this is what the first loop where i=0 accomplishes)
    // then, we loop over all of the words again, this time starting with lines that already have i=1 syllable in them. for each word that has j syllables, we add dp[1] to dp[j+1] (this is what the loop where i=1 accomplishes). this is because there were dp[1] ways to write a line with 1 syllable, so if we add this word to those lines, then there are an additional dp[1] ways to make a line with i+1 syllables
    // we then repeat this starting with lines that already have 2 syllables, etc, up to K syllables. note that for each word we consider adding, we have to check that to make sure the total number of syllables does not exceed K
    long[] dp = new long[K+1];
    dp[0] = 1;
    for (int i = 0; i <= K; i++) {
      // loop over each word
      for (int j = 0; j < N; j++) {
        int numSyllablesInWord = words[j][0];

        // check that adding this number of syllables to i does not exceed K
        int updatedNumSyllables = i + numSyllablesInWord;
        if (updatedNumSyllables <= K) {
          // because (a+b)%n = ((a%n)+(b%n)) % n, we just keep taking the mod as we add to dp[updatedNumSyllables]
          dp[updatedNumSyllables] = (dp[updatedNumSyllables] + dp[i]) % MOD;
        }
      }
    }

    // dp2[i] stores the number of ways you can write a line ending with rhyme class i
    // to compute dp2, we iterate through each word. given the word is part of rhyme class i, we update dp2[i] by adding the number of ways we can complete the line with the remaining number of syllables (essentially counting the number of ways we can write a line with K syllables that ends with this word)

    long dp2[] = new long[N+1];
    for (int i = 0; i < N; i++) {
      int numSyllablesInWord = words[i][0];
      int rhymeClass = words[i][1];

      dp2[rhymeClass] = (dp2[rhymeClass] + dp[K-numSyllablesInWord]) % MOD;
    }

    // to compute the answer, we iterate through each rhyme scheme in freq. for each rhyme scheme, let numLines be the number of lines of that rhyme scheme we need. we iterate through all of the rhyme classes, and for each rhyme class, we compute the number of ways we can write numLines with that rhyme class (by raising dp2[i] to numLines)

    long answer = 1;
    for (String s : freq.keySet()) {
      long numPermutationsRhymeScheme = 0;
      for (int i = 0; i <= N; i++) {
        long numPermutationsRhymeClass = dp2[i];
        if (numPermutationsRhymeClass > 0) {
          numPermutationsRhymeScheme = (numPermutationsRhymeScheme + pow(numPermutationsRhymeClass, freq.get(s))) % MOD;
        }
      }

      // multiply all the total number of permutations for each rhyme scheme together
      // because (a*b)%n = ((a%n)*(b%n)) % n, we just keep taking the mod as we multiply
      answer = (answer * numPermutationsRhymeScheme) % MOD;
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("poetry.out")));
    pw.println(answer);
    pw.close();
  }

  // we need to use a fast exponentiation algorithm, which can compute (a^b)mod1000000007 in O(logb). Math.pow() will not work for this problem
  // reference: https://en.wikipedia.org/wiki/Exponentiation_by_squaring
  static long pow(long a, long b) {
    final long MOD = 1000000007;

	  // Recursive version - O(log(b))
    if (b == 0) return 1;
    else if (b == 1) return a;
    else if (b % 2 == 0) return pow(a * a % MOD, b / 2);
    else return (a * pow(a * a % MOD, b / 2)) % MOD;

    // iterative version - O(log(b))
    /*
    long ans = 1;
    for (; b > 0 ; b /= 2, a = (a*a)%MOD) {
      if ( (b & 1) > 0) 
        ans = (ans * a) % MOD;
    }
    return ans;
    */

    // Straightforward linear exponentiation - O(b)
    /*
    long answer = 1;
      for (int i = 0; i < b; i++) {
        answer = (answer * a) % MOD;
      }
    return answer;
    */
  }
}