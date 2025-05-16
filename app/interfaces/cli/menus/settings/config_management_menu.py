from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.table import Table
from app.services.account_service import AccountService

class ConfigManagementMenu(BaseMenu):
    def show(self):
        while True:
            self.clear_screen()
            self.render_header("Configuration Management")
            options = {
                '1': ("List Templates", lambda: self._list()),
                '2': ("Apply Template to Numbers", lambda: self._apply()),
                '3': ("Remove Template", lambda: self._remove()),
                '4': ("Export Audit", lambda: self._export()),
                '0': ("Back", lambda: None)
            }
            choice = self.prompt_choice(options)
            if choice == '0':
                return

    def _list(self):
        templates = AccountService().list_config_templates()
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("SID")
        table.add_column("Name")
        for tmpl in templates:
            table.add_row(tmpl.sid, tmpl.name)
        console.print(table)
        console.input("Press any key to return.")

    def _apply(self):
        input("Press any key to return.")

    def _remove(self):
        input("Press any key to return.")

    def _export(self):
        input("Press any key to return.")