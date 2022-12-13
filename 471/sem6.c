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

sem_t mutex, turnstile1, turnstile2;
int count = 0;

void *threadX(void *nothing);

int main(int argc, char *argv[])
{
    pthread_t th[NTHREADS];
    int numbers[NTHREADS];

    srandom(getpid());

    sem_init(&mutex, 0, 1);           // protect access to count
    sem_init(&turnstile1, 0, 0);      // barrier after job 1
    sem_init(&turnstile2, 0, 1);      // barrier after job 2

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

    for(int reps=0; reps<3; reps++){

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
            if(count == NTHREADS) {
                sem_wait(&turnstile2);
                sem_post(&turnstile1);
            }
        sem_post(&mutex);

        sem_wait(&turnstile1);      // wait until all jobs have posted to turnstile (count == NTHREADS)
        sem_post(&turnstile1);

        printf("thread %d doing job 2\n", mynumber);
        usleep(random() % 1000000);      // simulate doing job 2

        sem_wait(&mutex);
            count--;
            if(count == 0) {
                sem_wait(&turnstile1);
                sem_post(&turnstile2);
            }
        sem_post(&mutex);

        sem_wait(&turnstile2);      // wait until all jobs have posted to turnstile (count == 0)
        sem_post(&turnstile2);

    }
    pthread_exit(0);
}
