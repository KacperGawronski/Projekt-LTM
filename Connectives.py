from Token import Token
from dictionary import notation

class Connective(Token):
	def __init__ (self,token_a,token_b,target_order,negation=False,notation='classic'):
		Token.__init__(self,notation)
		self.target_order=target_order
		self.content_a=token_a
		self.content_b=token_b
		self.negation=negation
	def set_target_order(self,target):
		self.target_order=target
		self.content_a.set_target_order(target)
		self.content_b.set_target_order(target)
	def eliminate_ie(self):
		self.content_a=self.content_a.eliminate_ie()
		self.content_b=self.content_b.eliminate_ie()
		return self.set_notation(self.notation)
	def set_notation(self,variant):
		self.notation=variant
		self.content_a.set_notation(variant)
		self.content_b.set_notation(variant)
		return self
	def total_process_negation(self):
		tmp=self.process_negation()
		tmp.content_a=tmp.content_a.total_process_negation()
		tmp.content_b=tmp.content_b.total_process_negation()
		return tmp
	def quantifiers_below(self):
		return self.content_a.quantifiers_below() or self.content_b.quantifiers_below()
	def remove_negation_from_before_quantifiers(self):
		if self.quantifiers_below():
			tmp=self.process_negation()
			tmp.content_a=tmp.content_a.remove_negation_from_before_quantifiers()
			tmp.content_b=tmp.content_b.remove_negation_from_before_quantifiers()
			return tmp
		else:
			return self.copy()
	def get_variables(self):
		return self.content_a.get_variables()|self.content_b.get_variables()
	def get_tree(self):
		return [self.content_a.get_tree(),self.content_b.get_tree()]
	def set_values(self,values_pairs):
		self.content_a.set_values(values_pairs)
		self.content_b.set_values(values_pairs)
	def prompt_values(self):
		values_pairs={}
		for i in self.get_variables():
			values_pairs[i]=bool(input(i+': '))
		self.content_a.set_values(values_pairs)
		self.content_b.set_values(values_pairs)

class And(Connective):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}And:\n{}Negation {}\n{}\n{}_AND_\n{}\n'.format(space,space,self.negation,self.content_a.describe(deepness+1),space,self.content_b.describe(deepness+1))
	def __init__(self,token_a,token_b,target_order,negation=False,notation='classic'):
		Connective.__init__(self,token_a,token_b,target_order=target_order,negation=negation,notation=notation)
	def __repr__(self):
		if self.target_order == "in":
			return Token._get_negation_string(self)+notation[self.notation]['lbracket']+str(self.content_a) + notation[self.notation]['and'] + str(self.content_b)+notation[self.notation]['rbracket']
		if self.target_order == "pre":
			return Token._get_negation_string(self)+notation[self.notation]['and'] +notation[self.notation]['lbracket']+ str(self.content_a)+str(self.content_b)+notation[self.notation]['rbracket']	
		if self.target_order == "post":
			return notation[self.notation]['lbracket']+str(self.content_a)+str(self.content_b) +notation[self.notation]['rbracket']+notation[self.notation]['and'] + Token._get_negation_string(self)
	def neg(self,deepness=0):
		if deepness>0:
			return Or(self.content_a.neg(deepness-1),self.content_b.neg(deepness-1),self.target_order,notation=self.notation,negation=self.negation).set_notation(self.notation)
		else:
			return And(self.content_a,self.content_b,target_order=self.target_order,notation=self.notation,negation=not self.negation).set_notation(self.notation)
	def process_negation(self):
		if self.negation:
			return Or(self.content_a.neg(1),self.content_b.neg(1),self.target_order,notation=self.notation)
		else:
			return self.copy()
	def get_value(self):
		if self.negation:
			return not self.content_a.get_value() or not self.content_b.get_value()
		else:	
			return self.content_a.get_value() and self.content_b.get_value()
	def copy(self):
		 return And(self.content_a,self.content_b,target_order=self.target_order,notation=self.notation,negation=self.negation)
class Or(Connective):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}Or:\n{}Negation {}\n{}\n{}_OR_\n{}\n'.format(space,space,self.negation,self.content_a.describe(deepness+1),space,self.content_b.describe(deepness+1))
	def __init__(self,token_a,token_b,target_order,negation=False,notation='classic'):
		Connective.__init__(self,token_a,token_b,target_order=target_order,negation=negation,notation=notation)
	def __repr__(self):
		if self.target_order == "in":
			return Token._get_negation_string(self)+notation[self.notation]['lbracket']+str(self.content_a) + notation[self.notation]['or'] + str(self.content_b)+notation[self.notation]['rbracket']
		if self.target_order == "pre":
			return Token._get_negation_string(self)+notation[self.notation]['or'] +notation[self.notation]['lbracket']+ str(self.content_a)+str(self.content_b)+notation[self.notation]['rbracket']
		if self.target_order == "post":
			return notation[self.notation]['lbracket']+str(self.content_a)+str(self.content_b)+notation[self.notation]['rbracket'] + notation[self.notation]['or']+Token._get_negation_string(self)
	def neg(self,deepness=0):
		if deepness>0:
			return And(self.content_a.neg(deepness-1),self.content_b.neg(deepness-1),target_order=self.target_order,notation=self.notation,negation=self.negation).set_notation(self.notation)
		else:
			return Or(self.content_a,self.content_b,target_order=self.target_order,notation=self.notation,negation=not self.negation).set_notation(self.notation)
	def process_negation(self):
		if self.negation:
			return And(self.content_a.neg(0),self.content_b.neg(0),self.target_order,notation=self.notation)
		else:
			return self.copy()
	def get_value(self):
		if self.negation:
			return not self.content_a.get_value() and not self.content_b.get_value()
		else:
			return self.content_a.get_value() or self.content_b.get_value()
	def copy(self):
		return Or(self.content_a.neg(0),self.content_b.neg(0),self.target_order,notation=self.notation,negation=self.negation)
