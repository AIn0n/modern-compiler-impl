#include <stdio.h>
#include "chap1/tokens.h"
#include "chap1/exercise_1.h"
#include "chap1/exercise_2.h"

int
main(void)
{
// test maxargs
	A_stm prog = A_CompoundStm(
		A_AssignStm(
			"a", 
			A_OpExp(A_NumExp(5), A_plus, A_NumExp(3))
		),
		A_CompoundStm(
			A_AssignStm(
				"b", 
				A_EseqExp(
					A_PrintStm(
						A_PairExpList(
							A_IdExp("a"),
							A_LastExpList(
								A_OpExp(
									A_IdExp("a"),
									A_minus,
									A_NumExp(1)
								)
							)
						)
					),
					A_OpExp(A_NumExp(10), A_times, A_IdExp("a"))
				)
			),
		A_PrintStm(A_LastExpList(A_IdExp("b")))
		)
	);
	printf("%i\n", maxargs(prog));
	A_stm prog1 = A_PrintStm(
		A_PairExpList(
			A_EseqExp(
				A_PrintStm(
					A_PairExpList(
						A_NumExp(1),
						A_PairExpList(
							A_NumExp(2),
							A_LastExpList(
								A_NumExp(3)
							)
						)
					)
				),
				A_NumExp(2137)
			),
			A_LastExpList(A_NumExp(69))
		)
	);
	printf("%i\n", maxargs(prog1));

puts("====================");
puts("= TEST INTERPRETER =");
puts("====================");
// test interpret
	interpret(prog);
}
