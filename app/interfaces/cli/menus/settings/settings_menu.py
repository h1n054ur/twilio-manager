from app.interfaces.cli.menus.base_menu import BaseMenu
from app.use_cases.settings_flow import SettingsFlow

class SettingsMenu(BaseMenu):
    def show(self):
        SettingsFlow(parent=self).run()