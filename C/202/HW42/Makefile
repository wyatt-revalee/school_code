
CC = gcc
CARGS = -Wall -g -lm

all: bst word_counts_generic int_example

bst: bst.c /u1/h0/jkinne/public_html/cs202-f2019/code/data_structures/binary_tree/bst.h
	$(CC) $(CARGS) -c bst.c -o bst.o

word_counts_generic: bst.o word_counts_generic.c
	$(CC) $(CARGS) bst.o word_counts_generic.c -o word_counts_generic

bst_words: bst_words.c bst_words.h
	$(CC) $(CARGS) -c bst_words.c -o bst_words.o

word_counts: bst_words.o word_counts.c
	$(CC) $(CARGS) bst_words.o word_counts.c -o word_counts

int_example: int_example.c bst.o
	$(CC) $(CARGS) bst.o int_example.c -o int_example
