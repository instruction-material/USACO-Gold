import java.io.*;
import java.util.*;

class Main {
  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("time.in"));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int N = Integer.parseInt(st.nextToken());
    int M = Integer.parseInt(st.nextToken());
    int C = Integer.parseInt(st.nextToken());

    int[] mooniesPerCity = new int[N];
    st = new StringTokenizer(br.readLine());
    for (int i = 0; i < N; i++) {
      mooniesPerCity[i] = Integer.parseInt(st.nextToken());
    }

    ArrayList<Integer>[] edges = new ArrayList[N];

    for (int i = 0; i < N; i++) {
      edges[i] = new ArrayList<Integer>();
    }

    for (int i = 0; i < M; i++) {
      st = new StringTokenizer(br.readLine());
      int start = Integer.parseInt(st.nextToken())-1;
      int end = Integer.parseInt(st.nextToken())-1;
      edges[start].add(end);
    }

    br.close();

    // profit[i][j] holds the max profit if we visit city i after traveling for j days, disregarding the preparation cost. at the end, the answer will just be the maximum of the values in profit[0][...] minus that preparation cost
    int[][] profit = new int[N][1001];
    for (int i = 0; i < N; i++) {
      for (int j = 0; j <= 1000; j++) {
        profit[i][j] = -1;
      }
    }

    // we know that m=0 at the first city, where we start
    profit[0][0] = 0;

    // in this problem, we start at the first city on the first day with 0 profit. we then traverse the graph by visiting each of its neighbors, and updating profit accordingly. we can use a PriorityQueue to keep track of each node we need to visit; each node has a city, day, and profit associated with it. when we poll from the PQ, we go in order of the days (smallest days first), and then secondarily by profit (largest profit first)

    PriorityQueue<int[]> pq = new PriorityQueue<int[]>(new Comparator<int[]>(){
      public int compare(int[] a, int[] b) {
        if (a[1] != b[1]) {
          return a[1]-b[1]; // return smaller day
        } else {
          return b[2]-a[2]; // return larger profit
        }
      }
    });

    // start at the first city
    pq.add(new int[]{0,0,0});

    while (!pq.isEmpty()) {
      int[] node = pq.poll();
      int city = node[0];
      int day = node[1];
      int currProfit = node[2];

      if (day==1000) continue;

      for (int neighbor: edges[city]) {
        if (profit[neighbor][day+1] < currProfit + mooniesPerCity[neighbor]) {
          profit[neighbor][day+1] = currProfit + mooniesPerCity[neighbor];
          pq.add(new int[]{neighbor, day+1, profit[neighbor][day+1]});
        }
      }
    }

    int answer = 0;
    for (int i = 0; i <= 1000; i++) {
      answer = Math.max(answer, profit[0][i]-C*i*i);
    }

    // write output
    PrintWriter pw = new PrintWriter("time.out");
    pw.println(answer);
    pw.close();
  }
}