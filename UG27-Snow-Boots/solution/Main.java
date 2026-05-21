// http://www.usaco.org/index.php?page=viewproblem2&cpid=813

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {

    // read input
    BufferedReader br = new BufferedReader(new FileReader("snowboots.in"));
    
    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int B = Integer.parseInt(st.nextToken());

    // read in Snow objects
    Snow[] snow = new Snow[N];
    st = new StringTokenizer(br.readLine());
    for (int i = 0; i < N; i++) {
      int d = Integer.parseInt(st.nextToken());
      snow[i] = new Snow(d, i);
    }

    // read in Boot objects
    Boot[] boots = new Boot[B];
    for (int i = 0; i < B; i++) {
      st = new StringTokenizer(br.readLine());
      int d = Integer.parseInt(st.nextToken());
      int s = Integer.parseInt(st.nextToken());
      boots[i] = new Boot(d, s, i);
    }
    
    br.close();

    // sort snow and boots by decreasing depth
    Arrays.sort(snow);
    Arrays.sort(boots);

    // in this problem, we consider each boot, in decreasing depth order. for each boot, we "remove" the Snow objects that are too deep for this boot depth. while we are doing this, we continuously update the max step size the boot would have to be able to make. at the end, if the boot can make this step size, then it's a valid boot
    // we link up the Snow objects in a doubly linked list (tracking which index points to which index) so that we always know the order the Snow objects have to be traversed in, and can update the max step size accordingly.

    // to start, the Snow objects are arranged in the order they are given
    int[] prev = new int[N];
    int[] next = new int[N];

    for (int i = 0; i < N; i++) {
      prev[i] = i-1;
      next[i] = i+1;
    }

    // answer array to store whether each boot is valid
    int[] answer = new int[B];

    int snowIndex = 0;
    int maxStep = 1;

    for (int i = 0; i < B; i++) {
      Boot boot = boots[i];

      // remove all Snow objects that are too deep
      while (snow[snowIndex].depth > boot.depth) {
        // update linked list
        int curr = snow[snowIndex].index;
        next[prev[curr]] = next[curr];
        prev[next[curr]] = prev[curr];

        // update max step size
        maxStep = Math.max(maxStep, next[curr] - prev[curr]);

        snowIndex++;
      }

      // check if this boot is valid
      System.out.println(maxStep);
      if (boot.step >= maxStep) {
        answer[boot.index] = 1;
      }
    }
    
    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("snowboots.out")));
    for (int num : answer) {
      pw.println(num);
    }
    pw.close();
  }
}

class Snow implements Comparable<Snow> {
  int depth;
  int index;

  public Snow(int d, int i) {
    depth = d;
    index = i;
  }
  public int compareTo(Snow other) {
    return other.depth - depth;
  }
}

class Boot implements Comparable<Boot> {
  int depth;
  int step;
  int index;

  public Boot(int d, int s, int i) {
    depth = d;
    step = s;
    index = i;
  }
  public int compareTo(Boot other) {
    return other.depth - depth;
  }
}