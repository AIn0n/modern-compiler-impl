%{
#include <string.h>
#include "util.h"
#include "tokens.h"
#include "errormsg.h"

int charPos=1;
int comment_nesting = 0;

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

%x COMMENT

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
for  {adjust(); return FOR;}
array {adjust(); return ARRAY;}
if    {adjust(); return IF;}
then  {adjust(); return THEN;}
else  {adjust(); return ELSE;}
while {adjust(); return WHILE;}
to    {adjust(); return TO;}
do    {adjust(); return DO;}
let   {adjust(); return LET;}
in    {adjust(); return IN;}
end   {adjust(); return END;}
of    {adjust(); return OF;}
break {adjust(); return BREAK;}
nil   {adjust(); return NIL;}
function {adjust(); return FUNCTION;}
var   {adjust(); return VAR;}
type  {adjust(); return TYPE;}
[a-zA-Z][a-zA-Z0-9_]* {adjust(); yylval.sval=String(yytext); return ID;}
[0-9]+	 {adjust(); yylval.ival=atoi(yytext); return INT;}
.	 {adjust(); EM_error(EM_tokPos,"illegal token");}
"/*" {adjust(); comment_nesting++; BEGIN(COMMENT);}
"*/" {EM_error(EM_tokPos, "Unclosed comment");}


<COMMENT>{

    "/*" { adjust(); comment_nesting++; continue;}
    "*/" {
            adjust(); 
            comment_nesting--;
            if (!comment_nesting) {
                BEGIN(INITIAL);
            }
        }
    <<EOF>> { EM_error(EM_tokPos, "EOF during comment");}
    . {adjust(); continue;}
}