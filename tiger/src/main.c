#include <stdio.h>
#include <assert.h>
#include "chap1/tokens.h"
#include "chap1/exercise_1.h"
#include "chap1/exercise_2.h"
#include "chap1/bst.h"

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

puts("==================");
puts("= EXERCISE 1.1.a =");
puts("==================");

	T_tree t = Tree(
		Tree(
			Leaf("Alan"),
			"Bob",
			Leaf("Ellen")
		),
		"John",
		Tree(
			Leaf("Karen"),
			"Tom",
			Leaf("Wendy")
		)
	);

	assert(member("Karen", t));
	assert(member("Przemek", t) == 0);


puts("==================");
puts("= EXERCISE 1.1.c =");
puts("==================");

	string seq1[9] = {
		"t", 
		"s", 
		"p", 
		"i", 
		"p", 
		"f", 
		"b", 
		"s", 
		"t",
	};
	T_tree t1 = nullptr;

	for (int i = 0; i < 9; ++i) {
		t1 = insert(seq1[i], t1);
	}

	print_tree(t1);

	string seq2[9] = {
		"a", 
		"b", 
		"c", 
		"d", 
		"e", 
		"f", 
		"g", 
		"h", 
		"i",
	};

	T_tree t2 = nullptr;
	for (int i = 0; i < 9; ++i) {
		t2 = insert(seq2[i], t2);
	}

	print_tree(t2);
}
