import json
from termcolor import colored as c



#  Name:                   DotBot interpreter
#  Author:                 Troy Gomme
#  Username:               Penguin Interactive  (@PenguinInteractive/@PengInt)
#  Description:            Interpreter for the custom coding language I'm developing: DotBot!
#  Start Date:             December
#  Version:                0.0.1
#  Version Date:           18.12.2025



#================================   LEXER   ================================#
#================================           ================================#

class Token:
	tokens = []
	utokens = []
	colourcoding = {
		'Type': (204, 255, 204),
		'Operator': (255, 255, 255),
		'Variable': (255, 255, 255),
		'Boolean': (153, 102, 255),
		'New Line': (0, 0, 0),
		'Define': (153, 204, 255),
		'Indent': (0, 0, 0),
		'If Statement': (255, 153, 204),
		'While Statement': (153, 204, 255),
		'For Statement': (102, 153, 255),
		'Punctuation': (255, 255, 255),
		'Function': (255, 204, 102),
		'Attribute': (255, 204, 102),
		'Method': (255, 204, 51),
		'Bracket': (204, 204, 255),
		'String': (255, 204, 153),
		'Integer': (102, 255, 153),
		'Float': (102, 255, 153),
		'Global Object': (255, 102, 102),
		'Comment': (102, 102, 102),
		'File Extension': (255, 0, 0),
		'Module': (0, 204, 204)
	}
	def __init__(this, contents: dict, type, supered=False):
		if 'start' in contents:
			this.start = contents['start']
		else:
			this.start = ''
		if 'middle' in contents:
			this.middle = contents['middle']
		else:
			this.middle = '{Anything}'
		if 'end' in contents:
			this.end = contents['end']
		else:
			this.end = ''
		this.type = type
		if this.start == '' and this.middle in ['{Anything}', ''] and this.end == '' and this.type != 'New Line' and this.type != 'Indent':
			#print(c('Empty Token creation attempt!', (255, 102, 102)))
			del this
		else:
			print(f' ->  {c('New Token:', (102, 153, 255))}        {c(str(this.type), (102, 255, 102))}{' '*(18-len(str(this.type)))}{c(f'{this.start}{this.middle}{this.end}', Token.colourcoding[this.type])}')
			if not supered:
				Token.tokens.append(this)
			for token in Token.utokens:
				if token.start == this.start and token.middle == this.middle and token.end == this.end and token.type == this.type:
					#print('token overlap')
					return
			if not supered:
				Token.utokens.append(this)
	def sType(this, type):
		this.type = type
		print(f' ->  {c('Updated Token:', (153, 102, 255))}    {c(str(this.type), (102, 255, 102))}{' '*(18-len(str(this.type)))}{c(f'{this.start}{this.middle}{this.end}', Token.colourcoding[this.type])}')
	def print(this):
		print(f' ->  {c('Token:', (102, 153, 255))}            {c(str(this.type), (102, 255, 102))}{' '*(18-len(str(this.type)))}{c(f'{this.start}{this.middle}{this.end}', Token.colourcoding[this.type])}')
	def printToken(this):
		if this.type == 'New Line':
			print('\n', end='')
			return
		if this.type == 'Indent':
			print('    ', end='')
			return
		print(c(f'{this.start}{this.middle}{this.end}', Token.colourcoding[this.type]), end=' ')
		


