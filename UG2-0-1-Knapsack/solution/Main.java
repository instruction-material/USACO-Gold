import java.util.*;

class Main {
  public static void main(String[] args) {
    /*
      A 0-1 knapsack problem takes the form: Given the weights and values of n items, put these items in a knapsack of capacity w to maximize the value of the knapsack.

      Brute force approach: try all 2^n combinations

      DP approach: construct an n x w grid, where each row is an item and each column is total weight of knapsack, from 0 to w.

      Each cell in this grid represents the maximum value of the knapsack if up to item i can be included and the total weight is exactly j.

      This way, at every cell, we are essentially asking - should we include item i if the maximum weight of the knapsack is j? What is the maximum value we can get if we include or don't include item i?

      If we don't include it, then the maximum value is just the value of the cell above it. If we do include it, then the maximum value is the value of that item, plus the maximum value of the knapsack without that item at a lower maximum weight.

      The answer will simply be the value in the bottom right cell, since here we have the option to include all items and the true maximum weight.

      To find which items are in the knapsack, we perform a traceback from the bottom right. If the value in the cell is equal to the one above it, then the item that row represents must not be in the knapsack. If it is not equal, then that item must be in the knapsack. We move to the previous row (i.e. item) and over to a lesser weight if the item was included. Continue until we reach a cell with 0 value.
    */

    int[] weights = {1,3,4,5};
    int[] values = {1,4,5,7};
    int numItems = 4;
    int maxWeight = 7;

    int[][] dp = new int[numItems+1][maxWeight+1];

    // first row and col remain as 0s, since cannot get any value from 0 weight or 0 items
    
    for (int i = 1; i <= numItems; i++) {
      for (int j = 1; j <= maxWeight; j++) {
        // if including this item will exceed the maximum weight of this cell, then we simply take the value from the cell above because we cannot include it
        if (weights[i-1] > j) {
          dp[i][j] = dp[i-1][j];
        } else {
          // otherwise, calculate the value we can get from including this item versus not including it
          int maxValueWithout = dp[i-1][j];
          int maxValueWith = values[i-1] + dp[i-1][j-weights[i-1]];
          dp[i][j] = Math.max(maxValueWithout, maxValueWith);
        }
      }
    }

    System.out.println("Max value: " + dp[numItems][maxWeight]);

    // traceback - fill ArrayList with the indices of the items in the knapsack

    ArrayList<Integer> items = new ArrayList<Integer>();

    int row = numItems;
    int col = maxWeight;
    while(true) {
      if (dp[row][col] == 0) {
        break;
      }

      if (dp[row][col] == dp[row-1][col]) {
        row--;
      } else {
        items.add(row-1);
        col -= weights[row-1];
      }
    }

    System.out.println("Item indicies in knapsack: "+ items);

    /*
      An alternate version of this problem is: Given the weights and values of n items, find the minimum cost put some of these items in a knapsack that must weigh at least w.

      We use the same DP array setup, but now in each cell we store the minimum cost to weigh at least a certain weight.
    */ 

    
  }
}