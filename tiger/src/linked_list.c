#include <stdlib.h>

#include "linked_list.h"

Table_
Table(string id, int val, struct table *tail)
{
	Table_ t = checked_malloc(sizeof(*t));
	t->id = id;
	t->value = val;
	t->tail = tail;
	return t;
}

Table_
update(Table_ src, string id, int val)
{
	return Table(id, val, src);
}

int
lookup(Table_ t, string key)
{
	if (t == nullptr) {
		exit(1);
	}

	for (Table_ tmp = t; tmp != nullptr; tmp = tmp->tail) {
		if (tmp->id == key) {
			return tmp->value;
		}
	}
	exit(1);
}
