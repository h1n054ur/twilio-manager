from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.console import Console
from rich.table import Table
from app.services.account_service import AccountService

console = Console()

class BillingMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = AccountService()

    def show(self):
        self.clear_screen()
        self.render_header("Usage & Billing")
        usage = self.service.get_usage()
        billing = self.service.get_billing()

        table = Table(show_header=False, box=None)
        for key, value in usage.__dict__.items():
            table.add_row(key.replace('_', ' ').title(), str(value))
        console.print(table)
        console.print()
        table2 = Table(show_header=False, box=None)
        for key, value in billing.__dict__.items():
            table2.add_row(key.replace('_', ' ').title(), str(value))
        console.print(table2)
        console.input("Press any key to return.")