class Forwards_Chaining():
	def __init__(self,KB,query,symbols):
		self.KB = KB
		self.query = query
		self.symbols = symbols
		self.found_symbols = []
		
		self.name = 'Forwards_Chaining'
		
	#Prevents symbols from being included multiple times while ensuring a correct result
	def append_symbol(self,sSymbol):
		if sSymbol not in self.found_symbols:
			self.found_symbols.append(sSymbol)
		else:
			self.found_symbols.remove(sSymbol)
			self.found_symbols.append(sSymbol)
			
	def solve(self):	
		#Go through KB, and set those that are automatically true or false as such
		for statement in self.KB:
			if statement.rightside is statement.leftside[0]:
				if statement.rightside is self.query:
					self.append_symbol(statement.rightside)
					return True,self.found_symbols
					
				statement.rightside.inferred = True
				self.append_symbol(statement.rightside)
			
		
		for statement in self.KB:
			for lSymbol in statement.leftside:
				lSymbol.inferres.append(statement.rightside)
			
			statement.rightside.inferred_by = statement.leftside
			
			
						 
		#There are three states that a node can have, True, False or None.
		#If any inferred_by nodes are false, then inferred is false
		#If any are None, then we skip it
		
		if self.query is None: #To catch invalid queries
			return None,None
			
		while self.query.inferred is None:
			for statement in self.KB:
				statement.rightside.inferred = True
				for lSymbol in statement.leftside:
					#Catches nodes that are not inferred by anything and are therefor false
					if len(lSymbol.inferred_by) == 0 and lSymbol.inferred is None:
						lSymbol.inferred = False
						statement.rightside.inferred = False
					
					#Catches nodes that have not been explored, and prevents premature evaluation
					if lSymbol.inferred is None:
						statement.rightside.inferred = None
						break
						
					if lSymbol.inferred == False:
						statement.rightside.inferred = False
						
				
				if statement.rightside.inferred == True:
					statement.rightside.inferred = True
					self.append_symbol(statement.rightside)

				
				if self.query.inferred is not None:
					for symbol in self.query.inferred_by:
						self.append_symbol(symbol)
						
					self.append_symbol(self.query)
					return self.query.inferred,self.found_symbols
				
		
		self.append_symbol(statement.leftside[0])
		return None,self.found_symbols