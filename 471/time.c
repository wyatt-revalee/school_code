 #include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <time.h>
#include <sys/time.h>

#define MILLION 1000000
int main(int argc, char *argv[])
{

    struct timeval v1, v2;
    long microsecs;

    gettimeofday(&v1, 0);
    printf("%ld, %ld \n", v1.tv_sec, v1.tv_usec);

    for(int i = 0; i < 100000; i++){
        int j;

        j += i;
    }
    gettimeofday(&v2, 0);
    microsecs = MILLION * (v2.tv_sec - v1.tv_sec) + (v2.tv_usec - v1.tv_usec);
    printf("%ld, %ld \n", v2.tv_sec, v2.tv_usec);
    printf("%ld microseconds\n", microsecs);

    return 0;
}
