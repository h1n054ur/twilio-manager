import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from app.services.number_service import NumberService

console = Console()

class BaseMenu:
    def __init__(self, parent=None):
        self.parent = parent
        self.options = {}

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_header(self, title: str):
        console.print(Panel(f"[bold]{title}[/bold]", expand=True))

    
    def render_options(self, options: dict[str, str]):
        """Display menu options with consistent styling."""
        console = __import__('rich.console').console.Console()
        for key, desc in options.items():
            # Key in magenta, desc in white, highlight placeholder text in yellow
            console.print(f"[magenta][{key}][/][white] {desc}")

    def prompt_choice(self, options: dict[str, callable] or dict[str, tuple]):
        """
        options: either { key: action } or { key: (description, action) }.
        """
        # Separate descriptions and actions
        actions = {}
        descriptions = {}
        for k, v in options.items():
            if isinstance(v, tuple):
                descriptions[k] = v[0]
                actions[k] = v[1]
            else:
                descriptions[k] = ""
                actions[k] = v
        # Auto-inject Back if parent exists
        if self.parent and '0' not in actions:
            descriptions['0'] = "Back"
            actions['0'] = lambda: None
        # Render options
        self.render_options(descriptions)
        # Prompt loop
        while True:
            choice = console.input("Choose an option: ")
            action = actions.get(choice)
            if action:
                return action()
            console.print("[red]Invalid choice, try again.[/red]")

        self.options = options.copy()
        # Auto-inject Back if parent exists
        if self.parent:
            self.options['0'] = lambda: None
        while True:
            choice = console.input("Choose an option: ")
            action = self.options.get(choice)
            if action:
                return action()
            console.print("[red]Invalid choice, try again.[/red]")

    def prompt_input(self, label: str, validator: callable=None):
        while True:
            value = console.input(f"{label}: ")
            if validator:
                try:
                    if validator(value):
                        return value
                except Exception:
                    pass
                console.print("[red]Invalid input, try again.[/red]")
            else:
                return value

    def show(self):
        raise NotImplementedError("Each menu must implement its own show()")

    # Helper methods for PurchaseFlow orchestration
    def select_country(self):
        from app.models.country_data import COUNTRY_DATA
        # Define fixed order for countries
        country_order = ['US', 'CA', 'GB', 'AU']
        options = {str(i+1): code for i, code in enumerate(country_order)}
        options['0'] = None
        
        while True:
            self.clear_screen()
            self.render_header("Select Country")
            
            # Create a table for better presentation
            from rich.table import Table
            table = Table(show_header=True, header_style="bold cyan", box=None)
            table.add_column("Option", justify="right", style="magenta")
            table.add_column("Country", style="green")
            table.add_column("Available Number Types", style="yellow")
            
            for key, code in options.items():
                if code:
                    country_data = COUNTRY_DATA[code]
                    name = country_data['name']
                    number_types = ', '.join(country_data['number_types'].keys())
                    table.add_row(f"[{key}]", name, number_types)
            
            table.add_row("[0]", "Back", "")
            console.print(table)
            
            choice = console.input("\nChoose country: ")
            if choice in options:
                return options[choice]
            console.print("[red]Invalid choice.[/red]")
            console.input("Press any key to continue.")

    def select_number_type(self, country):
        from app.models.country_data import COUNTRY_DATA
        country_data = COUNTRY_DATA[country]
        number_types = country_data['number_types']
        
        # Create ordered list of types
        type_list = ['local', 'mobile', 'tollfree']
        options = {str(i+1): t for i, t in enumerate(type_list) if t in number_types}
        options['0'] = None
        
        while True:
            self.clear_screen()
            self.render_header("Select Number Type")
            
            # Create a table for better presentation
            from rich.table import Table
            table = Table(show_header=True, header_style="bold cyan", box=None)
            table.add_column("Option", justify="right", style="magenta")
            table.add_column("Number Type", style="green")
            table.add_column("Price", style="yellow")
            
            for key, t in options.items():
                if t:
                    price = number_types.get(t, 0)
                    table.add_row(f"[{key}]", t.title(), f"${price:.2f}")
            
            table.add_row("[0]", "Back", "")
            console.print(table)
            
            choice = console.input("\nChoose number type: ")
            if choice in options:
                return options[choice]
            console.print("[red]Invalid choice.[/red]")
            console.input("Press any key to continue.")

    def select_search_mode(self, country):
        while True:
            self.clear_screen()
            self.render_header("Search Mode")
            console.print("[1] By Digits/Area Code")
            console.print("[2] By Locality")
            console.print("[0] Back")
            choice = console.input("Choose search mode: ")
            if choice == '0':
                return None, None, None
            if choice == '1':
                pattern = console.input("Enter digits to search: ")
                return 'digits', pattern, None
            if choice == '2':
                locality = LocalityInputMenu(parent=self, country=country).show()
                if locality:
                    return 'locality', None, locality
            console.print("[red]Invalid choice.[/red]")
            console.input("Press any key to continue.")

    def select_capabilities(self):
        cap_map = {'1': ['voice'], '2': ['sms'], '3': ['voice', 'sms']}
        while True:
            self.clear_screen()
            self.render_header("Select Capabilities")
            console.print("[1] Voice")
            console.print("[2] SMS")
            console.print("[3] Voice & SMS")
            console.print("[0] Back")
            choice = console.input("Choose capabilities: ")
            if choice == '0':
                return None
            if choice in cap_map:
                return cap_map[choice]
            console.print("[red]Invalid choice.[/red]")
            console.input("Press any key to continue.")


    def _save_results_to_file(self, items):
        """Save search results to JSON or CSV file."""
        import json
        import csv
        from datetime import datetime
        
        # Get file format choice
        console.print("\nSave format:")
        console.print("[1] JSON")
        console.print("[2] CSV")
        choice = console.input("Choose format: ")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            if choice == '1':
                # Save as JSON
                data = [{
                    'phone_number': getattr(num, 'phone_number', ''),
                    'city': getattr(num, 'city', ''),
                    'state': getattr(num, 'state', ''),
                    'type': getattr(num, 'type', ''),
                    'price': getattr(num, 'price', '')
                } for num in items]
                
                filename = f"number_search_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                    
            elif choice == '2':
                # Save as CSV
                filename = f"number_search_{timestamp}.csv"
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Phone Number', 'City', 'State', 'Type', 'Price'])
                    for num in items:
                        writer.writerow([
                            getattr(num, 'phone_number', ''),
                            getattr(num, 'city', ''),
                            getattr(num, 'state', ''),
                            getattr(num, 'type', ''),
                            getattr(num, 'price', '')
                        ])
            else:
                console.print("[red]Invalid choice. File not saved.[/red]")
                return
                
            console.print(f"[green]Results saved to {filename}[/green]")
            
        except Exception as e:
            console.print(f"[red]Error saving file: {str(e)}[/red]")
        
        console.input("Press any key to continue.")

    def prompt_list_selection(self, items, title: str, page_size=10):
        """Display a paginated table of items and prompt for selection by index."""
        from rich.table import Table
        current_page = 0
        total_pages = (len(items) + page_size - 1) // page_size

        while True:
            self.clear_screen()
            self.render_header(title)
            
            # Create table
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Index", justify="right")
            table.add_column("Number")
            table.add_column("City")
            table.add_column("State")
            table.add_column("Type")
            table.add_column("Price")
            
            # Calculate page bounds
            start_idx = current_page * page_size
            end_idx = min(start_idx + page_size, len(items))
            
            # Add rows for current page
            for idx, num in enumerate(items[start_idx:end_idx], start=start_idx + 1):
                table.add_row(
                    str(idx),
                    getattr(num, 'phone_number', ''),
                    getattr(num, 'city', ''),
                    getattr(num, 'state', ''),
                    getattr(num, 'type', ''),
                    str(getattr(num, 'price', ''))
                )
            
            console.print(table)
            console.print(f"\nPage {current_page + 1} of {total_pages}")
            console.print("\nOptions:")
            console.print("[n] Next page  [p] Previous page  [s] Save to file")
            console.print("[x] Select number(s)  [0] Back")
            
            choice = console.input("Enter choice: ").lower()
            
            if choice == '0':
                return None
            elif choice == 'n' and current_page < total_pages - 1:
                current_page += 1
            elif choice == 'p' and current_page > 0:
                current_page -= 1
            elif choice == 's':
                self._save_results_to_file(items)
            elif choice == 'x':
                # Select one or more numbers
                indices = console.input("Enter number index(es) separated by comma: ")
                try:
                    selected = []
                    for idx in indices.split(','):
                        idx = int(idx.strip()) - 1
                        if 0 <= idx < len(items):
                            selected.append(idx)
                    if selected:
                        return selected
                except ValueError:
                    pass
                console.print("[red]Invalid selection.[/red]")
                console.input("Press any key to continue.")
            else:
                console.print("[red]Invalid choice.[/red]")
                console.input("Press any key to continue.")
