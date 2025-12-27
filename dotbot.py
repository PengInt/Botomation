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


file = open('BOTUTILS.bot', 'r')
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
		elif script[i] in ['@', '#', '&', '%']:
			start = script[i]
			i += 1
			j = i
			while script[j+1] not in ' \n()[]{}\'"/<>,*&^%$#@!~;:|+-=_`?\\' and j+2 != len(script):
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
		if this.type == 'New Line':
			print('\n', end='')
			return
		if this.type == 'Indent':
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
		ntype = 'Variable'
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
		if contents != '' and type != '':
			FunctionalToken.tokens.append(this)
		this.print = this.__print2
		this.printToken = this.__printToken2

class Variable:
	variables = {}
	def __init__(this, name: str, types: list, value):
		this.name = name
		this.types = types
		this.value = value
		if type(this.value) not in types:
			print(c(f'\n  [ERROR] - Variable value not matching type (Evaluating variable {this.name} | Types {this.types} | Value {this.value})', (255, 51, 51)))


print()
def parse():
	i = 0
	while i < len(Token.tokens)-1:
		contents = ''
		tp = ''
		token = Token.tokens[i]
		#token.print()
		t = token.type
		if t == 'Comment':
			i += 1
			continue
		j = i
		nT = Token.tokens[j+1]
		if t == 'Variable' and nT.type == 'Punctuation' and nT.middle == '.':
			tp = 'VAR'
			while j+2 != len(Token.tokens) and nT.type in ['Punctuation', 'Attribute', 'Method']:
				if nT.type == 'Punctuation' and nT.middle != '.':
					print('punctuation that isn\'t \'.\'')
					break
				if nT.type == 'Method':
					tp = 'FUNC'
				j += 1
				nT = Token.tokens[j+1]
			section = Token.tokens[i:j+1]
			i = j
			cPath = ''
			for tk in section:
				if tk.type == 'Punctuation':
					cPath += '/'
				elif tk.type in ['Variable', 'Attribute', 'Method']:
					cPath += tk.middle
			contents = cPath
			if len(cPath) == 0:
				print(c('\n\n   ----------------- \n  | ERROR IN PARSER |\n   ----------------- ', (255, 102, 0)))
				exit()
			if cPath[0] == '/' or cPath[-1] == '/':
				print(c('ERROR: Unexpected punctuation: (Evaluating \'.\')', (255, 0, 0)))
				#exit()
		FunctionalToken(contents, tp)
		i += 1
parse()
for token in FunctionalToken.tokens:
	token.printToken()