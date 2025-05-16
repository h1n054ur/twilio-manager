from app.interfaces.cli.menus.base_menu import BaseMenu
from app.use_cases.manage_flow import ManageFlow

class ManageMenu(BaseMenu):
    def show(self):
        ManageFlow(parent=self).run()