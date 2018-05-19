from Token import *
from Quantifiers import *
from Connectives import *
from Values import *
import string
keywords={
	'K':And,
	'A':Or,
	'C':Implication,
	'E':Equivalence
}
def find_order(formule):
	if formule[0] in 'NKACE':
		return 'pre'
	if formule[-1] in 'NKACE':
		return 'post'
	return 'in'

def find_half_of_token(formule):
	l=len(formule)
	count=0
	i=0
	stack=[]
	while i<l:
		if formule[i] in 'AKCEN':
			stack.append([formule[i],0])
		else:
			if stack[-1][0]=='N':
				stack.pop()
				stack[-1][1]+=1
			else:
				stack[-1][1]+=1
				while (stack[-1][0] in 'AKCE' and stack[-1][1]==2) or (stack[-1][0]=='N' and stack[-1][1]==1):
					stack.pop()
					stack[-1][1]+=1
		i+=1
		if len(stack)==0:
			print('ERROR',formule)
		if stack[0][1]==1:
			return i
	return i
def find_end_of_token(formule):
	l=len(formule)
	count=0
	i=0
	stack=[]
	while i<l:
		if formule[i] in 'AKCEN':
			stack.append((formule[i],count))
			count=0
			i+=1
			continue
		else:
			if stack[-1]=='N':
				count=stack.pop()[1]+1
			else:
				count+=1
				if count%2==0:
					count=stack.pop()[1]+1
		i+=1
		if len(stack)==0:
			return i
	return i-1
