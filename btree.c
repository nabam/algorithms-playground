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
  /*printf("%p %p %p\n", (void*)node, node->keys, (void*)node->children);*/
  free(node->keys);
  free(node->children);
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
  btree_node *child = node, *result = node;

  while (child != NULL) {
    result = child;
    child = result->children[btree_node_get_pos(result, key, cmp)];
  }

  return result;
}

void btree_insert(btree* tree, void* key, int (*cmp)(void* a, void* b)) {
  btree_node *node, *child;
  node = btree_find_node(tree->head, key, cmp);

  if (node->allocated < tree->m - 1) {
    btree_node_insert(node, key, cmp);
  } else {

    btree_split(tree, node, key, cmp);
    btree_node_destroy(node);
  }
}

void btree_split(btree* tree, btree_node* node, void* key, int (*cmp)(void* a, void* b)) {
  void *mkey;
  int middle, pos;
  btree_node *parent, *left, *right;
  btree_node *l = NULL, *r = NULL;

  for (;;) {
    middle = (node->allocated + 1) >> 1;
    pos = btree_node_get_pos(node, key, cmp);
    parent = node->parent;

    if (parent == NULL) {
      parent = btree_node_create(tree->m, node->key_size);
    }

    left = btree_node_create(tree->m, node->key_size);
    left->parent = parent;

    right = btree_node_create(tree->m, node->key_size);
    right->parent = parent;

    if (pos < middle) {
      memcpy(left->keys,
             node->keys,
             node->key_size * pos);
      memcpy(left->children,
             node->children,
             sizeof(btree_node*) * pos);

      memcpy(left->keys + node->key_size * (pos + 1),
             node->keys + node->key_size * pos,
             node->key_size * (middle - 1 - pos));
      memcpy(left->children + pos + 2,
             node->children + pos + 1,
             sizeof(btree_node*) * (middle - 1 - pos));

      memcpy(right->keys,
             node->keys + node->key_size * middle,
             node->key_size * (node->allocated - middle));
      memcpy(right->children,
             node->children + middle,
             sizeof(btree_node*) * (node->allocated - middle + 1));

      memcpy(left->keys + node->key_size * pos,
             key,
             node->key_size);
      left->children[pos] = l;
      left->children[pos + 1] = r;

      mkey = node->keys + node->key_size * (middle - 1);
    } else if (pos > middle) {
      int rpos = pos - middle - 1;

      memcpy(left->keys,
             node->keys,
             node->key_size * middle);
      memcpy(left->children,
             node->children,
             sizeof(btree_node*) * (middle + 1));

      memcpy(right->keys,
             node->keys + node->key_size * (middle + 1),
             node->key_size * rpos);
      memcpy(right->children,
             node->children + middle + 1,
             sizeof(btree_node*) * rpos);

      memcpy(right->keys + node->key_size * (rpos + 1),
             node->keys + node->key_size * pos,
             node->key_size * (node->allocated - pos));
      memcpy(right->children + rpos + 2,
             node->children + pos + 1,
             sizeof(btree_node*) * (node->allocated - pos));

      memcpy(right->keys + node->key_size * (rpos),
             key,
             node->key_size);
      right->children[rpos] = l;
      right->children[rpos + 1] = r;

      mkey = node->keys + node->key_size * middle;
    } else {
      memcpy(left->keys,
             node->keys,
             node->key_size * middle);
      memcpy(left->children,
             node->children,
             sizeof(btree_node*) * middle);

      memcpy(right->keys,
             node->keys + node->key_size * middle,
             node->key_size * (node->allocated - middle));
      memcpy(right->children + 1,
             node->children + middle + 1,
             sizeof(btree_node*) * (node->allocated - middle));

      left->children[middle] = l;
      right->children[0] = r;
      mkey = key;
    }

    left->allocated = middle;
    right->allocated = node->allocated - middle;

    for (int i = 0; i <= left->allocated; i++) {
      if (left->children[i] != NULL) left->children[i]->parent = left;
    }

    for (int i = 0; i <= right->allocated; i++) {
      if (right->children[i] != NULL) right->children[i]->parent = right;
    }

    if (parent->allocated < tree->m - 1) {
      int pos = btree_node_insert(parent, mkey, cmp);
      memmove(parent->children + pos + 1,
              parent->children + pos,
              sizeof(btree_node*) * (parent->allocated - pos));

      parent->children[pos] = left;
      parent->children[pos + 1] = right;

      if (parent->parent == NULL) {
        tree->head = parent;
      }

      return;
    } else {
      node = parent;
      key = mkey;
      l = left;
      r = right;
    }
  }
}

int btree_node_get_pos(btree_node* node, void* key, int (*cmp)(void* a, void* b)) {
  int m, l = 0, r = node->allocated - 1;

  if (r < 0) {
    return 0;
  }

  for (;;) {
    m = (r - l) >> 1;
    if (cmp(key, (node->keys + node->key_size * r)) == 1) {
      return r + 1;
    } else if (cmp(key, (node->keys + node->key_size * l)) < 1){
      return l;
    } else if (cmp(key, (node->keys + node->key_size * r)) == 0 || m == 0) {
      return r;
    } else if (cmp(key, (node->keys + node->key_size * (l + m))) == 1) {
      l = l + m;
    } else {
      r = l + m;
    }
  }
}

int btree_node_insert(btree_node* node, void* key, int (*cmp)(void* a, void* b)) {
  int pos = btree_node_get_pos(node, key, cmp);
  if (pos < node->allocated) {
    memmove(node->keys + node->key_size * (pos + 1),
        node->keys + node->key_size * pos,
        node->key_size * (node->allocated - pos));
  }
  memcpy(node->keys + node->key_size * pos,
         key,
         node->key_size);

  node->allocated++;
  return pos;
}

/* for testing */
int cmp_int(void* a, void* b) {
  if (*(int *)a > *(int *)b) return 1;
  else if (*(int *)a == *(int *)b) return 0;
  else return -1;
}

char* array_dump(void* str, int len, btree_node** children) {
  int i, buffer = 255;
  char *result = malloc(buffer*sizeof(char)), *pos = result;

  *pos++ = '[';

  for (i = 0; i < len && pos < result + buffer - 1; i++) {
    pos += snprintf(pos, result - pos, "%d, ", *(int*)(str + sizeof(int) * i));
  }

  if (i > 0) {
    *(pos - 2) = ']';
    *(pos - 1) = '\0';
    pos--;
  } else {
    *pos++ = ']';
    *pos = '\0';
  }

  /**pos++ = ' ';*/
  /**pos++ = '(';*/
  /*for (i = 0; i < len + 1 && pos < result + buffer - 1; i++) {*/
    /*pos += snprintf(pos, result - pos, "%p, ", (void*)children[i]);*/
  /*}*/
  /**(pos - 2) = ')';*/
  /**(pos - 1) = '\0';*/

  return result;
}

char* tree_dump(btree_node* node, int depth) {
  btree_node* cur = NULL;

  if (node == NULL) return NULL;

  for (int i = 0; i < depth; i++) printf("  ");
  char* d = array_dump(node->keys, node->allocated, node->children);
  puts(d);
  free(d);

  for (int i = 0; i < node->allocated + 1; i++) {
    tree_dump(node->children[i], depth + 1);
  }
}

int main() {
  btree* tree = btree_create(20, sizeof(int));
  for(int i = 0; i < 1000; i += 1) {
    int r = rand() << 1 >> 18;
    btree_insert(tree, &r, &cmp_int);
  }
  tree_dump(tree->head, 0);
  btree_destroy(tree);
  return EXIT_SUCCESS;
}
