#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include "/u1/h0/jkinne/public_html/cs202-f2019/code/data_structures/binary_tree/bst.h"

// find where word is in the tree and return its parent
// if not in the tree then return what would be parent if
// we inserted
tree_t *bst_lookup_parent(tree_t *root, void *data, int data_size) {
  if (root == NULL) return NULL;

  // look for word in the tree.  keep track of current
  // and its parent as we go.
  tree_t *current=root, *parent = NULL;
  while (current  != NULL) {
    int result = current->compare(data, data_size, current->data, current->data_size);
    if (result == 0) return parent; // found the word in the tree

    parent = current;

    if (result < 0)
      current = current->left;
    else
      current = current->right;
  }

  return parent;
}

// make a new node - allocate memory, set right/left = NULL,
//   put in word and number
tree_t *bst_make_node(void *data, int data_size,
		      int (*compare)(void *, int, void *, int),
		      void (*print)(void *, int, int),
		      void (*free)(void *, int)) {
  // create a new node
  tree_t *t = (tree_t *) malloc(sizeof(tree_t));
  assert(t != NULL);
  t->left = t->right = NULL;

  t->data = malloc(data_size);
  memcpy(t->data, data, data_size);
  t->data_size = data_size;

  t->compare = compare;
  t->print = print;
  t->free = free;

  return t;
}


// free memory from the node
void bst_free_node(tree_t *t) {
  if (t == NULL) return;
  if (t->data != NULL) t->free(t->data, t->data_size);
  free(t);
}

// HW42 - if allow_duplicate is non-zero, still do the insert if duplicate, and insert duplicates on left
tree_t *bst_insert(tree_t *root,
		   void *data, int data_size, unsigned int flags,
		   int (*compare)(void *, int, void *, int),
		   void (*print)(void *, int, int),
		   void (*free)(void *, int)) {
  if (data == NULL) return root; // sanity check

  tree_t *t = bst_make_node(data, data_size, compare, print, free);

  tree_t * curr = t->parent;
  while(curr != NULL) {
    break;
  }

  // NULL root is empty tree, so t is now the root, return it
  if (root == NULL) return t;

  // find where should be inserted (lookup)
  tree_t *parent = bst_lookup_parent(root, data, data_size);
  t->parent = parent;
  if (parent == NULL) {
    // root != NULL but parent==NULL means s is in the root
    bst_free_node(t);
    return root;
  }

  // there is a parent, let's see...
  int result = parent->compare(data, data_size, parent->data, parent->data_size);
  if (result < 0 && parent->left == NULL) // put on the left
    parent->left = t;
  else if (result > 0 && parent->right == NULL) // put on the right
    parent->right = t;
  else // already in the tree
    bst_free_node(t);

  // HW42 - check whether node is balanced or not (need max_depth set
  //  properly in order to do this), and if not balanced o
  //  AVL rotation(s).
  //  See https://www.geeksforgeeks.org/avl-tree-set-1-insertion/

  return root;
}


tree_t *bst_lookup(tree_t *root, void *data, int data_size) {
  tree_t *current=root;
  while (current  != NULL) {
    int result = current->compare(data, data_size, current->data, current->data_size);
    if (result == 0) break;

    if (result < 0)
      current = current->left;
    else
      current = current->right;
  }
  return current;
}

tree_t *bst_delete(tree_t *root, tree_t *p, unsigned int flags) {
  // HW42 - needs to be completed
  /*
    Let p be the node to delete.
    Let p_parent be p's parent.
    Cases
    1) p is a leaf
       p_parent->(left or right) = NULL
    2) p->left != NULL
       p_largest = largest in p->left subtree
       put p_largest in pword_counts
       p_largest->right = p->right
       p_largest->left = p->left
       somewhere in there, delete(p_largest) recursively
    3) p->left == NULL
       p_parent->(left or right) = p->right
    After that, free p
   */
  return root;
}

// helper function for bst_print, prints the tree
//  with the # spaces indicating depth
void bst_print__(tree_t *root, int depth) {
  if (root == NULL) return;

  bst_print__(root->left, depth+1);
  root->print(root->data, root->data_size, depth);
  bst_print__(root->right, depth+1);
}

// HW42 - modify bst_print so it uses parameters as described in bst.h
void bst_print(tree_t *root, int limit, unsigned int flags) {
  bst_print__(root, 0);
}

// HW42 - complete function as described in bst.h
void bst_map(tree_t *root, void (*fun)(tree_t *, void *), void *param) {
}
