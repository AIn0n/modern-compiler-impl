#ifndef _LINKED_LIST_H_
#define _LINKED_LIST_H_

#include "utils.h"

typedef struct table *Table_;

struct table {
    string id;
    int value;
    Table_ tail;
};

Table_ Table(string, int, struct table *);

#endif
