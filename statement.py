class Statement():	
	def __init__(self,string_statement):
		#Standalone characters are both left and right
		self.leftside = []
		self.rightside = None
		
		self.leftside_length = 1
		self.is_true = False
		
		self.visited = False
		self.raw_statement = string_statement
		
		def __repr__(self):
			return self.raw_statement
		def __str__(self):
			return self.raw_statement