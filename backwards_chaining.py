class Backwards_Chaining():
	def __init__(self,KB,query,symbols):
		self.KB = KB
		self.query = query
		self.symbols = symbols
		self.found_symbols = []
		
		self.name = 'Backwards_Chaining'
	
	#Gets symbol object from char
	def get_symbol(self,char):
		#Catch symbols masquerading as chars
		try:
			char.char = char.char
			
			return char
		#Gets symbol with matching char
		except:
			for symbol in self.symbols:	
				if symbol.char == char:
					return symbol
			
	def get_next_statement(self,current_char):
		#Find statement that inferres current char, so right hand side
		for statement in self.KB:
			if statement.rightside == current_char and statement.visited == False:
				return statement
	
	#Recursion
	def get_inferrer(self,sSymbol):
		if sSymbol is not None and sSymbol.inferred != True:
			#Find statement with query
			current_statement = self.get_next_statement(sSymbol)
			if current_statement is not None:
				sSymbol.inferred_by = current_statement.leftside
				
				current_statement.visited = True #Prevents duplication
				self.found_symbols.insert(0,sSymbol)
				
				if current_statement.leftside[0] == current_statement.rightside:
					current_statement.rightside.inferred = True
					return None
				
				if len(sSymbol.inferred_by) == 0:
					return None
					
				for symbol in sSymbol.inferred_by:
					self.get_inferrer(symbol)	
					
			else:
				sSymbol.inferred = False
		
	def set_inferred(self,sSymbol):
		is_true = True
		
		if len(sSymbol.inferred_by) == 0: #Symbols that are not inferred by anything
			is_true = False
		else:
			for inferrer in sSymbol.inferred_by:
				if inferrer.inferred == False:
					is_true = False
					break
					
		sSymbol.inferred = is_true
			
			
			
	def solve(self):	
		#Gets a chain of symbols and the statements that lead them there
		self.get_inferrer(self.query)

		#Implements logic to set them as true or false
		for symbol in self.found_symbols:
			self.set_inferred(symbol)
			
		if self.query is None:
			return None,None
		return self.query.inferred,self.found_symbols