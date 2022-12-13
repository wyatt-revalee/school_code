
/*
 *  Reader/Writer Problem -- no starvation for writers (as a group)
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <math.h>

#include <pthread.h>
#include <semaphore.h>

#include <time.h>
#include <sys/time.h>

#define MILLION   5000000

#define NREADERS  13
#define NWRITERS   3
#define NTHREADS (NREADERS + NWRITERS)

int nreaders = 0;
sem_t mutex;               // protect nreaders variable
sem_t roomEmpty;           // blocks when thread(s) are in critical section(s)
sem_t turnstile;           // allows arriving writers to enter critical section before readers that arrive later

struct timeval start, end; //Time recording variables
long readerWaitTime, writerWaitTime, seconds;

void *threadReader(void *nothing);  // function for the reader thread
void *threadWriter(void *nothing);  // function for the writer thread

int main(int argc, char *argv[])
{
    pthread_t th[NTHREADS];            // pthread's thread data structure
    int numbers[NTHREADS];             // array with thread id's
    double x,y;

    sem_init(&turnstile, 0, 1);        //
    sem_init(&mutex, 0, 1);            // protect access to total
    sem_init(&roomEmpty, 0, 1);        // prevent writers from entering a non-empty room and
                                       // prevent readers from entering when a writer is in the room

    for(int i = 0 ; i < NTHREADS ; i++)
        numbers[i] = (i < NREADERS) ? i : i - NREADERS;  // x = y if condition else z

    for(int i = 0 ; i < NTHREADS ; i++)
        if(i < NREADERS)
            pthread_create(&th[i], 0, (void *) threadReader, &numbers[i]);
        else
            pthread_create(&th[i], 0, (void *) threadWriter, &numbers[i]);

    for(int i = 0 ; i < NTHREADS ; i++)
        pthread_join(th[i], 0);

    printf("Mean reader wait time was %ld microseconds\n", readerWaitTime);
    printf("Mean writer wait time was %ld microseconds\n", writerWaitTime);

    return 0;
}

void *threadReader(void *nothing)
{
    int mynumber;

    mynumber = *(int *) nothing;

    for(int i = 0; i < 10; i++){
        usleep(random() % MILLION);  // simulate doing non-critical work

        gettimeofday(&start, NULL);

        sem_wait(&turnstile);
        sem_post(&turnstile);

        sem_wait(&mutex);
            nreaders++;
            if(nreaders == 1)
                sem_wait(&roomEmpty);
        sem_post(&mutex);

        gettimeofday(&end, NULL);

        seconds = (end.tv_sec * 1000000 + end.tv_usec) - (start.tv_sec * 1000000 + start.tv_usec);
        readerWaitTime += seconds;

        printf("reader %d has entered the critical section\n", mynumber);

// beginning of critical section

        usleep(random() % MILLION);  // simulate time to do work in critical section

// end of critical section

        printf("reader %d has left the critical section\n", mynumber);

        sem_wait(&mutex);
            nreaders--;
            if(nreaders == 0)
                sem_post(&roomEmpty);
        sem_post(&mutex);

    }

    pthread_exit(0);
}


void *threadWriter(void *nothing)
{
    int mynumber;

    mynumber = *(int *) nothing;

    for(int i = 0; i < 10; i++){
        usleep(random() % MILLION);   // simulate doing non-critical work

        gettimeofday(&start, NULL);

        sem_wait(&turnstile);
            sem_wait(&roomEmpty);
        sem_post(&turnstile);

        gettimeofday(&end, NULL);

        seconds = (end.tv_sec * 1000000 + end.tv_usec) - (start.tv_sec * 1000000 + start.tv_usec);
        writerWaitTime += seconds;

            printf("writer %d has entered the critical section\n", mynumber);

// beginning of writer's critical section

            usleep(random() % MILLION);   // simulate doing work

// end of writer's critical section

        sem_post(&roomEmpty);

        printf("writer %d has left the critical section\n", mynumber);

    }

    pthread_exit(0);
}

