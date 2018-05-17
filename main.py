from Tokens import *


#token=Tokenize('\\neg (p \\leftrightarrow \\exists_{x}(q<129389))','in')	
token=Tokenize('(p \\lor q)\\leftrightarrow\\neg(p\\rightarrowq)')
token.set_notation('Polish')
token.set_target_order('pre')
print(token)
print(token.neg(10))
token=Tokenize('\\neg(\\forall_{x\in Y}((y<x<z) \\lor P(x))\\leftrightarrow (x<z))','in')
#token=Tokenize('\\neg\\forall_{x}(p\\land q)','in')
print(token)
print(token.neg(1))
print(token.neg(2))
print(token.neg_total())
