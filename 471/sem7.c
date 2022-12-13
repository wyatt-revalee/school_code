/*
* Compute PI: PI^2/6 = 1 + 1/2^2 + 1/3^2 + 1/4^2 + ...
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#include <pthread.h>
#include <semaphore.h>

#define N    10000000000L
#define NTHREADS        50

sem_t mutex;
double total = 0;

void *threadPI(void *nothing);

int main(int argc, char *argv[])
{
    pthread_t th[NTHREADS];
    int numbers[NTHREADS];
    double x, y;

#if 0
    for(long i = 1; i < N; i++) {
        x = (double) i;
        y = 1.0/(x*x);
        total += y;
    }
    printf("%.12lf\n", sqrt(6.0*total));
    exit(0);
#endif

    sem_init(&mutex, 0, 1);           // protect access to total

    for( int i = 0; i < NTHREADS; i++)
        numbers[i] = i+1;

    for( int i = 0; i < NTHREADS; i++)
        pthread_create(&th[i], 0, (void *) threadPI, &numbers[i]);


    for( int i = 0; i < NTHREADS; i++)
            pthread_join(th[i], 0);

    printf("%.12lf\n", sqrt(6.0*total));

    return 0;

}

void *threadPI(void *nothing)
{

    int mynumber;
    double x, y;
    double local_total;

    mynumber = *(int *) nothing;

    local_total = 0.0;
    for(long i = mynumber; i < N; i+= NTHREADS) {
        x = (double) i;
        local_total += 1.0/(x*x);
    }
    sem_wait(&mutex);
        total += local_total;
    sem_post(&mutex);

    pthread_exit(0);
}
