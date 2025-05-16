from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.console import Console
from app.services.number_service import NumberService

console = Console()

class ReleaseMenu(BaseMenu):
    def __init__(self, parent, number):
        super().__init__(parent)
        self.number = number
        self.service = NumberService()

    def show(self):
        self.clear_screen()
        self.render_header(f"Release {self.number.phone_number}")
        confirm = self.prompt_input("Confirm release? [y/n]", validator=lambda x: x.lower() in ('y','n'))
        if confirm.lower() == 'y':
            self.service.release_number(self.number.sid)
            console.print("[green]Number released[/green]")
        console.input("Press any key to return.")