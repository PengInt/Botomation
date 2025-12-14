#================================   LEXER   ================================#
#================================           ================================#

CASESPECIFIC = False

comment = {'start': '~ ', 'end': ' ;'}

constants = ['SCRIPT', '']

complexTokens = {
	'%': ['WITH', 'DEFINE', 'GET'],
	'#&': ['INT', 'FLOAT', 'BOOL', 'LIST', 'OBJECT', 'CLASS', 'ATTRIBUTE', 'METHOD', 'MULTIPLE', 'EXPORT', 'FUNCTION', '{ObjectClassName}']
}


#================================   PARSER  ================================#
#================================           ================================#

