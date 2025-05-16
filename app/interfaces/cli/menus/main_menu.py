from app.interfaces.cli.menus.base_menu import BaseMenu
from app.interfaces.cli.menus.purchase.purchase_menu import PurchaseMenu
from app.interfaces.cli.menus.manage.manage_menu import ManageMenu
from app.interfaces.cli.menus.settings.settings_menu import SettingsMenu

class MainMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

    def show(self):
        self.clear_screen()
        self.render_header("Main Menu")
        self.prompt_choice({
            '1': ("📞 Purchase Numbers", lambda: PurchaseMenu(parent=self).show()),
            '2': ("📟 Manage Numbers", lambda: ManageMenu(parent=self).show()),
            '3': ("🧾 Settings & Admin", lambda: SettingsMenu(parent=self).show()),
            'q': ("Quit", lambda: exit(0))
        })