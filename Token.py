from dictionary import notation
from itertools import product

class Token:
	def __init__(self,variant='classic'):
		self.notation=variant
	def set_notation(self,variant):
		self.notation=variant
		return self
	def change_negation(self):
		self.negation=not self.negation
		return self
	def process_negation(self):
		return self.copy()
	def set_target_order(self,target):
		self.target_order=target
	def eliminate_ie(self):
		print('ERROR ELIMINATE_IE: NOT IMPLEMENTED')
	def _get_negation_string(self):
		if self.negation:
			return notation[self.notation]['neg']
		else:
			return ''
	def total_process_negation(self):
		return self.copy()
	def quantifiers_below(self):
		return False
	def remove_negation_from_before_quantifiers(self):
		return self.process_negation()
	def ref_object(self):
		return self
	def get_variables(self):
		return set([self.name])
	def get_tree(self):
		return self
	def set_values(self,values_pairs):
		self.value=values_pairs[self.name]
	def prompt_values(self):
		self.value=bool(input(self.name+':'))
	def yield_product(self,variables):
		pr=product([True,False],repeat=len(variables))
		for i in pr:
			yield list(i)
	def find_valuation(self):
		variables = self.get_variables()
		pairs=[]
		for i in self.yield_product(variables):
			pairs.append(dict(zip(variables,i)))
		values=[]
		for i in pairs:
			self.set_values(i)
			values.append((i,self.get_value()))
		return values
	def is_tautology(self,values):
		if all(map(lambda x:x[1],values)):
			return True
		else:
			return False
	def print_ascii_evaluation_table(self):
		variables=list(self.get_variables())
		print(variables)
		values=self.find_valuation()
		print(('\t'.join(variables))+'\t'+self.__repr__())
		for i in values:
			for j in range(len(variables)):
				print(str(1*i[0][variables[j]]),end='\t')
			print(str(1*i[1]))
		print('Is tautology: ',self.is_tautology(values))
	def dnf(self):
		'''dysjunkcyjna postać normalna, odpowiednik apn'''
		values=self.find_valuation()
		result=''
		values=list(filter(lambda x:x[1],values))
		if self.target_order=='pre':
			l=len(values)
			for i in range(l):
				if i<l-1:
					result+=notation[self.notation]['or']
				result+=notation[self.notation]['lbracket']
				m=len(values[i][0])
				k=0
				for j in values[i][0]:
					result+=notation[self.notation]['and'] if k<m-1 else ''
					result+=j if values[i][0][j] else self._get_negation_string()+j
					k+=1
				result+=notation[self.notation]['rbracket']
		elif self.target_order=='in':
			l=len(values)
			for i in range(l):
				m=len(values[i][0])
				k=0
				result+=notation[self.notation]['lbracket']
				for j in values[i][0]:
					result+=j if values[i][0][j] else self._get_negation_string()+j
					result+=notation[self.notation]['and'] if k<m-1 else ''
					k+=1
				result+=notation[self.notation]['rbracket']
				if i<l-1:
					result+=notation[self.notation]['or']
		
		elif self.target_order=='post':
			l=len(values)
			for i in range(l):
				result+=notation[self.notation]['lbracket']
				m=len(values[i][0])
				k=0
				for j in values[i][0]:
					result+=j if values[i][0][j] else j+self._get_negation_string()
					result+=notation[self.notation]['and'] if k>0 else ''
					k+=1
				result+=notation[self.notation]['rbracket']
				if i>0:
					result+=notation[self.notation]['or']
		return result
	def cnf(self):
		values=self.find_valuation()
		result=''
		values=list(filter(lambda x:not x[1],values))
		if self.target_order=='pre':
			l=len(values)
			for i in range(l):
				if i<l-1:
					result+=notation[self.notation]['and']
				result+=notation[self.notation]['lbracket']
				m=len(values[i][0])
				k=0
				for j in values[i][0]:
					result+=notation[self.notation]['or'] if k<m-1 else ''
					result+=j if values[i][0][j] else self._get_negation_string()+j
					k+=1
				result+=notation[self.notation]['rbracket']
		elif self.target_order=='in':
			l=len(values)
			for i in range(l):
				m=len(values[i][0])
				k=0
				result+=notation[self.notation]['lbracket']
				for j in values[i][0]:
					result+=j if values[i][0][j] else self._get_negation_string()+j
					result+=notation[self.notation]['or'] if k<m-1 else ''
					k+=1
				result+=notation[self.notation]['rbracket']
				if i<l-1:
					result+=notation[self.notation]['and']
		
		elif self.target_order=='post':
			l=len(values)
			for i in range(l):
				result+=notation[self.notation]['lbracket']
				m=len(values[i][0])
				k=0
				for j in values[i][0]:
					result+=j if values[i][0][j] else j+self._get_negation_string()
					result+=notation[self.notation]['or'] if k>0 else ''
					k+=1
				result+=notation[self.notation]['rbracket']
				if i>0:
					result+=notation[self.notation]['and']
		return result
