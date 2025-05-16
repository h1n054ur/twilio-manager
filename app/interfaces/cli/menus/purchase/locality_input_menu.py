from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.console import Console
from rich.table import Table
from app.models.country_data import COUNTRY_DATA

console = Console()

class LocalityInputMenu(BaseMenu):
    def __init__(self, parent=None, country=None):
        super().__init__(parent)
        self.country = country

    def show(self):
        regions = COUNTRY_DATA.get(self.country, {}).get('regions', {})
        if not regions:
            console.print("[red]No regions found for this country.[/red]")
            self.prompt_choice({'0': ("Back", lambda: None)})
            return None

        items = list(regions.keys())
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Index", justify="right")
        table.add_column("Locality")
        for i, loc in enumerate(items, start=1):
            table.add_row(str(i), loc)
        console.print(table)

        options = {str(i): (loc, (lambda loc=loc: loc)) for i, loc in enumerate(items, start=1)}
        options['0'] = ("Back", lambda: None)
        choice = self.prompt_choice(options)
        return choice