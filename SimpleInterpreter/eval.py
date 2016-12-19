#CIS 424 - Project 2
#Write interpreter for a simple programming language using top-down recursive-descent method and inherited
#attributes with a strong-typed grammar

import sys
import re
realRegex = re.compile("\d*\.\d+")		#Regex to compare against strings from lexemeList to check for real type values
test=-1
lexemeList = []
lookahead=None
current=None
idict={}
rdict={}
f = open(sys.argv[1], 'r')
for line in f:
	for lexeme in line.split():
		lexemeList.append(lexeme)
f.close()

#Function for stating error and exiting program
def myError():
	print("Syntax Error")
	sys.exit(1)
	return

#Function for traversing lexeme list and saving current value and next value
def lex():
	global test
	test+=1
	global current
	current = lexemeList[test]
	global lookahead
	if(test+1==len(lexemeList)):	#Check for end of file to avoid OutOfBound Exception
		lookahead = 'end'
	else:
		lookahead = lexemeList[test+1]
	return

#Main Function of the Interpreter which calls all other functions based on grammar
def prog():
	lex()
	decl_list()
	lex()
	stmt_list()
	return

#Recursive Function that calls necessary functions for the declaring of variables of type int or real
def decl_list():
	decl()
	if(lookahead==';'):
		lex()
		if(lookahead=='int' or lookahead=='real'):	#Check if recursion is needed then do
			lex()
			decl_list()
	else:
		myError()
	return

#Function to determine type and then call function to add variable to proper dictionary
def decl():
	global t
	t=type_1()
	id_list(t)
	return

#Function that sets type for variable
def type_1():
	if (current=='int'):
		return 'int'
  	elif(current=='real'):
		return 'real'
	else:
		myError()

#Function that adds variable to proper dictionary based on return from type_1()
def id_list(type):
	lex()	
	if(type=='int'):
		idict[current] = 0
	elif(type=='real'):
		rdict[current] = 0
	if(lookahead==','):
		lex()
		id_list(type)
	return

#Recursive Function that calls necessary functions to execute the statements iprint, rprint, and any variable assignments
def stmt_list():
	stmt()
	if(lookahead==';'):
		lex()
		if(lookahead=='end'):	#Check for end of file otherwise do recursion
			return
		else:
			lex()
			stmt_list()
	else:
		myError()
	return

#Function that calls necessary functions to evaluate the expressions for the various statements and prints to cmd results of iprint or rprint calls
def stmt():
	var = None	#To save the variable name when doing assignment stmts
	if(current in idict and lookahead=='='):
		var = current
		t='int'
		lex()	#lex here to move past the = and to the expression
		idict[var] = expr(t)
	elif(current in rdict and lookahead=='='):
		var = current
		t='real'
		lex()	#lex here to move past the = and to the expression
		rdict[var] = expr(t)
	elif(current=='iprint'):
		t='int'
		print(str(expr(t)))
	elif(current=='rprint'):
		t='real'
		print(str(expr(t)))
	else:
		myError()
	return

#Function to evaluate additions and subtractions in the expression after multiplication, division, and exponentiation is handled
def expr(t):
	tval = 0
	lex()
	tval = term(t)
	while(lookahead=="+" or lookahead=="-"):
		lex()
		if(current=="+"):
			lex()
			tval = tval + term(t)
		else:
			lex()
			tval = tval - term(t)
	return tval

#Function to evaluate multiplications and divisions in the expression after exponentiation is handled
def term(t):
	fval = 0
	fval = factor(t)
	while(lookahead=="*" or lookahead=="/"):
		lex()
		if(current=="*"):
			lex()
			fval = fval * factor(t)
		else:
			lex()
			fval = fval / factor(t)
	return fval

#Function to evaluate exponentiation after indentifying the base as another expression, a variable, or a number
def factor(t):
	bval = 0
	if(lookahead=="^"):
		bval = base(t)
		lex()
		lex()	#second lex to pass over the ^ and look at the expression after
		bval = bval ** factor(t)	#** is exponential not ^
	else:
		bval = base(t)
	return bval

#Function to identify the base as another expression, a variable, or a number
def base(t):
	val = 0
	if(current=='('):
		val = expr(t)
		if(lookahead==')'):
			lex()
			return val
		else:
			myError()
	elif(current in idict or current in rdict):
		if(t=='int'):		#Check type after identifying as a variable to avoid type mismatch
			if(current in idict):
				return idict[current]
			else:
				myError()
		elif(t=='real'):
			if(current in rdict):
				return rdict[current]
			else:
				myError()
	elif(realRegex.match(current) or current.isdigit()):
		if(t=='int'):		#Check type after identifying as a number to avoid type mismatch
			if('.' in current):
				myError()
			else:
				return int(current)
		elif(t=='real'):
			if('.' in current):
				return float(current)
			else:
				myError()
	else:
		myError()
	return
prog()

