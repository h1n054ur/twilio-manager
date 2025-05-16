from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.console import Console
from rich.table import Table
from app.services.number_service import NumberService

console = Console()

class AdvancedSearchMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = NumberService()

    def show(self):
        self.clear_screen()
        self.render_header("Advanced Search")
        num_type = self.prompt_input("Enter number type (or leave blank)")
        locality = self.prompt_input("Enter city or state (or leave blank)")
        price_min = self.prompt_input("Enter min price (or leave blank)", validator=lambda x: x == '' or x.replace('.', '', 1).isdigit())
        price_max = self.prompt_input("Enter max price (or leave blank)", validator=lambda x: x == '' or x.replace('.', '', 1).isdigit())
        results = self.service.search_advanced(
            number_type=num_type or None,
            locality=locality or None,
            price_min=float(price_min) if price_min else None,
            price_max=float(price_max) if price_max else None
        )
        table = Table(show_header=True, header_style="bold cyan")
        for col in ["phone_number","city","state","type","price"]:
            table.add_column(col.replace('_',' ').title())
        for num in results:
            table.add_row(num.phone_number, num.city, num.state, num.type, str(num.price))
        console.print(table)
        console.input("Press any key to return.")