// http://www.usaco.org/index.php?page=viewproblem2&cpid=837

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {

    // read input
    BufferedReader br = new BufferedReader(new FileReader("sort.in"));
    int N = Integer.parseInt(br.readLine());

    // read in array of Number objects, storing each number's value and position, so that we can sort by value and still retain its original position
    Number[] nums = new Number[N];
    for (int i = 0; i < N; i++) {
      nums[i] = new Number(i, Integer.parseInt(br.readLine()));
    }
    br.close();

    // sort Numbers by value
    Arrays.sort(nums);

    // in this problem, we consider drawing an imaginary line between each element in the array. in considering these lines, the most number of passes we have to do is equal to the largest number of elements that need to be moved from the right to the left side of this line. so for each line, as we're iterating through the numbers in sorted order, we can count the number of numbers to the right of the line that need to be moved by marking these numbers in a BIT as we go

    BinaryIndexedTree bit = new BinaryIndexedTree(N);

    // set this to 1 to start because worst case, if the array is already sorted, it will still print "moo" once to check that it is sorted
    int answer = 1;

    for (int i = 0; i < N-1; i++) {
      // add this number to the BIT
      bit.add(1, nums[i].pos);

      int numElementsToBeMovedFromRight = i+1-bit.sum(i);
      // System.out.println(nums[i].value + " " + numElementsToBeMovedFromRight);
      answer = Math.max(answer, numElementsToBeMovedFromRight);
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("sort.out")));
    pw.println(answer);
    pw.close();
  }
}

class Number implements Comparable<Number> {
  int pos;
  int value;

  public Number(int pos, int value) {
    this.pos = pos;
    this.value = value;
  }
  public int compareTo(Number num) {
    return value - num.value;
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