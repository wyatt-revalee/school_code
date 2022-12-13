// scanning text and counting word frequencies
// note - can use stripWords to clean up words before sending to this program
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>

#include "/u1/h0/jkinne/public_html/cs202-f2019/code/data_structures/binary_tree/bst.h"


/* Begin word_counts_t type declaration and functions for using */

int compare_int(void *data1, int data1_size, void *data2, int data2_size) {
  int *d1 = (int *) data1,
    *d2 = (int *) data2;

  return (*d1 - *d2);
}

void print_int(void *data, int data_size, int depth) {
  int *num = (int *) data;
  printf("%*s%d\n", depth, "", *num);
}

void free_int(void *data, int data_size) {
  ;
}

/* End word_counts_t type declaration and functions for using */




int main(int argc, char * argv[]) {
  tree_t * root = NULL;

  tree_t * p;

  int num;
  
  while (scanf("%d", &num) == 1) {
    int delete = 0;
    
    if (num < 0) { // negative is a code for deleting
      num *= -1;
      delete = 1;
    }

    p = bst_lookup(root, &num, sizeof(num));

    if (p == NULL && ! delete) {
      root = bst_insert(root,
			&num, sizeof(num), FLAG_DO_NOT_REBALANCE, 
			compare_int, print_int, free_int);
    }

    if (p != NULL && delete) {
      root = bst_delete(root, p, 0);
    }
  }

  bst_print(root, -1, FLAG_TREE | FLAG_SUMMARY | FLAG_SMALLEST_FIRST);

  return 0;
}
