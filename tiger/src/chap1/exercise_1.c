#include "exercise_1.h"
#include "tokens.h"

#include <stdio.h>

int
max(const int a, const int b)
{
	return (a > b) ? a : b;
}

int
max3(const int a, const int b, const int c)
{
	if (a > b || c > b) {
		return (a > c) ? a : c;
	}
	return b;
}

int
_maxargs_exp(A_exp exp)
{
	puts("parsing expression");
	switch(exp->kind) {
	case A_idExp:
		puts("--A_idExp");
	case A_numExp:
		puts("--A_numExp");
		return 0;
	case A_opExp:
		puts("--A_opExp");
		return 	_maxargs_exp(exp->u.op.left) +
			_maxargs_exp(exp->u.op.right);
	case A_eseqExp:
		puts("--A_eseqExp");
		return maxargs(exp->u.eseq.stm);
	}
	return 0;
}

int
_len_expl(const A_expList expl)
{
	if (expl->kind == A_pairExpList)
		return 1 + _len_expl(expl->u.pair.tail);
	return 1;
}

int
_maxargs_expl(A_expList expl)
{
	puts("parsing expression list");
	int args = _len_expl(expl);
	switch(expl->kind) {
	case A_pairExpList:
		return max3(
			args,
			_maxargs_expl(expl->u.pair.tail),
			_maxargs_exp(expl->u.pair.head)
		);
	case A_lastExpList:
		return max(
			args,
			_maxargs_exp(expl->u.last)
		); 
	}
	return 0;
}

int 
maxargs(A_stm stm)
{
	puts("parsing stm");
	switch(stm->kind) {
	case A_compoundStm:
		return max(
			maxargs(stm->u.compound.stm1), 
			maxargs(stm->u.compound.stm2)
		);
	case A_assignStm:
		return _maxargs_exp(stm->u.assign.exp);
	case A_printStm:
		return _maxargs_expl(stm->u.print.exps);
	}
	return 0;
}
