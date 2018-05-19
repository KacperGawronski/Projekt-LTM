import string
from Token import *
from Quantifiers import *
from Connectives import *
from Values import *
import classic_notation
import polish_notation
import string
import re
keywords={
	'\\exists':Exists,
	'\\forall':Forall,
	'\\land':And,
	'\\lor':Or,
	'\\rightarrow':Implication,
	'\\leftrightarrow':Equivalence
	}

def find_lower(formule):
	i=0
	l=len(formule)
	stack=[]
	while i<l:
		if formule[i]=='{':
			stack.append('{')
		if formule[i]=='}':
			stack.pop()
			if len(stack)==0:
				return i+1
		i+=1
	return 0
def skip_digits(formule):
	i=0
	l=len(formule)
	while i<l and formule[i] in string.digits:
		i+=1
	return i

def find_notation(formule):
	if any([len(re.findall(r'\\exists',formule))>0, 
		len(re.findall(r'\\forall',formule))>0,
		len(re.findall(r'\\land',formule))>0,
		len(re.findall(r'\\lor',formule))>0,
		len(re.findall(r'\\rightarrow',formule))>0,
		len(re.findall(r'\\leftrightarrow',formule))>0]) or '(' in formule:
		return 'classic'
	else:
		return 'Polish'
def Tokenize(formule,notation='check',target_order='check',order='check'):
	formule=formule.replace(' ','').replace('\t','').replace('\n','')
	if notation=='check':
		notation=find_notation(formule)
	if notation=='classic':	
		if order=='check':
			order= classic_notation.check_order(formule)
		if target_order=='check':
			target_order=order
		l=len(formule)
		tokens=[]
		if len(formule)==1:
			return Variable(formule[0],target_order)
		if order=='in':
			i=0
			while i<l:
				if formule[i] in classic_notation.left_brackets:
					jump=classic_notation.find_closing_bracket(formule[i:])
					tokens.append(Tokenize(formule[i+1:i+jump],notation='classic',target_order=order,order=order))
					i+=jump
					continue
				if formule[i:i+7] in ('\\exists','\\forall'):
					j=i+7
					lower_jump=find_lower(formule[j:])
					lower=formule[j:j+lower_jump]
					print('#',lower,'#')
					jump=classic_notation.find_end_of_token(formule[j+lower_jump:])
					tokens.append(keywords[formule[i:j]](Tokenize(formule[j+lower_jump:j+lower_jump+jump],notation='classic',target_order=target_order,order='in'),lower=lower,negation=False,target_order=target_order))
					i+=7+jump+lower_jump
					continue
				if formule[i] in string.ascii_lowercase or formule[i] in string.digits or classic_notation.check_relational_symbols(formule[i:]):
					#<TODO> ROZSZERZYĆ O INNE SYMBOLE RELACYJNE
					start=i
					if l>1:
						while (i<l-1 and formule[i+1] in string.digits) or (i<l and formule[i] in string.digits):
							i+=1
						while i<l and (formule[i] in string.digits or classic_notation.check_relational_symbols(formule[i:])):
							i+=skip_digits(formule[i:])
							i+=1
					if start!=i:
						tokens.append(Predicate('',formule[start:i+1],target_order))
					else:
						tokens.append(Variable(formule[i],target_order))
					i+=1
					continue
				if formule[i] in string.ascii_uppercase:
					jump=classic_notation.find_closing_bracket(formule[i+1:])
					tokens.append(Predicate(formule[i],formule[i+2:i+jump],negation=False,notation=notation,target_order=target_order))
					i+=1+jump
					continue
				if formule[i:i+4]=='\\neg':
					jump=classic_notation.find_end_of_token(formule[i+4:])
					if(formule[i+4] in classic_notation.left_brackets):
						tokens.append(Tokenize(formule[i+5:i+4+jump],notation,order=order))
					else:
						tokens.append(Tokenize(formule[i+4:i+4+jump],notation,order=order))
					print(formule[i:i+4+jump])
					i+=4+jump
					tokens[-1].change_negation()
					continue
				if formule[i:i+5]=='\\land':
					return And(tokens[0],Tokenize(formule[i+5:i+5+classic_notation.find_end_of_token(formule[i+5:])],notation=notation,target_order=target_order,order=order),target_order=target_order,negation=False)
				if formule[i:i+4]=='\\lor':
					return Or(tokens[0],Tokenize(formule[i+4:i+4+classic_notation.find_end_of_token(formule[i+4:])],notation,order=order),target_order=target_order,negation=False)
				if formule[i:i+11]=='\\rightarrow':
					return Implication(tokens[0],Tokenize(formule[i+11:i+11+classic_notation.find_end_of_token(formule[i+11:])],notation,order=order),target_order=target_order,negation=False)
				if formule[i:i+15]=='\\leftrightarrow':
					return Equivalence(tokens[0],Tokenize(formule[i+15:i+15+classic_notation.find_end_of_token(formule[i+15:])],notation,order=order),target_order=target_order,negation=False)

				i+=1
			if len(tokens)>1:
				print('Tokens converted to predicate: ',tokens)
				return Predicate(''.join(list(map(str,tokens))))
			return tokens[0]
	if notation=='Polish':
		if order=='check':
			order=polish_notation.find_order(formule)
		if target_order=='check':
			target_order=order
		stack=[]
		i=0
		l=len(formule)
		if l==1:
			return Variable(formule[i])
		if order=='pre':
			while i<l:
				if formule[i] in 'ACKE':
					jump=polish_notation.find_half_of_token(formule)
					return polish_notation.keywords[formule[i]](Tokenize(formule[i+1:i+jump],notation='Polish',order='pre'),Tokenize(formule[i+jump:],notation='Polish',order='pre'),notation='Polish',target_order=target_order)
				if formule[i] == 'N':
					return Tokenize(formule[i+1:],notation='Polish',order='pre').change_negation()
				if formule[i] in string.ascii_lowercase:
					return Variable(formule[i])
				i+=1
		if order=='post':
			return Tokenize(formule[::-1],notation='Polish',order='pre')
	print('Error: not implemented yet or wrong formule')
