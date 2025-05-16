from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.console import Console
from app.services.logs_service import LogsService

console = Console()

class AccountLogsMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = LogsService()

    def show(self):
        self.clear_screen()
        self.render_header("Account Logs")
        logs = self.service.list_logs('all', None)
        for log in logs:
            console.print(log)
        console.input("Press any key to return.")