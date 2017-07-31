import math

class Truth_Table():
	def __init__(self,KB,query,symbols):
		self.KB = KB
		self.query = query
		self.symbols = symbols
		
		self.name = 'Truth_Table'
		self.self_implied = []
		for statement in self.KB:
			if statement.leftside[0] == statement.rightside:
				self.self_implied.append(statement.rightside.char)
		
		self.length = int(math.pow(2,len(self.self_implied)))
		self.rows = [] #List of columns. Columns are boolean list.
		self.title_row = [] #Characters, statements, etc
		self.path = [] #List of rows to query
	
	def construct_table(self):
		#Populate table 
		offset = 1 #Offset is the number of cells that are set as true or false each iteration. 
		for symbol in self.self_implied:
			count = 0 #Acts as index
			flip = False
			column = []
			
			while count < self.length:
				column.append(flip)
				count += 1
				
				if count % offset == 0 and count != 0: #Checks if count is a multiple of offset.
					flip = not flip #Flip boolean
			column.append(flip)
			offset = offset*2
			self.rows.insert(0,column)
			
		#Add symbols to title_row
		for i in range(len(self.self_implied)):
			self.title_row.append(self.self_implied[i])
			
		#Add statements to title_row
		for statement in self.KB:
			if statement.rightside.char not in self.self_implied:
				self.title_row.append(statement)
				
		for i in range(0,len(self.title_row) - len(self.self_implied)):
			self.rows.append([None]*self.length) #Add empty columns for each non-existing element in title_row
		
		
	def print_top(self):
		to_print = ""
		for s in self.title_row:
			#If it's a statement, add the statement. If it's a char, add the char.
			try:
				to_print += s.raw_statement
			except:
				to_print += s
				
			#Add spaces to stop them cramping
			#title_row has both statements and symbols
			row_length = 5 #False is 5, should be max
			try:
				title_length = len(s.raw_statement)
			except:
				title_length = len(s)
				
			diff = title_length - row_length
			if diff < 0:
				for i in range(diff, 0):
					to_print += " "
			
			to_print+=("|")
		print(to_print)
		
		
	def print_table(self):
		self.print_top()
		for i in range(self.length):
			to_print = ""
			
			for r in range(0,len(self.rows)):
				#Add row
				to_print+=str(self.rows[r][i])
				
				#Add spaces to stop them cramping
				#title_row has both statements and symbols
				try:
					row_length = len(self.title_row[r].raw_statement)
				except:
					row_length = len(self.title_row[r])
				
				
				
				if row_length > 5:
					diff = row_length - len(str(self.rows[r][i]))
					
					if diff > 0:
						for i in range(0,diff):
							to_print += " "
				elif self.rows[r][i] in [True,None]: #Both are 4 letters long, so need to be expanded to minimum
					to_print += " "
				
				#Seperator
				to_print+=("|")
			print(to_print)
			
				
	def solve(self):
		self.construct_table()
		
		#Gets the statement that proves the query
		query_index = 0
		for statement in self.KB:
			query_index += 1
			if statement.rightside == self.query:
				query_statement = statement
				
				break
			
		
		query_index += len(self.self_implied) 
		found_query = False
		
		count = 0 #Value to be returned
		while found_query == False:
			for c in range(len(self.self_implied),len(self.title_row)): #For every non-symbol column
				for l in range(0,self.length): #For each boolean row
					if self.rows[c][l] is None: #Prevents evaluation of already evaluated rows
						#True by default, so true conditions cause a continue.
						#None if either is None.
						#False is either is False.
						result = True
						
						for symbol in self.title_row[c].leftside: #Evaluate cell	
							
							#Find row that implies symbol
							row_index = None

							if symbol.char in self.self_implied:
								for s in range(0,len(self.self_implied)):
									if symbol.char == self.self_implied[s]:
										row_index = s
										break
										
							else:
								for s in range(len(self.self_implied),len(self.title_row)):
									if self.title_row[s].rightside.char == symbol.char:
										row_index = s
										break
			
							#If it is not implied by a statement, and it does not imply itself, then it is false
							if row_index is None:
								result = False
								break
							
							#Check if the item in that row, with the same column, is True, False or None
							if self.rows[row_index][l] is None:
							
								result = None
								continue
							
							elif self.rows[row_index][l] == False:
								result = False
								break
								
						self.rows[c][l] = result
						
			#Checks if query has been evaluated for end condition
			try:
				if self.rows[query_index][0] is not None:
					found_query = True
			except: #If it is nowhere, like g in the test file
				return None,0
				
		self.print_table()
		self.evaluate(query_index)
		
		#Check if an entire row is true to see if it is true
		candidates = []
		
		#Populate candidate rows
		for r in self.path:
			for l in range(0,self.length): #For each boolean row
				if self.rows[r][l]:
					candidates.append(l)
					
		#Go through candidate rows, and remove those that are not true
		for r in candidates:
			for l in range(0,len(self.rows)): #For each boolean row
				if self.rows[l][r] == False:
					candidates.remove(r)
					break
					
		return len(candidates)>0,len(self.path)
						
	def evaluate(self,index):
		#Adds value to path
		if index not in self.path:
			self.path.append(index)	
		
		#Recursive addition
		if self.rows[index][0] is not None:
			st = self.title_row[index]
			
			if index >= len(self.self_implied):
				for symbol in self.title_row[index].leftside:
					for i in range(len(self.self_implied),len(self.title_row)):
						if symbol.char == self.title_row[i].rightside.char:
							
							#Deals with single characters, aka end of a valid chain
							if i < len(self.self_implied):
								if index not in self.path:
									self.path.append(index)
									break
							else:
								self.evaluate(i)
								break
						
			else: #End of non-valid chain
				for i in range(0,len(self.KB)):
					if self.title_row[index] == self.KB[i].rightside.char:
						if self.KB[i].rightside.char != self.KB[i].leftside[0].char:
							print("Failed! ", self.KB[i].rightside.char, " was not found in KB")
							for i in range(0,self.length):
								self.rows[index] = False
								
										
			
		
		