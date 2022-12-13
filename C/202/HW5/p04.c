/* Problem 4: Fill in swap_bytes function */

#include <stdio.h>

unsigned short swap_bytes(unsigned short x);

int main(int argc, char *argv[])
{
  unsigned short x;
  scanf("%hu", &x);
  printf("0x%04x -> 0x%04x\n", x, swap_bytes(x));
  return 0;
}

/* Takes an unsigned short as a parameter. Swap the two bytes in x using
 * bit operations and return the result. e.g. 0x4567 becomes 0x6745 */
unsigned short swap_bytes(unsigned short x)
{
  return ((x & 0xff) << 8) | (x >> 8);  //Clear "left" side using a bitmask and &, then shift right side to left
}                                       // Then adds back the cleared side to the right, using |.
