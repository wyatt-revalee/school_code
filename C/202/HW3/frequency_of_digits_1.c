#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    int* data = (int*) malloc(10 * sizeof(int));
    char c;

    for(int i = 0; i < 10; i++)
        *(data+i) = 0;

    while(scanf("%c", &c) == 1)
        if(c >= '0' && c <= '9')
            (*(data+(c-'0')))++;

    for(int i = 0; i < 10; i++)
        printf("%d ", *(data+i));

    return 0;
}
