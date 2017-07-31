class Symbol():	
	def __init__(self,char):
		self.char = char
		self.inferred = None
		
		self.inferred_by = []
		self.inferres = []
		
		def __repr__(self):
			return self.char
		def __str__(self):
			return self.char