#ifndef _BST_H_
#define _BST_H_

#include "utils.h"

typedef struct tree *T_tree;

struct tree {
    T_tree left;
    string key;
    T_tree right;
};

T_tree Tree(T_tree l, string k, T_tree r);
T_tree insert(string key, T_tree t);
bool member(string key, T_tree t);

// my functions

T_tree Leaf(string k);
void print_tree(T_tree t);

#endif
