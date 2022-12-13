/*
* Barrier - multiple threads meet at some location in the code
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <pthread.h>
#include <semaphore.h>

#define NTHREADS    10

sem_t mutex, turnstile;
int count = 0;

void *threadX(void *nothing);

int main(int argc, char *argv[])
{
    pthread_t th[NTHREADS];
    int numbers[NTHREADS];

    srandom(getpid());

    sem_init(&mutex, 0, 1);          // protect access to count
    sem_init(&turnstile, 0, 0);      // enable threads to proceed to job 2

    for( int i = 0; i < NTHREADS; i++)
        numbers[i] = i+1;

    for( int i = 0; i < NTHREADS; i++)
        pthread_create(&th[i], 0, (void *) threadX, &numbers[i]);


    for( int i = 0; i < NTHREADS; i++)
            pthread_join(th[i], 0);

    return 0;

}

void *threadX(void *nothing)
{

    int mynumber;

    mynumber = *(int *) nothing;

    for(int reps=0; reps<1; reps++){

        printf("thread %d doing job 1\n", mynumber);
        usleep(random() % 100000);      // simulate doing job 1

    /*
     * increment a variable
     * 1. move old value from memory to CPU
     * 2. adding one to value in the CPU
     * 3. storing new value back to memory
     */


        sem_wait(&mutex);
            count++;
        sem_post(&mutex);


        if(count == NTHREADS)
            sem_post(&turnstile);

        sem_wait(&turnstile);      // wait until all jobs have posted to turnstile (count == NTHREADS)
        sem_post(&turnstile);      // post that job is done

        printf("thread %d doing job 2\n", mynumber);
        usleep(random() % 1000000);      // simulate doing job 2
    }
    pthread_exit(0);
}
