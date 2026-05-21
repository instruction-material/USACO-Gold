// http://usaco.org/index.php?page=viewproblem2&cpid=898

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {

    // read input
    BufferedReader br = new BufferedReader(new FileReader("sleepy.in"));
    int N = Integer.parseInt(br.readLine());

    StringTokenizer st = new StringTokenizer(br.readLine());
    int[] cows = new int[N];
    for (int i = 0; i < N; i++) {
      cows[i] = Integer.parseInt(st.nextToken()) - 1;
    }
    br.close();

    // in this problem, we observe that the optimal way to complete the sorting is to tell each cow to go into its proper place in the sorted suffix of the sequence. that way, we never end up giving a cow a command more than once, and the cows in the sorted suffix will never get a command
    // this means that for each cow, the number of steps it has to take is equal to the number of cows that are not currently in the sorted suffix (not including itself), plus the number of cows that are smaller than itself in the sorted suffix
    // for this latter number, we use a BIT of size N and mark an element with a 1 when that cow is present in the sorted suffix. that way, we can calculate that number in O(logN) time

    // find index of first cow in sorted suffix
    int sortedStart = N-1;
    while (sortedStart > 0 && cows[sortedStart] > cows[sortedStart-1]) {
      sortedStart--;
    }

    // add the sorted cows to the BIT
    BinaryIndexedTree bit = new BinaryIndexedTree(N);
    for (int i = sortedStart; i < N; i++) {
      bit.add(1, cows[i]);
    }
    
    // write the number of cows that we need to give commands to (i.e. the number not in the sorted suffix)
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("sleepy.out")));
    pw.println(sortedStart);

    // loop through the cows up to sortedStart
    for (int i = 0; i < sortedStart; i++) {
      int numCows1 = sortedStart-1-i;
      int numCows2 = bit.sum(cows[i]);

      pw.print(numCows1 + numCows2);
      if (i != sortedStart-1) {
        pw.print(" ");
      }

      // add this cow to the sorted suffix
      bit.add(1, cows[i]);
    }

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