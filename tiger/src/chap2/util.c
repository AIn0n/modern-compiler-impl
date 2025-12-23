/*
 * util.c - commonly used utility functions.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "util.h"

void 
*checked_malloc(int len)
{
  void *p = malloc(len);
  if (!p) {
    fprintf(stderr,"\nRan out of memory!\n");
    exit(1);
  }
  return p;
}

string
String(char *s)
{
  string p = checked_malloc(strlen(s)+1);
  strcpy(p,s);
  return p;
}

U_boolList
U_BoolList(bool head, U_boolList tail)
{ 
  U_boolList list = checked_malloc(sizeof(*list));
  list->head = head;
  list->tail = tail;
  return list;
}

ST
ST_append(ST s, char c)
{
  if (s.size + 1 >= s.cap) {
    s.cap *= 2;
    string tmp = realloc(s.str, sizeof(s.cap));
    if (tmp == NULL) {
      exit(1);
    }
  }
  s.str[s.size++] = c;
  s.str[s.size] = '\0';
  return s;
}

ST
ST_init(void)
{
  return (ST) {
    .cap = 0,
    .size = 0,
    .str = NULL
  };
}