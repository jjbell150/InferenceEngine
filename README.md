Usage:
	InferenceEngine.exe [filename] [method] (language)
	InferenceEngine.exe testENG.txt fc English
	
	Method is type of inference; so fc (Forwards chaining), bc (Backwards chaining) or tt (Truth Table). 
	Language is optional, it will default to propositional.

	English KB's need to be in the form: if x then y (if raining then wet) and if x and z then y (if raining and outside then wet).
	Propositional KB's need to be in the form x=>y and x&z=>y.
	Each statement needs a ; after it to be recognized.
	
	A valid propositional KB can be used as an English KB. 
Terms:
	Symbol: Propositional symbols, stores whether it is inferred, what it infers and what infers it.
	Symbols: A list of symbols.
	Character: Plaintext representation of a symbol, "P2" for example.
	Operator: Either & or =>, essentially anything that isn't a symbol or whitespace.
	Statement: A collection of symbols separated by operators, which has a left and a right side.
	KB: A list of statements.

	Inferrer: A symbol that leads up to another symbol, in a tree structure it would be a child.
	Inferrers: All symbols that lead up to another symbol.
	Inferred: Whether a symbol is logically inferred, so if all of its inferrers are True.
	Infers: Logically concludes. I.e. All inferrers are True, so the inferred symbol is True.

Algorithms:
	Backwards_Chaining:
		Time taken: 8 hours

		This was the first one I created, and was one of the more difficult, as I had a hard time with the recursion.
		
		It works by backtracking from the query to its inferrers, and then from each inferrer to its own inferrers, right until the end.
		This creates a form of tree, which is searched in a depth-first fashion, left to right.
		
		Recursion step-by-step:
			1. Take current symbol (Starting with query).
			2. Find statement that infers symbol.
			3. Set inferrers as such.
			4. Send inferrer to the start to find its own inferrers.
			5. Repeat until all inferrers have been explored. 

		No known bugs.

	Forwards_Chaining:
		Time taken: 4 hours
		
		Between creating this and Backwards_Chaining I refactored the Statement class and get_KB method.
		So I was able to use them to greatly lower the complexity of the algorithm, which I did not have with the first one.
	
		It works by looping through each statement, checking if it is inferred, and then setting the rightside symbol as such.
		It repeats that loop until it has determined if the query is inferred or not, at which point it exits and returns all previous inferred symbols.
		
		In terms of a tree, it acts like a breadth_first search that starts from the bottom and works its way up.
		
		Step-by-step:
			1. Do a preliminary loop through the KB to set symbols that infer themselves as True
			2. Do another loop through to set inferred_by and inferres for each symbol
			3. Enter the main loop
			4. Check each symbol in the leftside of a statement to see if they are all True, or if one of them is false or neither.
			5. If all are true, then rightside is true. If one is false, rightside is false. If one is neither, then rightside is neither, which prevent premature evaluation.
			6. Repeat 4 and 5 until query has been determined to be true of false, and then return it.
		
		False is prioritized over neither, given the fact that we do not need to know how badly it failed, just that it did, like alpha-beta pruning.

		No known bugs.

	Truth-Table checking
		Time taken: 10 hours

		I spent a lot of time on the logic that creates the table, using offsets and recursion to generate the starting values in under 15 lines. 
		Unfortunately this left me with little time to work on the actual inference logic, so it is quite buggy.
		It ended up being rather complicated, and trying to fix a lot of those bugs ends up breaking it, so I decided to leave them and take the penalty rather than refactor it all. 
		Output is correct for the included test file and query, but other more complicated queries are sometimes wrong.

		It works by creating a truth-table with the self-inferring symbols and filling it in from there, which creates a form of tree.
		I go through that tree in a depth-first fashion, crossing out branches that lead to a False value.
		From there I check if there are more than 0 valid branches at the end, and return that to get the answer.
		I also return the depth of that tree for the second part of the required output.
		
		Step-by-step:
			1. Generate the starting values using an offset starting at 1 that doubles for each symbol to the left.
			It sets a block of values, the size of which is the offset, using a T-Flip-Flop that starts on False and flips each time the offset is reached, which is checked with using a modulus operator.
			2. It creates a title row with the symbols and sentences that correspond with the actual table's values, with extra columns for each sentence.
			3. It finds the row index value that determines the query.
			4. It loops through each cell setting them as True, False or None depending on how they are inferred.
			5. It checks if the query index row has been evaluated, and if so it breaks the evaluation loop.
			6. It creates a chain of index rows from the query to the start recursively.
			7. It goes through those index rows and prunes those rows that have a false along the chain.
			8. It returns True if there are any valid candidates left, and it returns the depth of those chains.
		
		Bugs:
			- The table printing method will only correctly display part of the table, showing many values beyond the first few as entirely False or None, when they are not.
			- It will rarely correctly infer values that are inferred by two symbols. Sometimes it will just outright fail, sometimes it will find the right value, sometimes it will have the wrong depth.
			- It will fail if you try to infer a symbol that infers itself, or that is not inferred at all.
			- It won't work with most English statements for some bizarre reason.
			Essentially it only works well for chains that consist of a single symbol inferring another, like d.
Extra:
	I created the KB in a way that allows for easy conversion between different formats. For example it can translate an English KB into a propositional KB incredibly easily.
	It is flexible enough that you can have incredibly large symbols, and as many of them as you'd like. 

	It cannot deal with negation or several righthand symbols however, which did not appear to be a required feature.
Test cases:
	English:
	TELL
	if raining and outdoors then wet; if wet and outdoors then cold; if cold and tired then sick; outdoors; raining; tired;
	ASK
	sick

	Propositional:
	TELL
	p2=>p3; p3 => p1; c => e; b&e => f; g&f => h; p1=>d; p1&p3 => c; a; b; p2;
	ASK
	d
