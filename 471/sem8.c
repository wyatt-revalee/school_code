/*
* Reader/Writers
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#include <pthread.h>
#include <semaphore.h>

#define MILLION     5000000

#define NREADERS    10
#define NWRITERS     3
#define NTHREADS  (NREADERS + NWRITERS)

int nreaders = 0;
sem_t mutex;        // protect nreaders
sem_t roomEmpty;

void *threadReader(void *nothing);
void *threadWriter(void *nothing);

int main(int argc, char *argv[])
{
    pthread_t th[NTHREADS];
    int numbers[NTHREADS];
    double x, y;


    sem_init(&mutex, 0, 1);         // protect access to nreaders
    sem_init(&roomEmpty, 0, 1);     // prevent writers from entering a non-empty room and
                                    // prevent readers from entering whena writer is in the room
    for( int i = 0; i < NTHREADS; i++)
        numbers[i] = (i < NREADERS) ? i : i - NREADERS;

    for( int i = 0; i < NTHREADS; i++)
        if(i < NREADERS)
            pthread_create(&th[i], 0, (void *) threadReader, &numbers[i]);
        else
            pthread_create(&th[i], 0, (void *) threadWriter, &numbers[i]);


    for( int i = 0; i < NTHREADS; i++)
            pthread_join(th[i], 0);

    return 0;

}

void *threadReader(void *nothing)
{

    int mynumber;

    mynumber = *(int *) nothing;

    for(;;){
        usleep(random() % MILLION);     // simulate doing non-critical work

        sem_wait(&mutex);
            nreaders++;
            if(nreaders ==1)
                sem_wait(&roomEmpty);
        sem_post(&mutex);

        printf("reader %d has entered the critical section\n", mynumber);

        /* critical code */
        usleep(random() % MILLION);     // simulate time to do work in critical section
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

    for(;;){
        usleep(random() % MILLION);    // simulate doing non-critical work

        sem_wait(&roomEmpty);
            printf("writer %d has entered the critical section\n", mynumber);
            /* critical code */
            usleep(random() % MILLION);     // simulate time to do work in critical section
            // end of critical section
        sem_post(&roomEmpty);

        printf("writer %d has left the critical section\n", mynumber);

    }

    pthread_exit(0);
}
