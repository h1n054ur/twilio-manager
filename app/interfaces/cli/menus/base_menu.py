import os
from rich.console import Console
from rich.panel import Panel

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
        options = {str(i+1): code for i, code in enumerate(COUNTRY_DATA.keys())}
        options['0'] = None
        while True:
            self.clear_screen()
            self.render_header("Select Country")
            for key, code in options.items():
                if code:
                    name = COUNTRY_DATA[code]['name']
                    console.print(f"[{key}] {code} - {name}")
                else:
                    console.print(f"[{key}] Back")
            choice = console.input("Choose country: ")
            if choice in options:
                return options[choice]
            console.print("[red]Invalid choice.[/red]")
            console.input("Press any key to continue.")

    def select_number_type(self, country):
        types = NumberService().list_number_types(country)
        options = {str(i+1): t for i, t in enumerate(types)}
        options['0'] = None
        while True:
            self.clear_screen()
            self.render_header("Select Number Type")
            for key, t in options.items():
                if t:
                    console.print(f"[{key}] {t}")
                else:
                    console.print(f"[{key}] Back")
            choice = console.input("Choose number type: ")
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


    def prompt_list_selection(self, items, title: str):
        """Display a table of items and prompt for selection by index."""
        from rich.table import Table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Index", justify="right")
        table.add_column("Number")
        table.add_column("City")
        table.add_column("State")
        table.add_column("Type")
        table.add_column("Price")
        for idx, num in enumerate(items, start=1):
            table.add_row(
                str(idx),
                getattr(num, 'phone_number', ''),
                getattr(num, 'city', ''),
                getattr(num, 'state', ''),
                getattr(num, 'type', ''),
                str(getattr(num, 'price', ''))
            )
        console.print(table)
        choice = console.input(f"Enter {title} index (or 0 to back): ")
        if choice == '0':
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                return idx
        except ValueError:
            pass
        console.print("[red]Invalid selection.[/red]")
        console.input("Press any key to continue.")
        return self.prompt_list_selection(items, title)
