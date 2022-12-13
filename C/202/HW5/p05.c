/* Problem 5: Fill in print_base_formula function */

#include <stdio.h>

void print_base_formula(int x, int base);

int main(int argc, char *argv[])
{
  int x;
  scanf("%d", &x);
  print_base_formula(x, 10);
  print_base_formula(x, 2);
  print_base_formula(x, 16);
  return 0;
}

/* Takes an int, x, as an argument. Print the base formula of x for the given
 * base. The function should work for all bases s.t. 1 <= base <= 16. For example,
 * if x = 25 and base = 10, the function should print "2 * 10 + 5 * 1". Alternatively,
 * if base = 2, the function should print "1 * 16 + 1 * 8". */
void print_base_formula(int x, int base)
{
  if      (base == 10) {
    while(x / 10 != 0) {
    }
  }
  else if (base == 2) {
    int oddOne     = x % 2;
    int ones   = (x % 16) -1;
    int sixteens = x / 16;
    printf("%d * 1 + %d * 8 + %d * 16\n", oddOne, ones, sixteens);
  }
  else if (base == 16) {
    int eights   = x % 16;
    int sixteens = x / 16;
    printf("%0x * 1 + %0x * 16\n", eights, sixteens);
  }
}
