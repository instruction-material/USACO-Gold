// http://usaco.org/index.php?page=viewproblem2&cpid=621

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("cbarn.in"));
    int N = Integer.parseInt(br.readLine());
    int[] cows = new int[N];
    for (int i = 0; i < N; i++) {
      cows[i] = Integer.parseInt(br.readLine());
    }
    br.close();
    
    // in this problem, the intuitive approach is to try each cow as a starting point and loop around the whole barn, picking up cows as you go and dropping off the earliest-picked-up cow at each room. we'll notice that for most possible starting points, we'll end up with a surplus of cows after we make it around the barn once, so we'll have revisisit some rooms to fully distribute the cows. however, for the optimal starting point, we'll be able to distribute the cows perfectly once we get to the last room (because we have exactly as many cows as rooms).
    // the straightforward approach would be to try each cow as the starting point, as described. however, n is too large. we can instead find the optimal n by starting at the beginning and keeping track of the last room we visit where we have no cows to drop off! this tells us that we should start at the room after it, and circle back to end at that room.

    // this loop does the initial cycle, to find the last room we visit where we have no cows to drop off
    int lastRoom = -1;
    int numCowsinQueue = 0;

    for (int i = 0; i < N; i++) {
      // pick up cows
      numCowsinQueue += cows[i];

      // update lastRoom if we have no cows in our queue
      if (numCowsinQueue == 0) {
        lastRoom = i;
      } else {
        // drop off 1 cow
        numCowsinQueue--;
      }
    }

    int startRoom = lastRoom + 1;
    long answer = 0;

    // now this loop starts at the startRoom, adding the cow's index where it was picked up into a queue. note that the loop indexing starts at 0, and we calculate r (the actual room index) for each iteration

    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < N; i++) {
      int r = (startRoom + i) % N; // current room index

      // pick up cows (add to queue)
      for (int j = 0; j < cows[r]; j++) {
          q.add(i);
      }

      // drop off 1 cow
      int droppedCow = q.poll();

      // update the total distance
      answer += (i - droppedCow) * (i - droppedCow);
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("cbarn.out")));
    pw.println(answer);
    pw.close();
  }
}