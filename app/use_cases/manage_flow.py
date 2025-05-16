from app.interfaces.cli.menus.base_menu import BaseMenu
from app.services.number_service import NumberService
from rich.console import Console

console = Console()

class ManageFlow(BaseMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.service = NumberService()

    def run(self):
        numbers = self.service.list_active_numbers()
        if not numbers:
            self.clear_screen()
            console.print("[yellow]No active numbers found.[/yellow]")
            console.input("Press any key to return.")
            return
        idx = self.prompt_list_selection(numbers, "number")
        if idx is None:
            return
        selected = numbers[idx]
        self.run_actions(selected)

    def run_actions(self, number):
        def make_call(): from app.interfaces.cli.menus.manage.call_menu import CallMenu; CallMenu(parent=self, number=number).show()
        def send_sms(): from app.interfaces.cli.menus.manage.sms_menu import SmsMenu; SmsMenu(parent=self, number=number).show()
        def view_logs(): from app.interfaces.cli.menus.manage.logs_menu import LogsMenu; LogsMenu(parent=self, number=number).show()
        def configure(): from app.interfaces.cli.menus.manage.config_menu import ConfigMenu; ConfigMenu(parent=self, number=number).show()
        def release(): from app.interfaces.cli.menus.manage.release_menu import ReleaseMenu; ReleaseMenu(parent=self, number=number).show()

        self.clear_screen()
        self.render_header(f"Manage {number.phone_number}")
        self.prompt_choice({
            '1': ("Make a Call", make_call),
            '2': ("Send SMS", send_sms),
            '3': ("View Logs", view_logs),
            '4': ("Configure Number", configure),
            '5': ("Release Number", release)
        })