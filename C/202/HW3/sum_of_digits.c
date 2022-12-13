#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {

    int n;
    int sum;
    scanf("%d", &n);
    // I'm not sure if this if statement is necessary.
    // Hackerrank has constraints listed, so I figured they should be added.
    if(10000 <= n <= 99999) {
        while (n>0) {
            sum += (n%10);
            n=n/10;
        }
    }
    printf("%d", sum);
    return 0;
}
