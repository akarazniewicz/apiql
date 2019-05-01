grammar ApiQL;


criteria
  : criterion (';' criterion)*
  ;

criterion
  : conjunction
  | disjunction
  | predicate
  ;


conjunction: 'and' '(' criteria ')';


disjunction: 'or' '(' criteria ')';


predicate: basic_predicate | compound_predicate;


basic_predicate: keyword basic_operator value;


compound_predicate: keyword compound_operator values;

keyword: KEYWORD;


basic_operator
  : '=='
  | '!='
  | '>'
  | '>='
  | '<'
  | '<='
  | 'like'
  | 'ilike'
  | 'notlike'
  | 'notilike'
  | 'startswith'
  | 'istartswith'
  | 'endswith'
  | 'iendswith'
  | 'contains'
  | 'notcontains'
  | 'icontains'
  | 'inotcontains'
  | 'match'
  ;


compound_operator
  : 'in'
  | 'notin'
  ;


values: '(' value (',' value)* ')';

value
   : number
   | boolean
   | nil
   | datetime
   | string;


boolean: 'true' | 'false';

nil: 'null';

number: NUMBER;

datetime: 'datetime' '(' STRING ')';

string: STRING;


// -*- Lexemes -*-


// We cannot directly use lexeme using 'fragment' in parser; still need to capture type of literal. This STRING
// redefinition is just to make parser happy.
STRING
   : ESCAPED_STRING
   ;

NUMBER
   : FLOAT
   | INT
   ;


KEYWORD
   : [a-zA-Z_]([a-zA-Z0-9_.]*)
   ;


ESCAPED_STRING
   : '"' (ESC | SAFECODEPOINT)* '"'
   ;



fragment ESC
   : '\\' (["\\/bfnrt] | UNICODE)
   ;


fragment UNICODE
   : 'u' HEX HEX HEX HEX
   ;


fragment HEX
   : [0-9a-fA-F]
   ;


fragment SAFECODEPOINT
   : ~ ["\\\u0000-\u001F]
   ;


FLOAT
   : '-'? INT ('.' [0-9] +)? ([Ee] [+\-]? INT)?
   ;


INT
   : '0' | [1-9] [0-9]*
   ;


// \- since - means "range" inside [...]

WS
   : [ \t\n\r] + -> skip
   ;