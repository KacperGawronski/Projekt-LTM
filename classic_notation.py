
import string
def check_order(formule):
	order='check'
	i=0;
	l=len(formule)
	while i<l:
		if formule[i] in string.ascii_letters:
			break	
		if formule[i]=='\\':
			if i+7<=l and (formule[i:i+7]=='\\exists' or formule[i:i+7]=='\\forall'):
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
			if i+4<=l and formule[i:i+4]=='\\neg':
				i+=4
				continue
			if (i+4<=l and formule[i:i+4]=='\\lor') or (i+5<=l and formule[i:i+5]=='\\land') or (i+11<=l and formule[i:i+11]=='\\rightarrow') or (i+15<=l and formule[i:i+15]=='\\leftrightarrow'):
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
			if i-6>=0 and ( formule[i-6]=='\\' and (formule[i-6:i+1]=='\\exists' or formule[i-6:i+1]=='\\forall')):
				i-=7
				continue
			if i-3>=0 and ( formule[i-3]=='\\' and formule[i-3:i+1]=='\\lor' ):
				order='post'
				break
			if i-4>=0 and ( formule[i-4]=='\\' and formule[i-4:i+1]=='\\land'):
				order='post'
				break
			if i-10>=0 and ( formule[i-10]=='\\' and formule[i-10:i+1]=='\\rightarrow'):
				order='post'
				break
			if i-14>=0 and (formule[i-14]=='\\' and formule[i-14:i+1]=='\\leftrightarrow'):
				order='post'
				break
			if i-3>=0 and ( formule[i-3]=='\\' and formule[i-3:i+1]=='\\neg'):
				order='post'
				break
			if formule[i] in string.ascii_letters:
				break
			i-=1
		if order=='check':
			order='in'
			
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
