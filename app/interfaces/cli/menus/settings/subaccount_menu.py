from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.console import Console
from rich.table import Table
from app.services.account_service import AccountService

console = Console()

class SubaccountMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = AccountService()

    def show(self):
        while True:
            self.clear_screen()
            self.render_header("Subaccount Management")
            subaccounts = self.service.list_subaccounts()
            table = Table(show_header=True, header_style="bold green")
            table.add_column("Index", justify="right")
            table.add_column("SID")
            table.add_column("Friendly Name")
            for idx, sa in enumerate(subaccounts, start=1):
                table.add_row(str(idx), sa.sid, sa.friendly_name)
            console.print(table)
            options = {'c': ("Create new subaccount", lambda: self._create()), '0': ("Back", lambda: None)}
            for i in range(1, len(subaccounts)+1):
                sid = subaccounts[i-1].sid
                options[str(i)] = (f"Switch to {sid}", lambda sid=sid: self.service.switch_subaccount(sid))
            choice = self.prompt_choice(options)
            if choice == 'c':
                name = self.prompt_input("Enter friendly name for new subaccount")
                new = self.service.create_subaccount(name)
                print(f"Created subaccount {new.sid}")
                console.input("Press any key to return.")
            else:
                console.input("Press any key to return.")