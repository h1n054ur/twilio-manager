from app.interfaces.cli.menus.base_menu import BaseMenu
from app.services.number_service import NumberService

class PurchaseConfirmMenu(BaseMenu):
    def __init__(self, parent, selections):
        super().__init__(parent)
        self.selections = selections
        self.service = NumberService()

    def show(self):
        while True:
            self.clear_screen()
            self.render_header("Purchase Confirmation")
            
            # Show selected numbers in a table
            from rich.table import Table
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Number")
            table.add_column("City")
            table.add_column("State")
            table.add_column("Type")
            table.add_column("Price")
            
            total_price = 0
            for num in self.selections:
                price = float(getattr(num, 'price', 0))
                total_price += price
                table.add_row(
                    getattr(num, 'phone_number', ''),
                    getattr(num, 'city', ''),
                    getattr(num, 'state', ''),
                    getattr(num, 'type', ''),
                    f"${price:.2f}"
                )
            
            console.print(table)
            console.print(f"\nTotal numbers: {len(self.selections)}")
            console.print(f"Total price: ${total_price:.2f}")
            
            # Confirmation options
            console.print("\nOptions:")
            console.print("[1] Confirm purchase")
            console.print("[2] Remove numbers")
            console.print("[0] Cancel")
            
            choice = console.input("\nChoose an option: ")
            
            if choice == '0':
                return
            elif choice == '1':
                # Show progress during purchase
                with Progress() as progress:
                    task = progress.add_task("[cyan]Purchasing numbers...", total=len(self.selections))
                    results = []
                    for num in self.selections:
                        try:
                            success = self.service.purchase_numbers([num.sid])[0]
                            results.append((num, success))
                        except Exception as e:
                            results.append((num, False))
                        progress.update(task, advance=1)
                
                # Show results
                self.clear_screen()
                self.render_header("Purchase Results")
                
                success_table = Table(show_header=True, header_style="bold green")
                failed_table = Table(show_header=True, header_style="bold red")
                for table in [success_table, failed_table]:
                    table.add_column("Number")
                    table.add_column("City")
                    table.add_column("State")
                    table.add_column("Status")
                
                for num, success in results:
                    row = [
                        getattr(num, 'phone_number', ''),
                        getattr(num, 'city', ''),
                        getattr(num, 'state', ''),
                        "[green]Success[/green]" if success else "[red]Failed[/red]"
                    ]
                    if success:
                        success_table.add_row(*row)
                    else:
                        failed_table.add_row(*row)
                
                if any(success for _, success in results):
                    console.print("\nSuccessfully purchased:")
                    console.print(success_table)
                
                if any(not success for _, success in results):
                    console.print("\nFailed to purchase:")
                    console.print(failed_table)
                
                console.input("\nPress any key to continue.")
                return
                
            elif choice == '2':
                # Remove numbers from selection
                indexes = console.input("Enter indexes to remove (comma-separated): ")
                try:
                    to_remove = set()
                    for idx in indexes.split(','):
                        idx = int(idx.strip()) - 1
                        if 0 <= idx < len(self.selections):
                            to_remove.add(idx)
                    
                    self.selections = [num for i, num in enumerate(self.selections) if i not in to_remove]
                    if not self.selections:
                        console.print("[yellow]All numbers removed. Returning to search results.[/yellow]")
                        console.input("Press any key to continue.")
                        return
                except ValueError:
                    console.print("[red]Invalid input. Please enter valid indexes.[/red]")
                    console.input("Press any key to continue.")