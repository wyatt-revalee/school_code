#include <stdio.h>
#include <stdlib.h>

int k;

void swap(int *i, int *j)
{
    int temp = *i;
    *i = *j;
    *j = temp;
}

void permute(int index, int *arr, int n)
{
    if (index == n - 1)
    {
        int fixCount = 0;
        for (int i = 0; i < n; i++)
        {
            if(arr[i] == i+1)
                fixCount++;
        }
        if(fixCount == k)
        {
            printf("[");
            for (int i = 0; i < n; ++i)
            {
                if(i == n-1)
                    printf("%d", arr[i]);
                else
                    printf("%d,", arr[i]);
            }
            printf("]\n");
        }
        return;
    }
    for (int i = index; i < n; i++)
    {
        swap(arr + index, arr + i);
        permute(index + 1, arr, n);
        swap(arr + i, arr + index);
    }
    return;
}

int main()
{
    int n;
    printf("n:");
    if (scanf("%d", &n) != 1)
        exit(1);
    printf("k:");
    if (scanf("%d", &k) != 1)
        exit(1);
    if(k > n){
        printf("k must be <= n");
        exit(1);
    }
    int arr[n];
    for (int i = 0; i < n; ++i)
        arr[i] = i + 1;
    permute(0, arr, n);
    return 0;
}