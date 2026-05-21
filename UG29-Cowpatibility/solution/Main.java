// http://usaco.org/index.php?page=viewproblem2&cpid=862

import java.io.*;
import java.util.*;

class Main {
  static HashMap<HashedSubset, Integer> subsets;

  public static void main(String[] args) throws IOException {
    // read input
    BufferedReader br = new BufferedReader(new FileReader("cowpatibility.in"));

    int N = Integer.parseInt(br.readLine());
    int[] flavors = new int[5];

    // in this problem, we first need to generate all the possible subsets of the 5 flavors for each cow. for example, if the 5 flavors are 1 2 3 4 5, then we need to generate 1, 2, 3, 4, 5, 1 2, 1 3, 1 4, 1 2 3, etc.
    // we store the frequencies of each of these subsets occurring across all cows in a HashMap
    // this way, we can use the principle of inclusion-exclusion (PIE) to count the number of compatible cows, i.e. those who share at least one flavor, and subtract that from N*(N-1)/2 to find the total number of incompatible cows
    // PIE tells us that the number of compatible cows = # pairs of cows who share 1 common flavor - # pairs of cows who share 2 common flavors + # pairs of cows who share 3 common flavors - # pairs of cows who share 4 common flavors + # pairs of cows who share 5 common flavors
    // these values are all contained within our HashMap, because if there are C cows who like three specific flavors, then there are C*(C-1)/2 pairs of cows who like those three specific flavors

    subsets = new HashMap<HashedSubset, Integer>();

    for (int i = 0; i < N; i++) {
      StringTokenizer st = new StringTokenizer(br.readLine());
      for (int j = 0; j < 5; j++) {
        flavors[j] = Integer.parseInt(st.nextToken());
      }

      // make sure the flavors are sorted
      Arrays.sort(flavors);

      updateSubsets(flavors);
    }

    br.close();

    // use the HashMap to compute answer - we use arr to determine whether the number should be added or substracted from the total based on the equation explained above
    int[] arr = {0, 1, -1, 1, -1, 1};
    long ans = 0;

    for (HashedSubset subset : subsets.keySet()) {
      long numCows = subsets.get(subset);
      ans += arr[subset.sz] * (numCows * (numCows - 1) / 2);
    }

    // we have calculated the number of compatible cows, so subtract from the total number of pairings to get the number of incompatible cows
    ans = (long)N*(N-1)/2 - ans;

    // write output
    PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter("cowpatibility.out")));
    pw.println(ans);
    // System.out.println(ans);
    pw.close();
  }

  static void updateSubsets(int[] flavors) {
    // add all the possible subsets of these 5 flavors to our HashMap
    // (1<<k) is a number with its kth bit set to 1, so when we and it with j (the subset number), we get which numbers are present in this given subset
    // e.x. if i = 9, which is 00101, then we will end up adding the 1st and 3rd flavors into the subset, because the inner loops picks up each number that is set to 1 one by one
    for (int i = 1; i < 32; i++) {
      int[] subset = new int[5];
      int sz = 0;
      for (int j = 0; j < 5; j++) {
        if ((i & (1<<j)) > 0) {
          subset[sz++] = flavors[j];
        }
      }

      // add this subset to the HashMap
      subsets.put(new HashedSubset(subset, sz), subsets.getOrDefault(new HashedSubset(subset, sz), 0) + 1);
    }
  }
}
class HashedSubset {
  int sz;
  int[] arr;
	
	public HashedSubset(int[] _arr, int _sz) {
    arr = _arr;
    sz = _sz;
    assert(arr.length==5);
	}
	
	@Override
	public int hashCode() {
		return Arrays.hashCode(arr);
	}
	
	@Override
	public boolean equals(Object other) {
		HashedSubset o = (HashedSubset) other;
		for (int i = 0; i < 5; i++) {
			if (arr[i] != o.arr[i]) {
				return false;
			}
		}
		return true;
	}
}