#ifndef BST_H_
#define BST_H_

/*
  Binary search tree that uses a word as the key value and 
  includes a count as well.
 */

// HW42 - items that you need to complete or use for
//  HW42 are noted as such in the files (do a search for HW42 to find them)

typedef struct tree {
  void * data;
  int data_size;
  struct tree *left, *right,
    *parent;      // HW42 - should be a pointer to a node's parent, or NULL if the node is the root
  int max_height; // HW42 - should be the max height of this node's children, 0 for a leaf node
  
  int (*compare)(void *, int, void *, int); // comparison function for this data type
  void (*print)(void *, int, int); // function for printing
  void (*free)(void *, int);       // function for freeing data
} tree_t;

// if data is not in the tree, insert it.
// return the root of the tree (which is created if the tree is empty)
//
// HW42
//   FLAG_ALLOW_DUPLICATES - allow for duplicate keys (adding to left if ==)
//   FLAG_DO_NOT_REBALANCE - do not rotate/rebalance
#define FLAG_ALLOW_DUPLICATES  0x10
#define FLAG_DO_NOT_REBALANCE  0x20
tree_t *bst_insert(tree_t *root,
		   void *data, int data_size, unsigned int flags,
		   int (*compare)(void *, int, void *, int),
		   void (*print)(void *, int, int),
		   void (*free)(void *, int));

// if data is in the tree, return a pointer to the tree_t node
tree_t *bst_lookup(tree_t *root, void *data, int data_size);

// remove p from the tree
tree_t *bst_delete(tree_t *root, tree_t *p, unsigned int flags);

// print the tree.
//
// HW42 - modify bst_print so it uses these parameters
// limit - don't print more than this many (if -1 print them all)
// flags -
//         FLAG_SMALLEST_FIRST - print smallest ones first, otherwise largest ones first
//         FLAG_SUMMARY        - print summary info - # nodes, max depth, average depth.
//         FLAG_TREE           - make printout look like a tree (by using spaces for depth)
//         FLAG_DEBUG          - along with printing the data, for each node print it's pointer, parent pointer, and max_height
#define FLAG_SMALLEST_FIRST 0x01
#define FLAG_SUMMARY        0x02
#define FLAG_TREE           0x04
#define FLAG_DEBUG          0x08
void bst_print(tree_t *root, int limit, unsigned int flags);

// HW42
//
// When this function is called, it will take the second parameter
// as a function and traverse the tree with the function getting
// called for each node of the tree, and with that function getting the
// param as its second parameter
void bst_map(tree_t *root, void (*fun)(tree_t *, void *), void *param);

#endif