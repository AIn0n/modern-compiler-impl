#pragma once

#include <assert.h>
#include <stdbool.h>

typedef char *string;

typedef struct {
	char *str;
	int size;
	int cap;
} ST;

void *checked_malloc(int);
string String(char *);

typedef struct U_boolList_ *U_boolList;
struct U_boolList_ {bool head; U_boolList tail;};
U_boolList U_BoolList(bool head, U_boolList tail);


// My own functions 

ST ST_append(ST s, char c);

ST ST_init(void);