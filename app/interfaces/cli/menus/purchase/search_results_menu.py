from app.interfaces.cli.menus.base_menu import BaseMenu
from rich.table import Table
from app.interfaces.cli.menus.purchase.purchase_confirm_menu import PurchaseConfirmMenu

class SearchResultsMenu(BaseMenu):
    def __init__(self, parent, results, page_size=10):
        super().__init__(parent)
        self.results = results
        self.page_size = page_size
        self.page = 0

    def show(self):
        total = len(self.results)
        while True:
            self.clear_screen()
            self.render_header("Search Results")
            start = self.page * self.page_size
            end = start + self.page_size
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Index", justify="right")
            table.add_column("Number")
            table.add_column("City")
            table.add_column("State")
            table.add_column("Type")
            table.add_column("Price")
            for idx, num in enumerate(self.results[start:end], start=start+1):
                table.add_row(
                    str(idx),
                    getattr(num, 'phone_number', ''),
                    getattr(num, 'city', ''),
                    getattr(num, 'state', ''),
                    getattr(num, 'type', ''),
                    str(getattr(num, 'price', ''))
                )
            console.print(table)

            options = {}
            if end < total:
                options['n'] = ("Next page", lambda: setattr(self, 'page', self.page+1))
            if self.page > 0:
                options['p'] = ("Previous page", lambda: setattr(self, 'page', self.page-1))
            options['s'] = ("Sort", lambda: None)
            options['j'] = ("Save JSON", lambda: None)
            options['c'] = ("Save CSV", lambda: None)
            options['x'] = ("Select numbers to purchase", lambda: PurchaseConfirmMenu(parent=self.parent, selections=[self.results[int(i)-1] for i in console.input("Enter indexes: ").split(',')]).show())
            options['0'] = ("Back", lambda: None)

            choice = self.prompt_choice(options)
            if choice == '0':
                return