#include "util.h"

typedef union  {
	int pos;
	int ival;
	string sval;
} YYSTYPE;

extern YYSTYPE yylval;

# define ID 257		//done
# define STRING 258
# define INT 259	//done
# define COMMA 260	//done
# define COLON 261
# define SEMICOLON 262	//done
# define LPAREN 263	//done
# define RPAREN 264	//done
# define LBRACK 265	//done
# define RBRACK 266	//done
# define LBRACE 267	//done
# define RBRACE 268	//done
# define DOT 269	//done
# define PLUS 270	//done
# define MINUS 271	//done
# define TIMES 272	//done
# define DIVIDE 273	//done
# define EQ 274		//done
# define NEQ 275	//done
# define LT 276		//done
# define LE 277		//done
# define GT 278		//done
# define GE 279		//done
# define AND 280	//done
# define OR 281		//done
# define ASSIGN 282	//done
# define ARRAY 283
# define IF 284
# define THEN 285
# define ELSE 286
# define WHILE 287
# define FOR 288
# define TO 289
# define DO 290
# define LET 291
# define IN 292
# define END 293
# define OF 294
# define BREAK 295
# define NIL 296
# define FUNCTION 297
# define VAR 298
# define TYPE 299
