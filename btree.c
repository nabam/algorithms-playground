/*
*/

#include "btree.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

btree_node* btree_node_create(int m, size_t s) {
  btree_node *node = malloc(sizeof(btree_node));
  node->children = malloc(sizeof(btree_node*) * m);
  node->keys = malloc(s * (m - 1));
  node->parent = NULL;
  node->allocated = 0;
  node->key_size = s;

  for (int i = 0; i < m; i++) {
    node->children[i] = NULL;
  }

  return node;
}

void btree_node_destroy(btree_node* node) {
  free(node->children);
  free(node->keys);
  free(node);
}

void btree_destroy_recursively(btree_node* node) {
  if (node == NULL) return;

  for (int i = 0; i < node->allocated + 1; i++) {
    btree_destroy_recursively(node->children[i]);
  }

  btree_node_destroy(node);
}

void btree_destroy(btree* tree) {
  btree_destroy_recursively(tree->head);
  free(tree);
}

btree* btree_create(int m, size_t s) {
  btree *tree = malloc(sizeof(btree));
  tree->head = btree_node_create(m, s);
  tree->m = m;

  return tree;
}

btree_node* btree_find_node(btree_node* node, void* key, int (*cmp)(void* a, void* b)) {
  int i = 0;

  for (i; i < node->allocated; i++) {
    if (!cmp(key, (node->keys + node->key_size * i))) {
      return node->children[i];
    }
  }
  return node->children[i];
}

void btree_insert(btree* tree, void* key, int (*cmp)(void* a, void* b)) {
  btree_node *node, *child;
  child = tree->head;

  do {
    node = child;
    child = btree_find_node(child, key, cmp);
  } while (child != NULL);

  if (node->allocated < tree->m - 1) {
    btree_node_insert(node, key, cmp);
  } else {
    btree_split(tree, node, key, cmp, NULL, NULL);
    btree_node_destroy(node);
  }
}

void btree_split(btree* tree, btree_node* node, void* key, int (*cmp)(void* a, void* b),
                 btree_node* l, btree_node* r) {

  int n_keys = node->allocated + 1;
  int med = n_keys >> 1;
  void* keys = malloc(node->key_size * n_keys);
  btree_node** children = malloc(sizeof(btree_node*) * (n_keys + 1));
  btree_node* parent = node->parent;
  btree_node *left, *right;

  int j = 0, i = 0;
  while(j < node->allocated && cmp(key, (node->keys + node->key_size * i))) {
    children[i] = node->children[j];
    memcpy(keys + node->key_size * i++,
           node->keys + node->key_size * j++,
           node->key_size);
  }

  children[i] = l;
  memcpy(keys + node->key_size * i++,
     key,
     node->key_size);
  children[i] = r;

  while(i < n_keys) {
    children[i + 1] = node->children[j + 1];
    memcpy(keys + node->key_size * i++,
           node->keys + node->key_size * j++,
           node->key_size);
  }

  if (parent == NULL) {
    parent = btree_node_create(tree->m, node->key_size);
  }

  left = btree_node_create(tree->m, node->key_size);
  for (i = 0; i < med; i++) {
    left->parent = parent;
    memcpy(left->keys + node->key_size * i,
           keys + node->key_size * i,
           node->key_size);
    left->children[i] = children[i];
    if (children[i] != NULL) children[i]->parent = left;
  }
  left->allocated = i;
  left->children[i] = children[i];
  if (children[i] != NULL) children[i]->parent = left;

  right = btree_node_create(tree->m, node->key_size);
  for (i = med + 1, j = 0; i < n_keys; i++, j++) {
    right->parent = parent;
    memcpy(right->keys + node->key_size * j,
           keys + node->key_size * i,
           node->key_size);
    right->children[j] = children[i];
    if (children[i] != NULL) children[i]->parent = right;
  }
  right->allocated = j;
  right->children[j] = children[i];
  if (children[i] != NULL) children[i]->parent = right;

  if (parent->allocated < tree->m - 1) {
    int pos = btree_node_insert(parent, keys + med * node->key_size, cmp);
    for (int i = parent -> allocated; i > pos + 1; i--) {
      parent->children[i] = parent->children[i - 1];
    }

    parent->children[pos] = left;
    parent->children[pos + 1] = right;

    if (parent->parent == NULL) {
      tree->head = parent;
    }
  } else {
    btree_split(tree, parent, keys + med * node->key_size, cmp, left, right);
  }

  free(keys);
  free(children);
}

int btree_node_insert(btree_node* node, void* key, int (*cmp)(void* a, void* b)) {
  int i = node->allocated;
  for (i; i > 0; i--) {
    if (cmp(key, (node->keys + node->key_size * (i - 1)))) {
      break;
    }
    memcpy(node->keys + node->key_size * i,
           node->keys + node->key_size * (i - 1),
           node->key_size);
  }
  memcpy(node->keys + node->key_size * i,
         key,
         node->key_size);

  node->allocated++;
  return i;
}

/* for testing */
int cmp_int(void* a, void* b) {
  return *(int *)a > *(int *)b;
}

char* array_dump(void* str, int len) {
  int i, buffer = 255;
  char *result = malloc(buffer*sizeof(char)), *pos = result;

  *pos++ = '[';

  for (i = 0; i < len && pos < result + buffer - 1; i++) {
    pos += snprintf(pos, result - pos, "%d, ", *(int*)(str + sizeof(int) * i));
  }

  if (i > 0) {
    *(pos - 2) = ']';
    *(pos - 1) = '\0';
  } else {
    *pos++ = ']';
    *pos = '\0';
  }
  return result;
}

char* tree_dump(btree_node* node, int depth) {
  btree_node* cur = NULL;

  if (node == NULL) return NULL;

  for (int i = 0; i < depth; i++) printf("  ");
  char* d = array_dump(node->keys, node->allocated);
  puts(d);
  free(d);

  for (int i = 0; i < node->allocated + 1; i++) {
    tree_dump(node->children[i], depth + 1);
  }
}

int main() {
  btree* tree = btree_create(20, sizeof(int));
  for(int i = 0; i < 1000; i++) {
    int r = rand() >> 20;
    btree_insert(tree, &r, &cmp_int);
  }
  tree_dump(tree->head, 0);
  btree_destroy(tree);
  return EXIT_SUCCESS;
}
