class Main {

  public static void main(String[] args) {
    int[] arr = {5, -5, 6, 2, 3};
    System.out.println(maxSubarraySum(arr));
    
    System.out.println(numPaths(3,2));

    int[][] items = {{1, 5}, {2, 3}, {4, 5}, {2, 3}, {5, 2}};
    System.out.println(knapsackRecursive(4, 10, items));
  }

  // given an array of positive and negative integers, find the maximum contiguous array sum

  public static int maxSubarraySum(int[] arr) {
    // the max sum up to arr[i+1] = the max sum up to arr[i], and then either add or don't add arr[i+1]. every time we look at a new number, we either add to the running sum or start a new running sum.

    int max = 0;
    int currSum = 0;

    for (int i = 0; i < arr.length; i++) {
      currSum = Math.max(arr[i], currSum+arr[i]);
      max = Math.max(max, currSum);
    }

    return max;
  }

  // given a MxN grid, how many paths can you take from the top left to the bottom right cell?
  // if start leads to a and b, numPaths(start,end) = numPaths(a,end) + numPaths(b,end)

  public static int numPaths(int m, int n) {
    int count[][] = new int[m][n]; 
    
    // fill in bottom row and rightmost column
    for (int i = 0; i < m; i++) {
      count[i][n-1] = 1;
    }

    for (int j = 0; j < n; j++) {
      count[m-1][j] = 1;
    }
    
    // count other paths, starting at bottom right
    for (int i = m-2; i >= 0; i--) { 
      for (int j = n-2; j >= 0; j--) {
        count[i][j] = count[i+1][j] + count[i][j+1];
      }
    }
    
    return count[0][0];
  }

  // 0-1 knapsack problem: given a set of n items and their weights and values, pick items that sum up to a weight limit to maximize the value
  // we can recursively try all 2^n combinations:

  public static int knapsackRecursive(int itemsIndex, int remainingCapacity, int[][] items) {
    if (itemsIndex == 0 || remainingCapacity == 0) {
      return 0;
    } else if (items[itemsIndex][0] > remainingCapacity) {
      return knapsackRecursive(itemsIndex-1, remainingCapacity, items);
    } else {
      // don't include this item
      int option1 = knapsackRecursive(itemsIndex-1, remainingCapacity, items);

      // include this item
      int option2 = items[itemsIndex][1] + knapsackRecursive(itemsIndex-1, remainingCapacity-items[itemsIndex][0], items);

      return Math.max(option1, option2);
    }
  }

  // however every time we land on a particular combination of (itemsIndex, remainingCapacity) 
}