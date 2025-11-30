#include "exercise_1_1.h"

T_tree Tree(T_tree l, string k, T_tree r) {
	T_tree t = (T_tree) checked_malloc(sizeof(*t));
	t->left=l;
	t->key=k;
	t->right=r;
	return t;
}

T_tree insert(string key, T_tree t) {
	if (t==NULL) 
		return Tree(NULL, key, NULL);

	const int cmp_res = strcmp(key,t->key);
	if (cmp_res < 0)
		return Tree(insert(key,t->left),t->key,t->right);
	else if (cmp_res > 0)
		return Tree(t->left,t->key,insert(key,t->right));
	else 
		return Tree(t->left,key,t->right);
}