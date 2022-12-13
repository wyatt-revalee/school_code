/* Problem 1: Fill in the function count1. */

#include <stdio.h>

unsigned int count1(unsigned int x);

int main(int argc, char *argv[])
{
  unsigned int x;
  scanf("%u", &x);
  printf("%u\n", count1(x));
  return 0;
}

/* Takes an unsigned int, x, as an argument. Count the number of 1's in the binary representation
 * of x. Return the corresponding unsigned int that has the same number of 1's in its most
 * significant bits. */
unsigned int count1(unsigned int x)
{
  int binary[32];
  int maxBinary[32];
  int maxInt = 0;
  int oneCount = 0;
  int i = 0;
  while(x > 0) {                      // Convert decimal int to binary, count ones
    binary[i] = x % 2;
    if(x%2) {
      oneCount ++;
    }
    x = x / 2;
    i++;
  }
  for(int k = 0; k < 32; k++) {      // Move the ones to the most significant bits
    if (oneCount > 0) {
      maxBinary[k] = 1;
    }
    else {
      maxBinary[k] = 0;
    }
    oneCount--;
  }
  for(int l = 0; l < 32; l++) {     // Convert binary arr into decimal int
    maxInt <<= 1;
    maxInt += maxBinary[l];
  }
  return maxInt;
}
