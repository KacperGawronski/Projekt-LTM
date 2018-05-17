from Token import Token
import string
class Quantifier(Token):
	def __init__(self,token,lower,order,target_order,negation=False):
		Token.__init__(self)
		self.order=order
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
class Forall(Quantifier):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}For all:\n{}Negation: {}\n{}Variables: {}\n{}Affected:\n{}'.format(space,space,self.negation,space,' '.join(self.variables),space,self.content.describe(deepness+1))
	def __init__(self,token,lower,order,target_order,negation=False):
		Quantifier.__init__(self,token,lower,target_order,order,negation)
	def neg(self,deepness=0):
		if deepness>0:
			if self.negation:
				return Exists(self.content.neg(deepness-1),self.lower,self.order,self.target_order,False)
			else:
				return Exists(self.content.neg(deepness-1),self.lower,self.order,self.target_order,True)
		else:
			return self
	def __repr__(self):
		if self.target_order=='post':
			return str(self.content)+'\\forall'+self.lower+Token._get_negation_string(self)
		else:
			return Token._get_negation_string(self)+'\\forall'+self.lower+' ('+ str(self.content)+')'
class Exists(Quantifier):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}Exists:\n{}Negation: {}\n{}Variables: {}\n{}Affected:\n{}'.format(space,space,self.negation,space,' '.join(self.variables),space,self.content.describe(deepness+1))
	def __init__(self,token,lower,order,target_order,negation=False):
		Quantifier.__init__(self,token,lower,target_order,order,negation)
	def neg(self,deepness=0):
		if deepness>0:
			if self.negation:
				return Forall(self.content.neg(deepness-1),self.lower,self.order,self.target_order,False)
			else:
				return Forall(self.content.neg(deepness-1),self.lower,self.order,self.target_order,True)
		else:
			return self
	def __repr__(self):
		if self.target_order=='post':
			return str(self.content)+'\\exists'+self.lower+Token._get_negation_string(self)
		else:
			return Token._get_negation_string(self)+'\\exists'+self.lower +' ('+ str(self.content)+')'