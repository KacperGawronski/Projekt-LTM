import string
from Token import *
from Quantifiers import *
from Connectives import *
from Values import *
import string
keywords={
	'\\exists':Exists,
	'\\forall':Forall,
	'\\land':And,
	'\\lor':Or,
	'\\rightarrow':Implication,
	'\\leftrightarrow':Equivalence
	}


def check_order(formule):
	order='check'
	i=0;
	l=len(formule)
	while i<l:
		if formule[i] in string.ascii_letters:
			break	
		if formule[i]=='\\':
			if formule[i:i+7]=='\\exists' or formule[i:i+7]=='\\forall':
				i+=7
				if formule[i]=='{':
					while formule[i]!='}':
						i+=1
				i+=1
				if formule[i]=='^' and formule[i+1]=='{':
					while formule[i]!='}' and i<l :
						i+=1
					i+=1
				continue
			if formule[i:i+4]=='\\neg':
				i+=4
				continue
			if formule[i:i+4]=='\\lor' or formule[i:i+5]=='\\land' or formule[i:i+11]=='\\rightarrow' or formule[i:i+15]=='\\leftrightarrow':
				order='pre'
				break
		i+=1
	if order=='check':
		i=l-1
		while i>=0:
			if formule[i] =='_':
				i-=1
				continue
			if formule[i]=='}':
				while i>=0 and formule[i]!='{':
					i-=1
				i-=2
				continue
			if formule[i-6]=='\\' and formule[i-6:i+1]=='\\exists' or formule[i-6:i+1]=='\\forall':
				i-=7
				continue
			if formule[i-3]=='\\' and formule[i-3:i+1]=='\\lor' :
				order='post'
				break
			if formule[i-4]=='\\' and formule[i-4:i+1]=='\\land':
				order='post'
				break
			if formule[i-10]=='\\' and formule[i-10:i+1]=='\\rightarrow':
				order='post'
				break
			if formule[i-14]=='\\' and formule[i-14:i+1]=='\\leftrightarrow':
				order='post'
				break
			if formule[i-3]=='\\' and formule[i-3:i+1]=='\\neg':
				order='post'
				break
			if formule[i] in string.ascii_letters:
				break
			i-=1
		if order=='check':
			order='in'
			
	print(order)
	return order


def check_relational_symbols(formule):
	symbols=('<','>','|','=','+','-','*','/')
	i=1
	l=len(formule)
	if l>1:
		return formule[0] in symbols or formule[1] in symbols
	if l==1:
		return formule[0] in symbols


left_brackets=('(','[')
right_brackets=(')',']')


def find_closing_bracket(text):
	i=1
	start=1
	l=len(text)
	stack=[text[0]]
	while(i<l):
		if text[i]=='(' or text[i]=='[':
			stack.append(text[i])
		
		else:	
			if text[i]==')' and stack[-1]=='(':
				stack.pop()
				if len(stack)==0:
					return i+1
			if text[i]==']' and stack[-1]=='[':
				stack.pop()	
				if len(stack)==0:
					return i+1
		i+=1
	return i
def find_end_of_token(formule):
	i=0
	l=len(formule)
	while i<l:
		if formule[i]=='_':
			i+=1
			if formule[i]=='{':
				while formule[i]!='}':
					i+=1
			i+=1
			continue
		if formule[i:i+7] in ('\\exists','\\forall'):
			i+=7
			continue
		if formule[i:i+4]=='\\neg':
			i+=4
			continue
		if formule[i] in left_brackets:
			i+=find_closing_bracket(formule[i:])
			return i
		if formule[i] in string.ascii_lowercase:
			i+=1
			break
		if formule[i] in string.ascii_uppercase:
			i+=find_closing_bracket(formule[i:])
			return i
		i+=1
	return i
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
	
	
def Tokenize(formule,target_order='in',order='check'):
	formule=formule.replace(' ','').replace('\t','').replace('\n','')

	if order=='check':
		order= check_order(formule)
	l=len(formule)
	tokens=[]
	in_quantifier=False
	in_neg=False
	if len(formule)==1:
		return Variable(formule[0],target_order)
	if order=='in':
		i=0
		while i<l:
			if formule[i] in left_brackets:
				jump=find_closing_bracket(formule[i:])
				tokens.append(Tokenize(formule[i+1:i+jump],target_order,'in'))
				i+=jump
				continue
			if formule[i:i+7] in ('\\exists','\\forall'):
				j=i+7
				lower_jump=find_lower(formule[j:])
				lower=formule[j:j+lower_jump]
				jump=find_end_of_token(formule[j+lower_jump:])
				tokens.append(keywords[formule[i:j]](Tokenize(formule[j+lower_jump:j+lower_jump+jump],target_order,'in'),lower,'in',target_order))
				i+=7+jump+lower_jump
				continue
			if formule[i] in string.ascii_lowercase or formule[i] in string.digits or check_relational_symbols(formule[i:]):
				#<TODO> ROZSZERZYĆ O INNE SYMBOLE RELACYJNE
				start=i
				if l>1:
					while (i<l-1 and formule[i+1] in string.digits) or (i<l and formule[i] in string.digits):
						i+=1
					while i<l and (formule[i] in string.digits or check_relational_symbols(formule[i:])):
						i+=skip_digits(formule[i:])
						i+=1
				if start!=i:
					tokens.append(Predicate('',formule[start:i+1],target_order))
				else:
					tokens.append(Variable(formule[i],target_order))
				i+=1
				continue
			if formule[i] in string.ascii_uppercase:
				jump=find_closing_bracket(formule[i+1:])
				tokens.append(Predicate(formule[i],formule[i+2:i+jump],target_order))
				i+=1+jump
				continue
			if formule[i:i+4]=='\\neg':
				jump=find_end_of_token(formule[i+4:])
				if(formule[i+4] in left_brackets):
					tokens.append(Tokenize(formule[i+5:i+4+jump],target_order,'in'))
				else:
					tokens.append(Tokenize(formule[i+4:i+4+jump],target_order,'in'))
				i+=4+jump
				tokens[-1].change_negation()
				continue
			if formule[i:i+5]=='\\land':
				return And(tokens[0],Tokenize(formule[i+5:i+5+find_end_of_token(formule[i+5:])],target_order,'in'),'in',target_order)
			if formule[i:i+4]=='\\lor':
				return Or(tokens[0],Tokenize(formule[i+4:i+4+find_end_of_token(formule[i+4:])],target_order,'in'),'in',target_order)
			if formule[i:i+11]=='\\rightarrow':
				return Implication(tokens[0],Tokenize(formule[i+11:i+11+find_end_of_token(formule[i+11:])],target_order,'in'),'in',target_order)
			if formule[i:i+15]=='\\leftrightarrow':
				return Equivalence(tokens[0],Tokenize(formule[i+15:i+15+find_end_of_token(formule[i+15:])],target_order,'in'),'in',target_order)

			i+=1
		if len(tokens)>1:
			return Predicate(''.join(list(map(str,tokens))))
		return tokens[0]
