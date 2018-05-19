from Token import Token
import string
class Quantifier(Token):
	def __init__(self,token,lower,target_order,negation=False,notation='classic'):
		Token.__init__(self,notation)
		self.target_order=target_order
		self.lower=lower
		self.content=token
		self.negation=negation
		self.variables=[]
		self.process_lower()
	def process_lower(self):
		i=0
		l=len(self.lower)
		while i<l:
			if self.lower[i:i+3] == '\\in':
				i+=3
				continue
			if self.lower[i] in string.ascii_lowercase:
				self.variables.append(self.lower[i])
			i+=1
	def set_target_order(self,target):
		self.target_order=target
		self.content.set_target_order(target)
	def eliminate_ie(self):
		self.content=self.content.eliminate_ie()
		return self
	def get_value(self):
		if self.negation:
			return not self.content.get_value()
		else:
			return self.content.get_value()
	def set_notation(self,variant):
		self.notation=variant
		self.content.set_notation(variant)
		return self
	def total_process_negation(self):
		tmp=self.process_negation()
		tmp.content.total_process_negation()
		return tmp
	def quantifiers_below(self):
		return True
	def remove_negation_from_before_quantifiers(self):
		if self.negation:
			tmp=self.process_negation()
		else:
			tmp=self.copy()
		if tmp.content.quantifiers_below():
			tmp.content=tmp.content.remove_negation_from_before_quantifiers()
		return tmp
class Forall(Quantifier):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}For all:\n{}Negation: {}\n{}Variables: {}\n{}Affected:\n{}'.format(space,space,self.negation,space,' '.join(self.variables),space,self.content.describe(deepness+1))
	def __init__(self,token,lower,target_order,negation=False,notation='classic'):
		Quantifier.__init__(self,token,lower,target_order,negation,notation=notation)
	def neg(self,deepness=0):
		if deepness>0:
			return Exists(self.content.neg(deepness-1),self.lower,self.target_order,notation=self.notation,negation=self.negation)
		else:
			return Forall(self.content,self.lower,self.target_order,notation=self.notation,negation=not self.negation)
	def __repr__(self):
		if self.target_order=='post':
			return str(self.content)+'\\forall'+self.lower+Token._get_negation_string(self)
		else:
			return Token._get_negation_string(self)+'\\forall'+self.lower+' ('+ str(self.content)+')'
	def process_negation(self):
		if self.negation:
			return Exists(self.content.neg(0),self.lower,self.target_order,notation=self.notation,negation=not self.negation)
		else:
			return self.copy()
	def copy(self):
		return Forall(self.content,self.lower,self.target_order,notation=self.notation,negation=self.negation)
class Exists(Quantifier):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}Exists:\n{}Negation: {}\n{}Variables: {}\n{}Affected:\n{}'.format(space,space,self.negation,space,' '.join(self.variables),space,self.content.describe(deepness+1))
	def __init__(self,token,lower,target_order,negation=False,notation='classic'):
		Quantifier.__init__(self,token,lower,target_order,negation,notation)
	def neg(self,deepness=0):
		if deepness>0:
			return Forall(self.content.neg(deepness-1),self.lower,self.target_order,notation=self.notation,negation=self.negation)
		else:
			return Exists(self.content,self.lower,self.target_order,notation=self.notation,negation=not self.negation)
	def __repr__(self):
		if self.target_order=='post':
			return str(self.content)+'\\exists'+self.lower+Token._get_negation_string(self)
		else:
			return Token._get_negation_string(self)+'\\exists'+self.lower +' ('+ str(self.content)+')'
	def process_negation(self):
		if self.negation:
			return Forall(self.content.neg(0),self.lower,self.target_order,notation=self.notation,negation=not self.negation)
		else:
			return self.copy()
	def copy(self):
		return Exists(self.content,self.lower,self.target_order,notation=self.notation,negation=self.negation)
