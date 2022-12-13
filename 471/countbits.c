#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{

    int x = argv[1];
    printbinary(x);

    return 0;
}

void printbinary(int x)
{
    if (a > 1)
        printbinary(a/2);

    printf("%d\n", a % 2);
}
