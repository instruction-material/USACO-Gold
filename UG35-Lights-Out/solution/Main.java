// http://www.usaco.org/index.php?page=viewproblem2&cpid=599

import java.io.*;
import java.util.*;

class Main {
  static int[][] verticies;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("lightsout.in"));
    int N = Integer.parseInt(br.readLine());
    verticies = new int[N+1][2];

    for (int i = 0; i < N; i++) {
      StringTokenizer st = new StringTokenizer(br.readLine());
      verticies[i][0] = Integer.parseInt(st.nextToken());
      verticies[i][1] = Integer.parseInt(st.nextToken());
    }

    br.close();

    // include the exit as the last vertex as well
    verticies[N][0] = verticies[0][0];
    verticies[N][1] = verticies[0][1];

    // first, calculate the mininum distance from a given vertex i to the exit
    int[] minDist = new int[N+1];
    
    // store the clockwise distances first
    for (int i = 1; i < N; i++) {
      minDist[i] = minDist[i-1] + getDist(i-1, i);
    }

    // now calculate the counterclockwise distance, and compare it to the clockwise distance
    for (int i = N-1; i > 0; i--) {
      int ccDist = minDist[i+1] + getDist(i+1, i);
      minDist[i] = Math.min(minDist[i], ccDist);
    }

    // now, construct an ArrayList of alternating angle-edgeLength-angle etc. values, to represent the barn, going in a clockwise direction
    ArrayList<Integer> barn = new ArrayList<Integer>();
    barn.add(0);  // this marks the exit
    for (int i = 0; i < N-1; i++) {
      barn.add(getDist(i, i+1));
      barn.add(getAngle(i+1));
    }
    barn.add(getDist(N-1, N));
    barn.add(0); // this marks the exit again

    // in this problem, we first want to use what we've calculated already to construct a HashMap of all the possible "intervals" Bessie could see in walking around the barn clockwise and ending at an exit. an interval is a sequence of angle-edgeLength-angle etc. vaues. the HashMap stores the interval and its frequency.
    // then, from each vertex, we walk clockwise until we see a unique interval, and from there we can calculate the total optimal distance to get to the exit

    HashMap<List<Integer>, Integer> intervals = new HashMap<List<Integer>, Integer>();

    for (int i = 0; i < barn.size(); i += 2) {
      for (int j = 1; i+j < barn.size(); j += 2) {
        List<Integer> interval = barn.subList(i, i+j);
        if (intervals.containsKey(interval)) {
          intervals.put(interval, intervals.get(interval) + 1);
        } else {
          intervals.put(interval, 1);
        }
      }
    }

    int answer = 0;
    for (int i = 0; i+2 < barn.size(); i += 2) {
      int dist = 0;

      // start by walking clockwise
      for (int j = 1; i+j < barn.size(); j += 2) {
        // if the interval we have formed is unique, go to the exit
        if (intervals.get(barn.subList(i, i+j)) == 1) {
          // this is the minDist Bessie needs to travel to the exit from this point
          dist += minDist[(i+j)/2];
          break;
        }

        // otherwise, go to the next vertex
        dist += getDist((i+j)/2, (i+j)/2 + 1);
      }

      // update ans (dist represents the distance in the dark, minDist[i/2] represents the distance in the light)
      answer = Math.max(answer, dist - minDist[i/2]);
    }

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("lightsout.out")));
    pw.println(answer);
    pw.close();
  }

  // calculates the distance between two verticies
  private static int getDist(int i, int j) {
    return Math.abs(verticies[i][0] - verticies[j][0]) + Math.abs(verticies[i][1] - verticies[j][1]);
  }

  // calculates the angle at vertex i; returns i if the interior angle is 90 degrees and 2 if the interior angle is 270 degrees
  private static int getAngle(int i) {
    String dir1 = getDirection(i-1, i);
    String dir2 = getDirection(i, i+1);

    if (dir1 == "N" && dir2 == "E") {
      return 1;
    }
    if (dir1 == "N" && dir2 == "W") {
      return 2;
    }
    if (dir1 == "S" && dir2 == "E") {
      return 2;
    }
    if (dir1 == "S" && dir2 == "W") {
      return 1;
    }
    if (dir1 == "E" && dir2 == "N") {
      return 2;
    }
    if (dir1 == "E" && dir2 == "S") {
      return 1;
    }
    if (dir1 == "W" && dir2 == "N") {
      return 1;
    }
    if (dir1 == "W" && dir2 == "S") {
      return 2;
    }

    return -1;  // should never be reached
  }

  // returns N, S, W, or E given the indices of two verticies
  private static String getDirection(int a, int b) {
    if (verticies[a][0] == verticies[b][0]) {
      if (verticies[a][1] > verticies[b][1]) {
        return "N";
      } else {
        return "S";
      }
    } else {
      if (verticies[a][0] > verticies[b][0]) {
        return "E";
      } else {
        return "W";
      }
    }
  }
}