def isfloat(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def toJson(item):
	return json.dumps(item, default=lambda o: o.__dict__, indent=4)

def fromJson(string):
	loads = json.loads(string)
	return Token({'start': loads['start'], 'middle': loads['middle'], 'end': loads['end']}, loads['type'])


file = open('testDotBotScript.bot', 'r')
#file = open('BOTUTILS.bot', 'r')
script = file.read()
file.close()
#script = 'SCRIPT.SetAttribute(\'case-sensitive\', FALSE)\n%DEFINE #INT &FLOAT &LIST variable = [2, 44.3, 0.000001]'
#print(script, '\n')
print('\033c', end='')
print('|========================|  FINDING  TOKENS  |========================|\n')
class SCRIPT:
	caseSensitive = True
	variables = {}
	@classmethod
	def var(cls, t: str, n: str, v):
		cls.variables[n] = [t, v]

def lex():
	i = 0
	while i < len(script):
		if script[i] in ' \t':
			if script[i] == '\t':
				Token({'start': '', 'middle': '', 'end': ''}, 'Indent')
			i += 1
			continue
		elif script[i] == '~':
			j = i
			while script[i] != ';':
				i += 1
			i += 1
			Token({'start': '', 'middle': script[j:i], 'end': ''}, 'Comment')
		start = ''
		middle = ''
		end = ''
		if script[i] == '\n':
			type = 'New Line'
		elif script[i] in '@#&%':
			start = script[i]
			i += 1
			j = i
			while script[j+1] not in ' \t\n()[]{}\'"/<>,*&^%$#@!~;:|+-=_`?\\' and j+2 != len(script):
				j += 1
			middle = script[i:j+1]
			type = ''
			if start in '#&':
				type = 'Type'
			elif start == '%':
				if middle == '':
					middle = start
					start = ''
					type = 'Operator'
				else:
					type = 'Define'
			elif start == '@':
				type = 'Module'
			i = j
		elif script[i] in '()[]{}':
			middle = script[i]
			type = 'Bracket'
		elif script[i] in '+-=/*<>':
			if script[i] == '/' and i + 1 != len(script):
				if script[i+1] =='/':
					middle = '//'
					i += 1
				else:
					middle = '/'
			elif script[i] == '-':
				if i+1 != len(script):
					if script[i+1] == '>':
						middle = '->'
						i += 1
					else:
						middle = '-'
				else:
					print(c('\n  [ERROR] - Unexpected Token (Evaluating \'-\')', (255, 51, 51)))
					exit()
			elif script[i] == '=':
				if i+1 != len(script):
					if script[i+1] == '=':
						middle = '=='
						i += 1
					else:
						middle = '='
				else:
					print(c('\n  [ERROR] - Unexpected Token (Evaluating \'=\')', (255, 51, 51)))
					exit()
			elif script[i] in '<>':
				if i+1 != len(script):
					if script[i+1] == '=':
						if i+2 != len(script):
							if script[i+2] == '=' and script[i] == '<':
								start = '<=='
								middle = ''
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# RETURN TO HERE
								end = '==>'
							else:
								middle = script[i:i+1]
						else:
							middle = script[i:i+1]
						i += 1
					else:
						middle = script[i]
				elif script[i] == '<':
					print(c('\n  [ERROR] - Unexpected Token (Evaluating \'<\')', (255, 51, 51)))
					exit()
			else:
				middle = script[i]
			type = 'Operator'
		elif script[i] in '\'"':
			start = script[i]
			type = 'String'
			i += 1
			j = i
			while script[j+1] != start and j+2 != len(script):
				j += 1
			middle = script[i:j+1]
			end = start
			i = j + 1
		elif script[i] in '.,:':
			middle = script[i]
			type = 'Punctuation'
		
		else:
			j = i
			type = 'Variable'
			if j+1 != len(script):
				while script[j+1] not in ' \n()[]{}\'"/<>,*&^%$#@!~;:|+-=_`?\\' and j+2 != len(script):
					if not script[i:j+1].isdecimal():
						if script[j+1] == '.':
							break
					j += 1
			middle = script[i:j+1]
			if middle.isdecimal():
				type = 'Integer'
			elif isfloat(middle):
				type = 'Float'
			i = j
		
		Token({'start': start, 'middle': middle, 'end': end}, type)
		i+=1
	
	print('\033c', end='')
	print('|========================|  UPDATING TOKENS  |========================|\n')
	
	
	
	for i in range(len(Token.tokens)):
		token = Token.tokens[i]
		if token.type == 'Variable':
			if token.middle == 'SCRIPT':
				token.sType('Global Object')
			elif token.middle in ['TRUE', 'FALSE']:
				token.sType('Boolean')
			elif token.middle in ['IF', 'ELSE', 'ELSEIF']:
				token.sType('If Statement')
			elif token.middle == 'FOR':
				token.sType('For Statement')
			elif token.middle == 'WHILE':
				token.sType('While Statement')
			elif token.middle in ['IS', 'NOT', 'IN', 'AND', 'OR', 'XOR']:
				token.sType('Operator')
		elif token.type == 'Punctuation' and token.middle == '.':
			if i+1 != len(Token.tokens):
				if Token.tokens[i+1].type != 'Variable':
					print(c('\n  [ERROR] - Unexpected Token (Evaluating \'.\')', (255, 51, 51)))
					exit()
				Token.tokens[i+1].sType('Attribute')
			else:
				print(c('\n  [ERROR] - Unexpected Token (Evaluating \'.\')', (255, 51, 51)))
				exit()
		elif token.type == 'Variable' or token.type == 'Attribute':
			if i+1 != len(Token.tokens):
				if Token.tokens[i+1].middle == '(':
					if token.type == 'Variable':
						token.sType('Function')
					else:
						token.sType('Method')
			elif token.type == 'Attribute':
				if token.middle in ['json', 'py', 'txt', 'html', 'js', 'css', 'c', 'cpp', 'cs', 'bot', 'java']:
					token.sType('File Extension')
	i = 0
	while i < len(Token.tokens):
		token = Token.tokens[i]
		ptoken = Token.tokens[i-1]
		if token.type == 'New Line' and ptoken.type == 'New Line':
			Token.tokens.pop(i)
			i -= 1
		i += 1
lex()

print('\033c', end='')
print('|========================|  UPDATED  TOKENS  |========================|\n')

for token in Token.tokens:
	token.print()

print('\033c', end='')
print('|========================|  COLOURED SCRIPT  |========================|\n')

for token in Token.tokens:
	token.printToken()

#================================   PARSER  ================================#
#================================           ================================#

class FunctionalToken (Token):
	tokens = []
	colourCoding = {
	   'TYPE': (204, 255, 204),
	   'OPER': (255, 255, 255),
	   'VAR': (255, 255, 255),    # and attributes
	   'BOOL': (153, 102, 255),
	   '\\n': (0, 0, 0),
	   'DEF': (153, 204, 255),
	   'TAB': (0, 0, 0),
	   'IF': (255, 153, 204),
	   'WHILE': (153, 204, 255),
	   'FOR': (102, 153, 255),
	   'PUNC': (255, 255, 255),
	   'FUNC': (255, 204, 102),    # and methods
	   '()': (204, 204, 255),
	   'STR': (255, 204, 153),
	   'INT': (102, 255, 153),
	   'FLOAT': (102, 255, 153),
	   'GL OBJ': (255, 102, 102),
	   '~  ;': (102, 102, 102),
	   'FL EXT': (255, 0, 0),
	   'MDL': (0, 204, 204)
	}
	def __print2(this):
		print(f' ->  {c('Token:', (102, 153, 255))}            {c(str(this.type), (102, 255, 102))}{' '*(18-len(str(this.type)))}{c(f'{this.start}{this.middle}{this.end}', FunctionalToken.colourCoding[this.type])}')
	def __printToken2(this):
		if this.type == '\\n':
			print('\n', end='')
			return
		if this.type == 'TAB':
			print('    ', end='')
			return
		print(c(f'{this.start}{this.middle}{this.end}', FunctionalToken.colourCoding[this.type]), end=' ')
	def __init__(this, contents: str, type: str):
		'''
		Args:
			
			contents: anything.
			
			type: one of the following:
				TYPE,
				
				OPER,
				
				VAR,
				
				BOOL,
				
				\\n,
				
				DEF,
				
				TAB,
				
				IF,
				
				WHILE,
				
				FOR,
				
				PUNC,
				
				FUNC,
				
				(),
				
				STR,
				
				INT,
				
				FLOAT,
				
				GL OBJ,
				
				~  ;,
				
				FL EXT,
				
				MDL.
		'''
		if type == 'TYPE':
			ntype = 'Type'
		elif type == 'OPER':
			ntype = 'Operator'
		elif type == 'VAR':
			ntype = 'Variable'
		elif type == 'BOOL':
			ntype = 'Boolean'
		elif type == '\\n':
			ntype = 'New Line'
		elif type == 'DEF':
			ntype = 'Define'
		elif type == 'TAB':
			ntype = 'Indent'
		elif type == 'IF':
			ntype = 'If Statement'
		elif type == 'WHILE':
			ntype = 'While Statement'
		elif type == 'FOR':
			ntype = 'For Statement'
		elif type == 'PUNC':
			ntype = 'Punctuation'
		elif type == 'FUNC':
			ntype = 'Function'
		elif type == '()':
			ntype = 'Bracket'
		elif type == 'STR':
			ntype = 'String'
		elif type == 'INT':
			ntype = 'Integer'
		elif type == 'FLOAT':
			ntype = 'Float'
		elif type == 'GL OBJ':
			ntype = 'Global Object'
		elif type == '~  ;':
			ntype = 'Comment'
		elif type == 'FL EXT':
			ntype = 'File Extension'
		elif type == 'MDL':
			ntype = 'Module'

		super().__init__({'start': '', 'middle': contents, 'end': ''}, ntype, True)
		this.type = type
		if contents != '' or type != '':
			FunctionalToken.tokens.append(this)
		this.print = this.__print2
		this.printToken = this.__printToken2
		this.special = None


print('\033c', end='')
def parse():
	i = 0
	while i < len(Token.tokens):
		contents = ''
		tp = ''
		token = Token.tokens[i]
		#token.print()
		t = token.type
		if t == 'Comment':
			i += 1
			continue
		j = i
		if i == len(Token.tokens)-1:
			contents = token.start + token.middle + token.end
			tp = token.type
			if tp == 'Type':
				tp = 'TYPE'
			elif tp == 'Operator':
				tp = 'OPER'
			elif tp == 'Variable' or tp == 'Attribute':
				tp = 'VAR'
			elif tp == 'Boolean':
				tp = 'BOOL'
			elif tp == 'New Line':
				tp = '\\n'
			elif tp == 'Define':
				tp = 'DEF'
			elif tp == 'Indent':
				tp = 'TAB'
			elif tp == 'If Statement':
				tp = 'IF'
			elif tp == 'While Statement':
				tp = 'WHILE'
			elif tp == 'For Statement':
				tp = 'FOR'
			elif tp == 'Punctuation':
				tp = 'PUNC'
			elif tp == 'Function' or tp == 'Method':
				tp = 'FUNC'
			elif tp == 'Bracket':
				tp = '()'
			elif tp == 'String':
				tp = 'STR'
			elif tp == 'Integer':
				tp = 'INT'
			elif tp == 'Float':
				tp = 'FLOAT'
			elif tp == 'Global Object':
				tp = 'GL OBJ'
			elif tp == 'Comment':
				tp = '~  ;'
			elif tp == 'File Extension':
				tp = 'FL EXT'
			elif tp == 'Module':
				tp = 'MDL'
		else:
			nT = Token.tokens[j+1]
			if t == 'Variable' and nT.type == 'Punctuation' and nT.middle == '.':
				tp = 'VAR'
				while j+2 != len(Token.tokens) and nT.type in ['Punctuation', 'Attribute', 'Method']:
					if nT.type == 'Punctuation' and nT.middle != '.':
						break
					j += 1
					nT = Token.tokens[j+1]
				section = Token.tokens[i:j+1]
				i = j
				cPath = ''
				for tk in section:
					if tk.type == 'Punctuation':
						cPath += '/'
					elif tk.type in ['Variable', 'Attribute', 'Method']:
						if tk.type == 'Method':
							tp = 'FUNC'
						cPath += tk.middle
				contents = cPath
				if len(cPath) == 0:
					print(c('\n\n   ----------------- \n  | ERROR IN PARSER |\n   ----------------- ', (255, 102, 0)))
					exit()
				if cPath[0] == '/' or cPath[-1] == '/':
					print(c('ERROR: Unexpected punctuation: (Evaluating \'.\')', (255, 0, 0)))
					exit()
			else:
				contents = token.start + token.middle + token.end
				tp = token.type
				if tp == 'Type':
					tp = 'TYPE'
				elif tp == 'Operator':
					tp = 'OPER'
				elif tp == 'Variable' or tp == 'Attribute':
					tp = 'VAR'
				elif tp == 'Boolean':
					tp = 'BOOL'
				elif tp == 'New Line':
					tp = '\\n'
				elif tp == 'Define':
					tp = 'DEF'
				elif tp == 'Indent':
					tp = 'TAB'
				elif tp == 'If Statement':
					tp = 'IF'
				elif tp == 'While Statement':
					tp = 'WHILE'
				elif tp == 'For Statement':
					tp = 'FOR'
				elif tp == 'Punctuation':
					tp = 'PUNC'
				elif tp == 'Function' or tp == 'Method':
					tp = 'FUNC'
				elif tp == 'Bracket':
					tp = '()'
				elif tp == 'String':
					tp = 'STR'
				elif tp == 'Integer':
					tp = 'INT'
				elif tp == 'Float':
					tp = 'FLOAT'
				elif tp == 'Global Object':
					tp = 'GL OBJ'
				elif tp == 'Comment':
					tp = '~  ;'
				elif tp == 'File Extension':
					tp = 'FL EXT'
				elif tp == 'Module':
					tp = 'MDL'
		FunctionalToken(contents, tp)
		if FunctionalToken.tokens[-1].type == '\\n':
			while FunctionalToken.tokens[len(FunctionalToken.tokens)-2].type in ['\\n', 'TAB']:
				FunctionalToken.tokens.pop(len(FunctionalToken.tokens)-2)
		i += 1
parse()

print('\033c', end='')
for token in FunctionalToken.tokens:
	token.printToken()

for i in range(len(FunctionalToken.tokens)-1, -1, -1):
	token = FunctionalToken.tokens[i]
	if token.type == 'TYPE':
		if token.middle[0] == '&':
			if token.special != None:
				try:
					FunctionalToken.tokens[i-1].special = token.middle[1:] + '|' + token.special
					FunctionalToken.tokens.pop(i)
				except IndexError:
					print(c('ERROR: Unexpected character at start of script: (Evaluating \'&\')', (255, 0, 0)))
					exit()
			else:
				try:
					FunctionalToken.tokens[i-1].special = token.middle[1:]
					FunctionalToken.tokens.pop(i)
				except IndexError:
					print(c('ERROR: Unexpected character at start of script: (Evaluating \'&\')', (255, 0, 0)))
					exit()
		elif token.middle[0] == '#':
			if token.special != None:
				token.special = token.middle[1:] + '|' + token.special
				token.middle = '#MULTIPLE'


class Variable:
	variables = {}
	forGeneratedExpression = {}
	def __init__(this, name: str, types: list, value):
		this.name = name
		this.types = types
		this.value = value
		if type(this.value) not in this.types:
			print(c(f'\n  [ERROR] - Variable value not matching type (Evaluating variable {this.name} | Types {this.types} | Value {this.value})', (255, 51, 51)))
			exit()
		if this.name in Variable.variables:
			print(c(f'\n  [ERROR] - Variable with name {this.name} already exists', (255, 51, 51)))
		Variable.variables[this.name] = this
		Variable.forGeneratedExpression[this.name] = this.value
	@classmethod
	def update(cls, var: str, nVal):
		if var not in cls.variables:
			print(c(f'\n  [ERROR] - Variable with name {var} doesn\'t exist', (255, 51, 51)))
		var = cls.variables[var]
		var.value = nVal
		if type(var.value) not in var.types:
			print(c(f'\n  [ERROR] - Variable value not matching type (Evaluating variable {var.name} | Types {var.types} | Value {var.value})', (255, 51, 51)))
			exit()
		




i = -1
def nextToken(setNext=True) -> FunctionalToken:
	global i
	if setNext:
		global FT
		i += 1
		if i == len(FunctionalToken.tokens):
			raise IndexError
		FT = FunctionalToken.tokens[i]
		FT.print()
		return FT
	else:
		if i+1 == len(FunctionalToken.tokens):
			raise IndexError
		FunctionalToken.tokens[i+1].print()
		return FunctionalToken.tokens[i+1]

def evalExpr(genExpr):
	pass

FT = FunctionalToken.tokens[0]
while i < len(FunctionalToken.tokens)-1:
	nextToken()
	
	if FT.type == 'DEF':
		nextToken()
		if FT.type == 'TYPE':
			if FT.middle == '#MULTIPLE':
				nVarType = FT.special.split('|')
			else:
				nVarType = [FT.middle[1:]]
			nextToken()
			if FT.type == 'VAR':
				nVarName = FT.middle
				nextToken()
				if FT.type == 'OPER' and FT.middle == '=':
					nVarVal = None
					generatedExpression = []
					parlvl = 0
					while FT.type != '\\n' and i < len(FunctionalToken.tokens)-1:
						nextToken()
						if FT.type == '\\n':
							break
						appendTo = generatedExpression
						for i in range(parlvl):
							appendTo = appendTo[len(appendTo)]
						if FT.type == '()' and FT.middle == '(':
							appendTo.append([])
							parlvl += 1
							continue
						if FT.type == '()' and FT.middle == ')':
							parlvl -= 1
							continue
						if FT.type == 'INT' or FT.type == 'FLOAT':
							appendTo.append(FT)
							continue
						if FT.type == 'OPER':
							appendTo.append(FT)
							continue
					for i in range(len(generatedExpression)):
						print(generatedExpression[i].type, end=' ')
					print()
				elif FT.type == 'OPER' and FT.middle == '->':
					continue
					print('making class or function probably - ignore this')
				else:
					print(c(f'ERROR: Unexpected token (Evaluating {FT.middle})', (255, 0, 0)))
					exit()
			else:
				print(c(f'ERROR: Unexpected token (Evaluating {FT.middle})', (255, 0, 0)))
				exit()
		else:
			print(c(f'ERROR: Unexpected token (No type specified after %DEFINE statement) (Evaluating {FT.middle}, which is a {FT.type})', (255, 0, 0)))
			exit()