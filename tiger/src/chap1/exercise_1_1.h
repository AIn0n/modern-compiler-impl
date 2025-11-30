#include <string.h>

#include "utils.h"

typedef struct tree *T_tree;

struct tree {
    T_tree left;
    string key;
    T_tree right;
};

T_tree Tree(T_tree l, string k, T_tree r);
T_tree insert(string key, T_tree t);