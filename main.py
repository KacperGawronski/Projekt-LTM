from Tokens import *

'''
Main function to process formule either in Polish notation,
reversed Polish notation or classic infix notation using LaTeX
is function Tokenize.
It parses string, creates token from it - either Variable, Predicate,
Connective or Quantifier. It recursively process string, and creates
tokens deeper and deeper, each of them is contained in parent -
Connective or Quantifier.
Negation is implemented as negation boolean value in Token.
Token created by Tokenize function have methods:

.copy(): returns copy of self

.change_negation(): set current negation to it's opposite. Returns self.

.process_negation(): if possible, removes negation from before
Connective or Quantifier. Returns processed result or self.copy()

.total_process_negation(): calls process_negation() in current object
and recursively in all contained objects. Stops at Variable or
Predicate. Returns result of such process.

.remove_negation_from_before_quantifiers(): process negations
recursively only if there is quantifier in children. Returns result or
self.copy()

.neg(deepness=0): returns negated variable (deepness allow to process
and negate object, it's children, children's children and so). 
Returns copy of Token with negated value.

.eliminate_ie(): alters Implications and Equivalences to equivalent 
formules using Conjugations and Alternatives.

.set_target_order(variant): allows to switch between
'in'-,'pre'-,'post'- -fix notations

.set_notation(variant): allows to switch between 'Polish' and 'classic'
notations.

.get_variables():returns set of Variables or Predicates located in
formule

.get_tree(): returns tree as list of lists showing placement of
Variables or Predicates in formule.

.describe(): returns string describing each Token in formule

.set_values(values_pairs): allow to set values of Variables and
Predicates from name:value pairs. In case of Predicates name is full
string describing predicate, for example: P(x)

.find_valuation(): returns list of valuations with resulting boolean
value of formule when values are applied

.print_ascii_valuation_table(): print possible valuations for given
formule

.cnf(): returns string of equivalent formule to Token in 
conjunctive normal form

.dnf(): returns string of equivalent formule to Token in
dysjunctive normal form (Polish APN)
'''
#token=Tokenize('\\neg (p \\leftrightarrow \\exists_{x}(q<129389))','in')	
#token=Tokenize('(p \\lor q)\\leftrightarrow\\neg(p\\rightarrowq)')
#token.set_notation('Polish')
#token.set_target_order('pre')
#print(token)
#print(token.neg(10))
#token=Tokenize('\\neg(\\forall_{x\in Y}((y<x<z) \\lor P(x))\\leftrightarrow (x<z))','in')
#token=Tokenize('\\neg\\forall_{x}(p\\land q)','in')
#print(token)
#print(token.neg(1))
#print(token.neg(2))
#print(token.eliminate_ie())
#print(token)
#token.set_notation('Polish')
#token.set_target_order('pre')
#print(token)
#token=Tokenize('\\neg (((\\exists_{x}P(x) \\land q) \\lor \\forall_{y}(P(y) \\land s)) \\leftrightarrow ((p \\leftrightarrow s) \\rightarrow (q \\leftrightarrow r)))')
#token=Tokenize('\\neg(p \\leftrightarrow q)')
#token=Tokenize('\\neg(\\exists_{x}(P(x)) \\land \\forall_{y}(R(y)))')
#token=Tokenize('NKKArsEpqECrsAKqrArp')
#token.set_notation('classic')
#token.set_target_order('in')
#print(token)
#token=token.remove_negation_from_before_quantifiers()
#print('___________')
#print(token.get_variables())
#print(token.get_tree())
#print(token.total_process_negation())
#token.prompt_values()
#token=Tokenize('\\exists_{x}((P(x))\\lor(\\neg(P(x))))')
token=Tokenize('NKNApqAKqrKNqNr')
print(token)
token.print_ascii_evaluation_table()
token.set_target_order('pre')
