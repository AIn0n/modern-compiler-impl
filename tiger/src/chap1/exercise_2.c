
#include "linked_list.h"
#include "tokens.h"

Table_
interpStm(A_stm s, Table_ t)
{
	switch (s->kind) {
	case A_compoundStm:
		Table_ first_stm_t = interpStm(s->u.compound.stm1, t);
		return interpStm(s->u.compound.stm2, first_stm_t);
	case A_assignStm:
		
	case A_printStm:
		break;
	}
}


void
interpret(A_stm stmt)
{

}