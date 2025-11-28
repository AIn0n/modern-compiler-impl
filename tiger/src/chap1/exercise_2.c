#include <stdio.h>

#include "linked_list.h"
#include "tokens.h"
#include "table_wrappers.h"


// moved the logic into new function to make it more readable
// but there is no any special need to extract it.
int
exec_operator(const int l, const int r, const A_binop op)
{
	switch (op) {
	case A_plus:
		return l + r;
	case A_minus:
		return l - r;
	case A_div:
		return l / r;
	case A_times:
		return l * r;
	}
}

struct IntAndTable
interpExp(A_exp e, Table_ t)
{
	switch(e->kind) {
	case A_idExp:
		return (struct IntAndTable) {
			.i = lookup(t, e->u.id),
			.t = t
		};
	case A_numExp:
		return (struct IntAndTable) {
			.i = e->u.num,
			.t = t
		};
	case A_opExp:
		struct IntAndTable l_res = interpExp(e->u.op.left, t);
		struct IntAndTable r_res = interpExp(e->u.op.right, l_res.t);
		return (struct IntAndTable) {
			.i = exec_operator(l_res.i, r_res.i, e->u.op.oper),
			.t = r_res.t
		};
	case A_eseqExp:
		Table_ stm_res = interpStm(e->u.eseq.stm, t);
		return interpExp(e->u.eseq.exp, stm_res);
	}
}

Table_
interpExpListPrint(A_expList expl, Table_ t)
{
	if (expl->kind == A_lastExpList) {
		struct IntAndTable exp_res = interpExp(expl->u.last, t);
		printf("%i\n", exp_res.i);
		return exp_res.t;
	}
	struct IntAndTable exp_res = interpExp(expl->u.pair.head, t);
	printf("%i ", exp_res.i);
	return interpExpListPrint(expl->u.pair.tail, exp_res.t);
}

Table_
interpStm(A_stm s, Table_ t)
{
	switch (s->kind) {
	case A_compoundStm:
		Table_ first_stm_t = interpStm(s->u.compound.stm1, t);
		return interpStm(s->u.compound.stm2, first_stm_t);
	case A_assignStm:
		struct IntAndTable assign_res = interpExp(s->u.assign.exp, t);
		return update(assign_res.t, s->u.assign.id, assign_res.i);
	case A_printStm:
		return interpExpListPrint(s->u.print.exps, t);
	}
}


void
interpret(A_stm stmt)
{

}