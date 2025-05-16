from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.console import Console
from app.services.voice_service import VoiceService

console = Console()

class CallMenu(BaseMenu):
    def __init__(self, parent, number):
        super().__init__(parent)
        self.number = number
        self.service = VoiceService()

    def show(self):
        self.clear_screen()
        self.render_header(f"Make a Call from {self.number.phone_number}")
        to = self.prompt_input("Enter destination number")
        result = self.service.make_call(from_=self.number.phone_number, to=to)
        console.print(f"[green]Call initiated: {result}[/green]")
        console.input("Press any key to return.")