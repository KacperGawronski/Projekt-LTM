from Token import Token
import string
class Variable(Token):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}Variable: {}\n{}negation: {}\n'.format(space,self.name,space,self.negation)
	def __init__(self,name,target_order,negation=False,value=False):
		Token.__init__(self)
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
		if deepness>0:
			return Variable(self.name,self.target_order,not self.negation)
		else:
			return self
	def get_value(self):
		return self.value
class Predicate(Token):
	def describe(self,deepness=0):
		space='\t'*deepness
		return '{}Predicate: {}\n{}Contains: {}\n{}Variables: {}\n{}Constants: {}\n{}Relations: {}\n{}Negation: {}\n'.format(space,self.name,space,self.formule,space,' '.join(self.variables),space,' '.join(self.constants),space,' '.join(self.relations),space,self.negation)
	def __init__(self,name,formule,target_order,negation=False,function=lambda x:False):
		Token.__init__(self)
		self.name=name
		self.formule=formule
		self.target_order=target_order
		self.negation=False
		self.function=function
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
	def neg(self,deepness):
		if deepness>0:
			return Predicate(self.name,self.formule,self.target_order,not self.negation)
		else:
			return self
	def get_value(self):
		return self.function(self.formule)
