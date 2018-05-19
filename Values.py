from Token import Token
import string
class Variable(Token):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}Variable: {}\n{}negation: {}\n'.format(space,self.name,space,self.negation)
	def __init__(self,name,target_order='in',negation=False,notation='classic',value=False):
		Token.__init__(self,notation)
		self.value=value
		self.target_order=target_order
		self.name=name
		self.negation=negation
	def __repr__(self):

		if self.target_order in ('in','pre'):
			return Token._get_negation_string(self)+ self.name
		else:
			return self.name+Token._get_negation_string(self)
	def neg(self,deepness=0):
		return Variable(self.name,target_order=self.target_order,negation=not self.negation,notation=self.notation,value=self.value)
	def get_value(self):
		if self.negation:
			return not self.value
		else:
			return self.value
	def eliminate_ie(self):
		return self.copy()
	def copy(self):
		return Variable(self.name,target_order=self.target_order,negation=self.negation,notation=self.notation,value=self.value)
	
class Predicate(Token):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}Predicate: {}\n{}Contains: {}\n{}Variables: {}\n{}Constants: {}\n{}Relations: {}\n{}Negation: {}\n{}Value:{}\n'.format(space,self.name,space,self.formule,space,' '.join(self.variables),space,' '.join(self.constants),space,' '.join(self.relations),space,self.negation,space,self.value)
	def __init__(self,name,formule,target_order='in',negation=False,notation='classic',value=False):
		Token.__init__(self,notation)
		self.name=name
		self.formule=formule
		self.target_order=target_order
		self.negation=negation
		self.value=value
		self.constants=[]
		self.variables=[]
		self.relations=[]
		self.process_content(formule)
	def process_content(self,formule):
		contents=formule.split(',')
		for c in contents:
			check=False
			tmp=''
			for i in range(len(c)):
				if c[i] in string.ascii_letters:
					if check:
						self.constants.append(tmp)
						tmp=''
						check=False
					self.variables.append(c[i])
				elif c[i] in string.digits:
					tmp+=str(c[i])
					check=True
				else:
					if check:
						self.constants.append(tmp)
						tmp=''
						check=False
					self.relations.append(c[i])
			if check:
				self.constants.append(tmp)
				tmp=''
				check=False
	def __repr__(self):
		if self.target_order in ('pre','in'):
			return Token._get_negation_string(self)+self.name+'('+str(self.formule)+')'
		else:
			return '('+str(self.formule)+')'+self.name+Token._get_negation_string(self)
	def neg(self,deepness=0):
			return Predicate(self.name,self.formule,target_order=self.target_order,negation=not self.negation,notation=self.notation,function=self.function)
	def get_value(self):
		if self.negation:
			return not self.value
		else:
			return self.value
	def eliminate_ie(self):
		return self.copy()
	def copy(self):
		return Predicate(self.name,self.formule,target_order=self.target_order,negation=self.negation,notation=self.notation,function=self.function)

	def get_variables(self):
		return set([self.name+'('+self.formule+')'])
	def set_values(self,values_pairs):
		self.value=values_pairs[self.name+'('+self.formule+')']
	def prompt_values(self):
		self.value=bool(input(self.name+'('+self.formule+'):'))
