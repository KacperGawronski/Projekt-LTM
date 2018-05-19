from dictionary import notation
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
