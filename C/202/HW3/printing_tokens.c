#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {

    char *s;
    s = malloc(1024 * sizeof(char));
    while(scanf("%99s", s)==1) {
        printf("%s\n", s);
    }
    s = realloc(s, strlen(s) + 1);
    return 0;
}
