/* Problem 2: Fill in the functions set and clear. */

#include <stdio.h>

unsigned char set(unsigned char x, int i);
unsigned char clear(unsigned char x, int i);

int main(int argc, char *argv[])
{
  unsigned char x;
  scanf("%hhu", &x);
  printf("%u\n", set(x, 2));
  printf("%u\n", clear(x, 4));
  return 0;
}

/* Takes both an unsigned char, x, and an integer, i, representing a bit index.
 * Set the bit in x at index i (starting at 0) to 1 and return the result. */
unsigned char set(unsigned char x, int i)
{
  int n = (x | 4);
  return n;
}

/* Takes both an unsigned char, x, and an integer, i, representing a bit index.
 * Set the bit in x at index i (starting at 0) to 0 and return the result. */
unsigned char clear(unsigned char x, int i)
{
  int n = (x & 4294967279);
  return n;
}
