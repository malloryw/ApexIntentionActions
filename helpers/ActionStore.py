from . import RegexHelper as re
from . import Actions as A
from . import PropertyActions as PA
from . import ClassActions as CA
from . import MethodActions as MA


def __init__():
	pass


class ActionStore():
	def __init__(self, message, action):
		super(ActionStore, self).__init__()
		self.message = message
		self.action = action


actions = {
	A.ADD_GETTER: PA.AddGetterAction(),
	A.ADD_SETTER: PA.AddSetterAction(),
	A.ADD_GETTER_SETTER: PA.AddGetterSetterAction(),
	A.ADD_CONSTRUCTOR_PARAMETER: PA.AddConstructorParameterAction(),

	A.ADD_CONSTRUCTOR: CA.AddConstructorAction(),
	A.ADD_INITIALIZER: CA.AddInitializerAction(),
	A.ADD_CONSTRUCTOR_INITIALIZER: CA.AddConstructorInitializerAction(),

	A.ADD_METHOD_OVERRIDE: MA.AddMethodOverrideChooseArgAction(),
	A.ADD_METHOD_OVERRIDE_CREATE: MA.AddMethodOverrideAction(),
}
prop_actions = [
	ActionStore('Add getter and setter', actions[A.ADD_GETTER_SETTER]),
	ActionStore('Add getter', actions[A.ADD_GETTER]),
	ActionStore('Add setter', actions[A.ADD_SETTER]),
	ActionStore('Add constructor parameter', actions[A.ADD_CONSTRUCTOR_PARAMETER])
]
class_actions = [
	ActionStore('Add constructor', actions[A.ADD_CONSTRUCTOR]),
	ActionStore('Add initializer', actions[A.ADD_INITIALIZER]),
	ActionStore('Add constructor and initializer', actions[A.ADD_CONSTRUCTOR_INITIALIZER]),
]
method_actions = [
	ActionStore('Generate overload', actions[A.ADD_METHOD_OVERRIDE]),
]
actions_map = {
	'prop': prop_actions,
	'class': class_actions,
	'method': method_actions,
}
regex_map = {
	'prop': r'(public|private|global|protected)\s*(static){0,1}\s+\w+\s+(\w+)\s*;',
	'class': r'(public|private|global|protected)\s*(virtual|abstract|with sharing|without sharing){0,1}\s+class\s+(\w+)\s*.*{',
	'method': re.METHOD_DEF_ARGS,
}


def getActions(view, line_reg):
	result = []
	line = view.substr(line_reg)
	for key, regex in regex_map.items():
		if(re.match_stripped(regex, line)):
			result = actions_map[key]
	for store in result:
		store.action.setView(view)
		store.action.setCode(line_reg)
	return result
