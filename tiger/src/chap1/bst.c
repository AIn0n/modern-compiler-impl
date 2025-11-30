#include <stdlib.h>
#include <string.h>

#include <stdio.h>

#include "bst.h"

T_tree Tree(T_tree l, string k, T_tree r) {
	T_tree t = (T_tree) checked_malloc(sizeof(*t));
	t->left=l;
	t->key=k;
	t->right=r;
	return t;
}

T_tree insert(string key, T_tree t) {
	if (t==nullptr) 
		return Tree(nullptr, key, nullptr);

	const int cmp_res = strcmp(key,t->key);
	if (cmp_res < 0)
		return Tree(insert(key,t->left),t->key,t->right);
	else if (cmp_res > 0)
		return Tree(t->left,t->key,insert(key,t->right));
	else 
		return Tree(t->left,key,t->right);
}

// function to make leaf - just a little bit less mess during tree initalization
T_tree
Leaf(string k)
{
	return Tree(nullptr, k, nullptr);
}


// exercise 1.1.a
bool
member(string key, T_tree t)
{
	if (t == nullptr)
		return false;
	
	const int cmp_res = strcmp(key, t->key);
	if (cmp_res == 0) {
		return true;
	} else if (cmp_res < 0) {
		return member(key, t->left);
	} else if (cmp_res > 0) {
		return member(key, t->right);
	}
	exit(1);
}

void
print_offset(const int offset)
{
	for (int i = 0; i < offset; ++i) {
		printf("\t");
	}
}

void
print_tree_rec(T_tree t, int depth)
{
	print_offset(depth);
	puts(t->key);
	if (t->left != nullptr) {
		print_offset(depth);
		puts("LEFT:");
		print_tree_rec(t->left, depth + 1);
	}
	if (t->right != nullptr) {
	print_offset(depth);
	puts("RIGHT:");
	print_tree_rec(t->right, depth + 1);
	}
}

void 
print_tree(T_tree t)
{
	print_tree_rec(t, 0);
}
