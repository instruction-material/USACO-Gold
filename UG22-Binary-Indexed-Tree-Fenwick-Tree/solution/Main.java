/*

Binary indexed trees (BIT) allow us to compute subarray sums in O(log(N)) time. Modifying the original array also takes O(log(N)) time. The latter fact is why we would us a BIT over a prefix sum array. (It takes O(N) time to update a prefix sum array.)

Example:

Original array: [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
Indicies:        0  1   2  3  4  5   6  7  8  9  10

BIT:

            0

1      2        4          8

       3      5   6      9   10

                    7           11

Note that the BIT goes from 0 to 11, one more than the last index.

* How is this tree laid out? *
Parent(i) = Binary representation of i, with rightmost set bit flipped

Ex. 8 in binary is 1000 -> rightmost set bit flipped = 0000 = 0
Ex. 10 in binary is 1010 -> rightmost set bit flipped = 1000 = 8
Ex. 11 in binary is 1011 -> rightmost set bit flipped = 1010 = 10

The way we do this in code is:
1. Take the two's complement of i (flip all the bits and add one)
2. AND this result with the original number
3. Subtract this result from the original number

* How do we fill the BIT with the appropriate numbers? *

            0

3      5        10          19

       -1      5   9      7    9

                    -3           3

0 is a dummy node, so always filled with 0
Ex. Slot 1 = 0 + 2^0, so this stores the sum of the next 1 element starting at 0, i.e. the subarray sum of indices (0,0), which is 3
Ex. Slot 2 = 0 + 2^1, so this stores the sum of the next 2 elements starting at 0, i.e. the subarray sum of indices (0,1), which is 5
Ex. Slot 3 = 2^1 + 2^0, so this stores the subarray sum of the next 1 element starting at 2, i.e. the subarray sum of indices (2,2), which is -1
Ex. Slot 4 = 0 + 2^2, so this stores the subarray sum of the next 4 elements starting at 0, i.e. the subarray sum of indices (0,3), which is 10
Ex. Slot 7 = 2^2 + 2^1 + 2^0, so this stores the subarray sum of the next 1 element starting at (2^2 + 2^1) = 6, i.e. the subarray sum of indices (6,6), which is -3
Ex. Slot 8 = 0 + 2^3, so this stores the sum of the next 8 elements starting at 0, i.e. the subarray sum of indices (0,7), which is 19

Notice that the examples described above are not very efficient. The efficient way to update the value of element i in the original array into our BIT is:
1. Start at the (i+1)th node in the tree and update it with the difference in values (if we are just creating our BIT, then it starts with all 0s)
2. Get the next node that should be updated and update it, until there are no further nodes to be updated (i.e. the next node exceeds the total number of nodes we need)

To get the next node that should be updated:
1. Take the two's complement of i (flip all the bits and add one)
2. AND this result with the original number
3. Add this result to the original node

This takes O(log(N)) time for each number in the original array we are updating. Thus, it takes O(Nlog(N)) time to create a BIT.

* How do we use the BIT to compute the sum over an interval? *

Ex. Let's find the sum of indices (0,5), inclusive. We go to node 6, which gives us the sum over (4,5). We find its parent, which is node 4, and gives us the sum over (0,3). We find its parent, which is the root. Summing the values of these nodes gives us the sum over (0,5), which is 19.

*/

class Main {
  public static void main(String[] args) {
    BinaryIndexedTree bit = new BinaryIndexedTree(11);
    bit.add(3, 0);
    bit.add(2, 1);
    bit.add(-1, 2);
    bit.add(6, 3);
    bit.add(5, 4);
    bit.add(4, 5);
    bit.add(-3, 6);
    bit.add(3, 7);
    bit.add(7, 8);
    bit.add(2, 9);
    bit.add(3, 10);

    System.out.println(bit.sum(5));
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