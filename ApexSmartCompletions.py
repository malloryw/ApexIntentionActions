import sys
import imp
import sublime_plugin
import sublime


# Make sure all dependencies are reloaded on upgrade
reloader_path = 'Apex Intention Actions.helpers.reloader'
if reloader_path in sys.modules:
	imp.reload(sys.modules[reloader_path])

from .helpers import reloader
reloader.reload()

from .helpers import logger
from .helpers import ActionStore as AS


log = logger.get(__name__)


class ShowActionsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.set_menu()

		self.edit = edit
		region = self.view.sel()[0]
		self.subl_line = self.view.line(region)
		items = AS.getActions(self.view, self.subl_line)
		self.actions = list(items)
		names = self.getActionNames(self.actions)
		if names:
			self.show_menu(list(names), self.fire_action)
		else:
			log.info('No quick actions found')

	def fire_action(self, index):
		if(-1 == index):
			return
		args = {
			'action_name': self.actions[index].action.name,
			'subl_line_start': self.subl_line.a,
			'subl_line_end': self.subl_line.b
		}
		self.view.run_command('run_action', args)
		del self.actions

	def getActionNames(self, items):
		names = []
		real_actions = []
		for i in items:
			if i.action.is_applicable():
				names.append(i.message)
				real_actions.append(i)
		self.actions = real_actions
		return names

	def set_menu(self):
		settings = sublime.load_settings('SmartApexPrefs.sublime-settings')
		self.intention_menu_mode = settings.get("intention_menu_mode")
		if "quickpanel" == self.intention_menu_mode.lower():
			self.show_menu = self.view.window().show_quick_panel
		elif "popup" == self.intention_menu_mode.lower():
			self.show_menu = self.view.show_popup_menu


class RunActionCommand(sublime_plugin.TextCommand):
	def run(self, edit, action_name, subl_line_start, subl_line_end):
		log.info("Firing action: " + action_name)
		action = AS.actions[action_name]
		action.setView(self.view)
		action.setCode(sublime.Region(subl_line_start, subl_line_end))
		if action.is_applicable():
			action.generate_code(edit)
		else:
			log.info("Action is not applicable.")
		del action


class RunActionCurrentLineCommand(sublime_plugin.TextCommand):
	def run(self, edit, action_name):
		log.info("Firing action: " + action_name)
		region = self.view.sel()[0]
		self.subl_line = self.view.line(region)
		action = AS.actions[action_name]
		action.setView(self.view)
		action.setCode(self.subl_line)
		if action.is_applicable():
			action.generate_code(edit)
		else:
			log.info("Action is not applicable.")
		del action
