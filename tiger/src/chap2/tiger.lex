%{
#include <string.h>
#include "util.h"
#include "tokens.h"
#include "errormsg.h"

int charPos=1;

int yywrap(void)
{
 charPos=1;
 return 1;
}


void adjust(void)
{
 EM_tokPos=charPos;
 charPos+=yyleng;
}

%}

%%
" "	 {adjust(); continue;}
\n	 {adjust(); EM_newline(); continue;}
","	 {adjust(); return COMMA;}
;   {adjust(); return SEMICOLON;}
:=  {adjust(); return ASSIGN;}
:   {adjust(); return COLON;}
"("  {adjust(); return LPAREN;}
")"  {adjust(); return RPAREN;}
"{"  {adjust(); return LBRACK;}
"}"  {adjust(); return RBRACK;}
"["  {adjust(); return LBRACE;}
"]"  {adjust(); return RBRACE;}
"."  {adjust(); return DOT;}
"+"  {adjust(); return PLUS;}
-    {adjust(); return MINUS;}
"*"  {adjust(); return TIMES;}
"/"  {adjust(); return DIVIDE;}
"="  {adjust(); return EQ;}
"<>" {adjust(); return NEQ;}
"<=" {adjust(); return LE;}
"<"  {adjust(); return LT;}
">=" {adjust(); return GE;}
">"  {adjust(); return GT;}
&    {adjust(); return AND;}
"|"  {adjust(); return OR;}
for  	 {adjust(); return FOR;}
[0-9]+	 {adjust(); yylval.ival=atoi(yytext); return INT;}
[a-zA-Z][a-zA-Z0-9_]* {adjust(); yylval.sval=String(yytext); return ID;}
.	 {adjust(); EM_error(EM_tokPos,"illegal token");}