class Implication(Connective):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}Implication:\n{}negation: {}\n{}{}\n=>\n{}\n'.format(space,space,self.negation,space,self.content_a.describe(deepness+1),self.content_b.describe(deepness+1))
	def __init__(self,token_a,token_b,target_order,negation=False,notation='classic'):
		Connective.__init__(self,token_a,token_b,target_order=target_order,negation=negation,notation=notation)
	def __repr__(self):
		if self.target_order == "in":
			return Token._get_negation_string(self)+notation[self.notation]['lbracket']+str(self.content_a) + notation[self.notation]['implication'] + str(self.content_b)+notation[self.notation]['rbracket']
		if self.target_order == "pre":
			return Token._get_negation_string(self)+notation[self.notation]['implication'] +notation[self.notation]['lbracket']+ str(self.content_a)+str(self.content_b)+notation[self.notation]['rbracket']
		if self.target_order == "post":
			return notation[self.notation]['lbracket']+str(self.content_a)+str(self.content_b)+notation[self.notation]['rbracket'] +notation[self.notation]['implication'] + Token._get_negation_string(self)
	def neg(self,deepness=0):
		if deepness>0:
			return And(self.content_a.neg(deepness-1),self.content_b.neg(deepness-1),target_order=self.target_order,notation=self.notation,negation=self.negation).set_notation(self.notation)
		else:
			return Implication(self.content_a,self.content_b,target_order=self.target_order,negation=not self.negation,notation=self.notation)
	def process_negation(self):
		if self.negation:
			return And(self.content_a.neg(0),self.content_b.neg(0),self.target_order,notation=self.notation)
		else:
			return self.copy()
		
	def eliminate_ie(self):
		return Or(self.content_a.neg(0),self.content_b,self.target_order,negation=self.negation,notation=self.notation).eliminate_ie()
	def get_value(self):
		if self.negation:
			return self.content_a.get_value and not self.content_b.get_value()
		else:
			print(self.content_a.get_value(),self.content_b.get_value())
			return not self.content_a.get_value() or self.content_b.get_value()
	def copy(self):
		return Implication(self.content_a,self.content_b,target_order=self.target_order,negation=self.negation,notation=self.notation)
class Equivalence(Connective):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}Equivalence:\n{}negation: {}\n{}\n{}<=>\n{}\n'.format(space,space,self.negation,self.content_a.describe(deepness+1),space,self.content_b.describe(deepness+1))
	def __init__(self,token_a,token_b,target_order,negation=False,notation='classic'):
		Connective.__init__(self,token_a,token_b,target_order=target_order,negation=negation,notation=notation)
	def __repr__(self):
		if self.target_order == "in":
			return Token._get_negation_string(self)+notation[self.notation]['lbracket']+str(self.content_a) + notation[self.notation]['equivalence'] + str(self.content_b)+notation[self.notation]['rbracket']
		if self.target_order == "pre":
			return Token._get_negation_string(self)+notation[self.notation]['equivalence'] + notation[self.notation]['lbracket']+str(self.content_a)+str(self.content_b)+notation[self.notation]['rbracket']	
		if self.target_order == "post":
			return notation[self.notation]['lbracket']+str(self.content_a)+str(self.content_b)+notation[self.notation]['rbracket'] +notation[self.notation]['equivalence']+Token._get_negation_string(self)
	def neg(self,deepness=0):
		if deepness>0:
			return Or(Implication(self.content_a,self.content_b,target_order=self.target_order,notation=self.notation).neg(deepness-1),Implication(self.content_b,self.content_a,target_order=self.target_order,notation=self.notation).neg(deepness-1),target_order=self.target_order,notation=self.notation,negation=self.negation).set_notation(self.notation)
		else:
			return Equivalence(self.content_a,self.content_b,target_order=self.target_order,negation=not self.negation,notation=self.notation)
	def process_negation(self):
		if self.negation:
			return Or(Implication(self.content_a,self.content_b,self.target_order,notation=self.notation).neg(1),Implication(self.content_b,self.content_a,self.target_order,notation=self.notation).neg(1),self.target_order,notation=self.notation)
		else:
			return self.copy() 
	def eliminate_ie(self):
		return And(Implication(self.content_a,self.content_b,target_order=self.target_order,notation=self.notation).eliminate_ie(),Implication(self.content_b,self.content_a,target_order=self.target_order,notation=self.notation).eliminate_ie(),target_order=self.target_order,negation=self.negation).eliminate_ie().set_notation(self.notation)
	def get_value(self):
		if self.negation:
			return (self.content_a.get_value() or self.content_b.get_value()) and (not self.content_a.get_value() or not self.content_b.get_value())
		else:
			return (self.content_a.get_value() and self.content_b.get_value()) or (not self.content_a.get_value() and not self.content_b.get_value())
	def copy(self):
		return Equivalence(self.content_a,self.content_b,target_order=self.target_order,negation=self.negation,notation=self.notation)
	
