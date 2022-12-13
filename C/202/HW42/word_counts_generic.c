// scanning text and counting word frequencies
// note - can use stripWords to clean up words before sending to this program
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#include "/u1/h0/jkinne/public_html/cs202-f2019/code/data_structures/binary_tree/bst.h"

tree_t *root_by_count = NULL;

/* Begin word_counts_t type declaration and functions for using */
typedef struct word_counts {
  char *word; // the "key"
  int num;    // more "data"  
} word_counts_t;

int compare_word_counts(void *data1, int data1_size, void *data2, int data2_size) {
  word_counts_t *d1 = (word_counts_t *) data1,
    *d2 = (word_counts_t *) data2;

  return strcmp(d1->word, d2->word);
}

int compare_word_counts_int(void *data1, int data1_size, void *data2, int data2_size) {
  word_counts_t *d1 = (word_counts_t *) data1,
    *d2 = (word_counts_t *) data2;

  return d1->num - d2->num;
}

void print_word_counts(void *data, int data_size, int depth) {
  word_counts_t *wc = (word_counts_t *) data;
  printf("%*s%s : %d\n", depth, "", wc->word, wc->num);
}

void free_word_counts(void *data, int data_size) {
  if (data == NULL) return;
  word_counts_t *wc = (word_counts_t *) data;
  if (wc->word != NULL) free(wc->word);
  free(wc);
}

/* End word_counts_t type declaration and functions for using */


// insert everything from into to
void insert_by_count(tree_t *from, void *to) {
  if (from == NULL) return;

  tree_t ** copy_to_pp = (tree_t **) to;
  *copy_to_pp =  bst_insert(*copy_to_pp,
			    from->data, from->data_size,
			    FLAG_ALLOW_DUPLICATES,
			    compare_word_counts_int, print_word_counts, free_word_counts);
}


int main(int argc, char * argv[]) {
  tree_t * root = NULL;

  char s[100];
  tree_t * p;

  word_counts_t wc;
  wc.num = 1;
  
  while (scanf("%99s", s) == 1) {
    wc.word = s;
    p = bst_lookup(root, &wc, sizeof(wc));
    
    if (p != NULL)
      (((word_counts_t *) p->data)->num)++;
    else {
      wc.word = strdup(s); // put word on the heap before inserting
      root = bst_insert(root,
			&wc, sizeof(wc), 0, 
			compare_word_counts, print_word_counts, free_word_counts);
    }
  }

  bst_print(root, 10, FLAG_TREE | FLAG_SUMMARY);

  printf("\n");
  
  bst_map(root, insert_by_count, &root_by_count);
  bst_print(root_by_count, 50, 0);

  return 0;
}
