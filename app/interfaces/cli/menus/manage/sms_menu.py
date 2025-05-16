from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.console import Console
from app.services.messaging_service import MessagingService

console = Console()

class SmsMenu(BaseMenu):
    def __init__(self, parent, number):
        super().__init__(parent)
        self.number = number
        self.service = MessagingService()

    def show(self):
        self.clear_screen()
        self.render_header(f"Send SMS from {self.number.phone_number}")
        to = self.prompt_input("Enter destination number")
        body = self.prompt_input("Enter message body")
        result = self.service.send_sms(from_=self.number.phone_number, to=to, body=body)
        console.print(f"[green]SMS sent: {result}[/green]")
        console.input("Press any key to return.")