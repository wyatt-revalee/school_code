/*
* Rendezvous - 2 threads/processes
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define NTHREADS    2

sem_t s1, s2;          /* a semaphore */

int shared_var = 0;

void *thread1(void *nothing);
void *thread2(void *nothing);

int main(int argc, char *argv[])
{

    pthread_t th[NTHREADS];
    int numbers[NTHREADS];


    srandom(getpid());

    sem_init(&s1, 0, 0);      // indicate that thread1 is done with job 1
    sem_init(&s2, 0, 0);      // indicate that thread2 is done with job 1

    for( int i = 0; i < NTHREADS; i++)
        numbers[i] = i+1;

    pthread_create(&th[0], 0, (void *) thread1, &numbers[0]);
    pthread_create(&th[1], 0, (void *) thread2, &numbers[1]);


    for( int i = 0; i < NTHREADS; i++)
            pthread_join(th[i], 0);

    printf("%d\n", shared_var);

    return 0;

}

void *thread1(void *nothing)
{

    int mynumber;

    mynumber = *(int *) nothing;

    usleep(random() % 100000);      // work to do before starting main job
    printf("thread %d doing job 1\n", mynumber-1);
    usleep(random() % 100000);      // work to do before starting main job

    sem_post(&s1);      // post that job1 is done
    sem_wait(&s2);      // wait until thread2's job1 is done

    printf("thread %d doing job 2\n", mynumber-1);
    usleep(random() % 1000);      // work to do before starting main job

    pthread_exit(0);

}

void *thread2(void *nothing)
{

    int mynumber;

    mynumber = *(int *) nothing;

    usleep(random() % 1000000);      // work to do before starting main job
    printf("thread %d doing job 1\n", mynumber-1);
    usleep(random() % 1000000);      // work to do before starting main job

    sem_post(&s2);      // post that job1 is done
    sem_wait(&s1);      // wait until thread1's job1 is done

    printf("thread %d doing job 2\n", mynumber-1);
    usleep(random() % 1000);      // work to do before starting main job

    pthread_exit(0);

}
