from dictionary import notation
class Token:
	def __init__(self):
		self.notation='classic'
	def set_notation(self,variant):
		self.notation=variant
	def change_negation(self):
		if self.negation:
			self.negation=False
		else:
			self.negation=True
		return self
	def process_negation(self):
		return self.neg()
	def set_target_order(self,target):
		self.target_order=target
	def eliminate_ie(self):
		return self
	def _get_negation_string(self):
		if self.negation:
			return notation[self.notation]['neg']
		else:
			return ''
