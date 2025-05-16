from app.interfaces.cli.menus.base_menu import BaseMenu
from app.services.number_service import NumberService

class PurchaseConfirmMenu(BaseMenu):
    def __init__(self, parent, selections):
        super().__init__(parent)
        self.selections = selections
        self.service = NumberService()

    def show(self):
        self.clear_screen()
        count = len(self.selections)
        items = "number" if count == 1 else "numbers"
        confirm = self.prompt_input(f"Proceed to purchase {count} {items}? [y/n]", 
                                    validator=lambda x: x.lower() in ('y','n'))
        if confirm.lower() == 'y':
            results = self.service.purchase_numbers([num.sid for num in self.selections])
            for num, success in zip(self.selections, results):
                status = "[green]✔[/green]" if success else "[red]✖[/red]"
                print(f"{status} {num.phone_number}")
            input("Press any key to continue.")