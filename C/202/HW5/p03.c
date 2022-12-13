/* Problem 3: Fill in function itobin. */

#include <stdio.h>
#include <string.h>

char *itobin(unsigned int x, char *buffer);

int main(int argc, char *argv[])
{
  unsigned int x;
  char buffer[100];
  scanf("%d", &x);
  itobin(x, buffer);
  return 0;
}

/* Takes an integer and a string buffer as arguments. Convert the integer to binary,
 * placing the binary string in buffer. Assume that buffer has already been allocated
 * an appropriate ammount of memory to hold 32 bits. Reminder: It will be your job to place
 * the null byte in the appropriate place. Returns buffer.*/
char *itobin(unsigned int x, char *buffer)
{
  int y = x;
  int i = 0;
  x = x | 2147483648;
  if (x < 2147483648) {
    x = x ^ 2147483648;
  }
  while(x > 0) {
    buffer[i] = x % 2;
    x = x / 2;
    i++;
  }
  if (y < 2147483648) {
    buffer[31] = 0;
  }
  for(int j = i-1; j >= 0; j--) {
    printf("%d", buffer[j]);

  }
  printf("\n");
}
