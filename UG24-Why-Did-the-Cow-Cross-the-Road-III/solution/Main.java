// http://usaco.org/index.php?page=viewproblem2&cpid=719

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("circlecross.in"));
    int N = Integer.parseInt(br.readLine());

    // create an array of Cows, where each Cow has its entry and exit point. in order to do this, use a helper array to store each Cow's entry point and retreive it when we see its exit point

    int[] arr = new int[N];
    for (int i = 0; i < N; i++) {
      arr[i] = -1;
    }

    Cow[] cows = new Cow[N];
    int cowCounter = 0;
    for (int i = 0; i < N*2; i++) {
      int cow = Integer.parseInt(br.readLine())-1;

      // if the corresponding cow in arr is still -1, then this is an entry point, otherwise this is an exit point
      if (arr[cow] == -1) {
        arr[cow] = i;
      } else {
        int entry = arr[cow];
        int exit = i;
        cows[cowCounter] = new Cow(entry, exit);
        cowCounter++;
      }
    }

    br.close();

    // sort cows by entry point
    Arrays.sort(cows);

    // in this problem, we look at each cow in order of increasing entry point. each time we look at a cow, we use a BIT and mark its exit position with a 1. we then use the BIT to calculate the number of exit points between this cow's entry and exit point, which is the number of crossings. note that if an exit point is marked in the BIT, then its corresponding entry point must be before this current cow's, because we are going through the cows in order of increasing entry point.

    BinaryIndexedTree bit = new BinaryIndexedTree(2*N);
    int numCrossings = 0;

    for (Cow c : cows) {
      numCrossings += bit.sum(c.exit) - bit.sum(c.entry);
      bit.add(1, c.exit);
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("circlecross.out")));
    pw.println(numCrossings);
    pw.close();

  }
}

class Cow implements Comparable<Cow> {
  int entry;
  int exit;

  public Cow(int a, int b) {
    entry = a;
    exit = b;
  }
  public int compareTo(Cow other) {
    return entry - other.entry;
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