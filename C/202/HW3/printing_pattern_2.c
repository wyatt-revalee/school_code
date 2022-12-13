#include <stdio.h>

int main()
{

    int n;
    scanf("%d", &n);
    int length = n*2 - 1;
    for(int i = 0; i < length; i++){
        for(int j=0;j<length;j++){
            int min = i < j ? i : j;
            min = min < length-i ? min : length-i-1;
            min = min < length-j-1 ? min : length-j-1;
            printf("%d ", n-min);
        }
        printf("\n");
    }
    return 0;
}
