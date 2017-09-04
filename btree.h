/*
*/

#include <stdlib.h>

typedef struct btree_node {
  void* keys;
  int allocated;
  size_t key_size;
  struct btree_node** children;
  struct btree_node* parent;
} btree_node;

typedef struct btree {
  struct btree_node* head;
  int m;
} btree;

btree_node* btree_node_create(int, size_t);
void btree_node_destroy(btree_node*);
int btree_node_insert(btree_node*, void*, int (*)(void*, void*));
int btree_node_get_pos(btree_node*, void*, int (*)(void*, void*));

btree* btree_create(int, size_t);
void btree_insert(btree*, void*, int (*)(void*, void*));
void btree_split(btree*, btree_node*, void*, int (*)(void*, void*), btree_node*, btree_node*);
btree_node* btree_find_node(btree_node*, void*, int (*)(void*, void*));
void btree_destroy(btree*);
