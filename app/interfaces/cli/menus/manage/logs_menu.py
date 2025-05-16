from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.table import Table
from app.services.logs_service import LogsService

class LogsMenu(BaseMenu):
    def __init__(self, parent, number):
        super().__init__(parent)
        self.number = number
        self.service = LogsService()

    def show(self):
        while True:
            self.clear_screen()
            self.render_header(f"View Logs for {self.number.phone_number}")
            options = {
                '1': ("Messaging Logs", lambda: self._view('sms')),
                '2': ("Call Logs", lambda: self._view('call')),
                '0': ("Back", lambda: None)
            }
            choice = self.prompt_choice(options)
            if choice == '0':
                return

    def _view(self, log_type):
        logs = self.service.list_logs(log_type, self.number.sid)
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("SID")
        table.add_column("Date")
        table.add_column("Status")
        for log in logs:
            table.add_row(
                getattr(log, 'sid', ''),
                getattr(log, 'date_created', '').isoformat() if getattr(log, 'date_created', None) else '',
                getattr(log, 'status', '')
            )
        console.print(table)
        console.input("Press any key to return.")