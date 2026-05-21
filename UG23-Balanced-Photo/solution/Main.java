// http://www.usaco.org/index.php?page=viewproblem2&cpid=693

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {

    // read input
    BufferedReader br = new BufferedReader(new FileReader("bphoto.in"));
    int N = Integer.parseInt(br.readLine());

    // save array of cow heights, and HashMap mapping heights to their position index
    int[] cows = new int[N];
    HashMap<Integer, Integer> indices = new HashMap<Integer, Integer>();
    for (int i = 0; i < N; i++) {
      int h = Integer.parseInt(br.readLine());
      cows[i] = -h;   // doing this so we can easily sort cows by decreasing height
      indices.put(-h, i);
    }
    br.close();

    // sort cows by decreasing height
    Arrays.sort(cows);

    // in this problem, we iterate through the cows, starting from the tallest cow. we use a BIT and mark a position with a 1 if we have seen this cow. this way, we can easily calculate the number of cows to the left and to the right of the given cow that are taller than the current cow.

    BinaryIndexedTree bit = new BinaryIndexedTree(N);
    int numUnbalanced = 0;

    for (int i = 0; i < N; i++) {
      int ind = indices.get(cows[i]);

      int numLeft = bit.sum(ind);
      int numRight = i - numLeft;

      // check if unbalanced
      if (Math.max(numLeft, numRight) > 2 * Math.min(numLeft, numRight)) {
        numUnbalanced++;
      }

      // add to BIT
      bit.add(1, ind);
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("bphoto.out")));
    pw.println(numUnbalanced);
    pw.close();
  }
}

class BinaryIndexedTree {
  private int[] A;

  public BinaryIndexedTree(int N) {
    A = new int[N+1];
  }

  // returns least significant bit of given integer
  private int LSB(int i) {
    return i & -i;
  }

  // add k to index i
  public void add(int k, int i) {
    for (i++; i < A.length; i += LSB(i)) {
      A[i] += k;
    }
  }

  // return sum of numbers up to index i
  public int sum(int i) {
    int total = 0;
    for (i++; i > 0; i -= LSB(i)) {
      total += A[i];
    }
    return total;
  }
}