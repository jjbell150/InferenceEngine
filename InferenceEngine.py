from symbol import Symbol
from statement import Statement

from forwards_chaining import Forwards_Chaining
from backwards_chaining import Backwards_Chaining
from truth_table import Truth_Table

import sys

class Main():
	def __init__(self):
		#If parameters are missing then they will default to unentered, which will trigger re _entry of both arguments
		try:
			self.file_name = sys.argv[1].lower() #File name
		except:
			self.file_name = 'Unentered'
			
		try:
			self.algorithm = sys.argv[2].lower() #Algorithm name
		except:
			self.algorithm = 'Unentered'
			
		try:
			self.language = sys.argv[3].lower() #Language
		except:
			self.language = "propositional"
			
		self.operators = ['&','=>']
		self.lines = self.get_lines() #Converts the file into a list
		self.symbols = self.get_symbols() #Gets a list of unique symbol objects
		self.KB = self.get_kb() #Creates the KB
		self.query = self.get_query() #Gets the query in object form	
		self.solver = self.find_solver() #Turn self.algorithm name into object reference
		
		result,query_statements = self.solver.solve() #The actual solving part
		self.print_result(result,query_statements) #Print results
	
	#Converts the name into an actual file, done this way to allow me to use several aliases
	def find_solver(self):
		solver = None
		while solver is None:
			if self.algorithm == 'backwards _chaining' or self.algorithm == 'bc': 
				solver = Backwards_Chaining(self.KB,self.query,self.symbols)
			elif self.algorithm == 'forwards _chaining' or self.algorithm == 'fc':
				solver = Forwards_Chaining(self.KB,self.query,self.symbols)
			elif self.algorithm == 'truth _table' or self.algorithm == 'tt':
				solver = Truth_Table(self.KB,self.query,self.symbols)			
			else:
				print('Valid self.algorithms are: Backwards _Chaining(BC), Forward _Chaining(FC), Truth Table (TT)')
				print('Please enter an self.algorithm:')
				self.algorithm = input()
		
		return solver
	def get_query(self):
		string_query = self.lines[3]
		for symbol in self.symbols:
			if symbol.char == string_query:
				return symbol
		
		print("Invalid query")
	def print_result(self,result,query_statements):
		if result is not None:
			print(str(result) + ": ")
			if self.algorithm == "tt" or self.algorithm == 'truth _table':
				print(query_statements)
			else:
				for symbol in query_statements:
					print(symbol.char)
					print(symbol.inferred)
		else:
			print("Inferrence failed! Unable to determine from input.")
		
	def get_lines(self):
		lines = None
		while lines is None:
			try:
				file = open(self.file_name, 'r')
				lines = file.readlines()
				file.close()
			except:
				print('Please enter a valid file:')
				self.file_name = input()
		return lines
		
	def convert_from_english(self):
		raw = self.lines[1].replace('then','=>').replace('itis','').replace('if','').replace('and','&') #List of statements
		prop_KB = []
		
		return raw
					
		
	def get_kb(self):
		if self.language == 'english':
			raw_KB = self.convert_from_english().replace(' ','').replace('\n','').split(';') #List of statementsself.convert_from_english()
		elif self.language == 'propositional':
			raw_KB = self.lines[1].replace(' ','').replace('\n','').split(';') #List of statements
			
		raw_KB.remove(raw_KB[len(raw_KB)-1]) #Removes empty element from last ; 
		
		#Creates list of statement objects
		KB = []
		for raw_statement in raw_KB:
			KB.append(Statement(raw_statement))
		
		#Fills out the KB
		for statement in KB:
			left_side = True
			char_index = 0
			char = statement.raw_statement[char_index]
			
			while char_index < len(statement.raw_statement): #Checks out of bounds
				#Deals with conjunctions, of which we can have as many as we want
				try:
					if statement.raw_statement[char_index+1] == '&':
						for symbol in self.symbols:
							if symbol.char == char:
								statement.leftside.append(symbol)
								break
								
						char_index += 2
						char = statement.raw_statement[char_index]
						#print(char)
				except:
					pass
				
				#Deals with the rightside transition
				try:
					if statement.raw_statement[char_index+1] == '=' and statement.raw_statement[char_index+2] == '>':
						for symbol in self.symbols:
							if symbol.char == char:
								statement.leftside.append(symbol)
								break
						
						left_side = False
						char_index += 3
						
						char = statement.raw_statement[char_index]
				except:
					pass
					
				#Deals with multicharacter symbols, up to any length
				try:
					char_index += 1
					char += statement.raw_statement[char_index]
				except: #It is at the end, works
					for symbol in self.symbols:
						if symbol.char == char:
							if left_side:
								statement.leftside.append(symbol)
							statement.rightside = symbol
							break
						
			statement.leftside_length = len(statement.leftside)
		return KB
		
	def get_symbols(self):
		if self.language == 'english':
			raw_symbols = self.convert_from_english().replace('&',';').replace('=>',';').replace(' ', '').replace('\n','').split(';') #Get a list of all non-operator symbols with duplicates
		elif self.language == 'propositional':
			raw_symbols = self.lines[1].replace('&',';').replace('=>',';').replace(' ', '').replace('\n','').split(';') #Get a list of all non-operator symbols with duplicates
		raw_symbols.sort()
		
		string_symbols = [] #Clean string symbol list with no duplicates
		symbols = [] #Clean list of symbol objects
		
		for symbol in raw_symbols:
			if symbol not in string_symbols:
				string_symbols.append(symbol)
				
		string_symbols.remove(string_symbols[0]) #First element will always be empty space due to it splitting on ;
		for symbol in string_symbols:
			symbols.append(Symbol(symbol))
		#	print (symbol)
		
		return symbols
Main()
