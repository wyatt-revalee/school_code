#include <stdio.h>

int main()
{

    int n;
    int k;

    printf("n:");
    scanf("%d", &n);
    printf("k:");
    scanf("%d", &k);

    if(k > n){
        printf("k must be <= n");
        return 0;
    }
    
    int numbers[n];
    for (int i = 1; i <= n; i++)
        numbers[i-1] = i;
    
    for(int i = 0; i < sizeof(numbers)/4; i++)
        printf("i:%d %d\n", i, numbers[i]);

    return 0;
}
