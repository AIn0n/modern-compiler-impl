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
# define COLON 261	//done
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
# define ARRAY 283	//done
# define IF 284		//done
# define THEN 285	//done
# define ELSE 286	//done
# define WHILE 287	//done
# define FOR 288	//done
# define TO 289		//done
# define DO 290		//done
# define LET 291	//done
# define IN 292		//done
# define END 293	//done
# define OF 294		//done
# define BREAK 295	//done
# define NIL 296	//done
# define FUNCTION 297	//done
# define VAR 298	//done
# define TYPE 299	//done
