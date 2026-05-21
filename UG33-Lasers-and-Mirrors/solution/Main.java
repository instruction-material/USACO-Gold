// http://www.usaco.org/index.php?page=viewproblem2&cpid=671

import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input - note that since x and y are both positive in this problem, we will use a negative number denote a y
    BufferedReader br = new BufferedReader(new FileReader("lasers.in"));
    
    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int xl = -Integer.parseInt(st.nextToken()) - 1;
    int yl = Integer.parseInt(st.nextToken());
    int xb = -Integer.parseInt(st.nextToken()) - 1;
    int yb = Integer.parseInt(st.nextToken());

    // store HashMap of points where key is one coordinate and value is the other coordinate

    HashMap<Integer, ArrayList<Integer>> points = new HashMap<Integer, ArrayList<Integer>>();

    for (int i = 0; i < N; i++) {
      st = new StringTokenizer(br.readLine());

      int x = -Integer.parseInt(st.nextToken()) - 1;
      int y = Integer.parseInt(st.nextToken());

      if (!points.containsKey(x)) {
        points.put(x, new ArrayList<Integer>());
      }
      points.get(x).add(y);

      if (!points.containsKey(y)) {
        points.put(y, new ArrayList<Integer>());
      }
      points.get(y).add(x);
    }

    br.close();

    // in this problem, we run BFS from the starting point, placing both the x and the y coordinate into the queue. when we pop an x coordinate from the queue, we use points to see which y coordinates it corresponds with, and we do the opposite for y coordinates. when we pop a coordinate that is equal to one of the barn's coordinates, then we know we can now reach the barn.

    // we have to use a HashMap called numMirrors to keep track of how many mirrors we've used to get to each coordinate, which also serves as our visited data structure.

    // also note that we have to use BFS instead of DFS to guarantee that we will find the minimum number of mirrors!

    Queue<Integer> q = new LinkedList<Integer>();
    int answer = 0;
    HashMap<Integer, Integer> numMirrors = new HashMap<Integer, Integer>();

    q.add(xl);
    q.add(yl);
    numMirrors.put(xl, 0);
    numMirrors.put(yl, 0);

    while (!q.isEmpty()) {
      int coord = q.poll();

      // check if we can access barn
      if (coord == xb || coord == yb) {
        answer = numMirrors.get(coord);
        break;
      }

      if (points.containsKey(coord)) {
        for (int newCoord : points.get(coord)) {
          if (!numMirrors.containsKey(newCoord)) {
            numMirrors.put(newCoord, numMirrors.get(coord) + 1);
            q.add(newCoord);
          }
        }
      }
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("lasers.out")));
    pw.println(answer);
    pw.close();
  }
}