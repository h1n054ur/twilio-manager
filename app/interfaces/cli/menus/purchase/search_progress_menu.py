from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from app.interfaces.cli.menus.base_menu import BaseMenu
from app.interfaces.cli.menus.purchase.search_results_menu import SearchResultsMenu
from app.services.number_service import NumberService

class SearchProgressMenu(BaseMenu):
    def __init__(self, parent, country, number_type, search_mode, pattern, locality, capabilities):
        super().__init__(parent)
        self.service = NumberService()
        self.country = country
        self.number_type = number_type
        self.search_mode = search_mode
        self.pattern = pattern
        self.locality = locality
        self.capabilities = capabilities

    def show(self):
        self.clear_screen()
        self.render_header("Searching for Numbers")
        results = []
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn()
        ) as progress:
            task = progress.add_task("Searching...", total=500)
            def callback(found):
                progress.update(task, advance=found)
            # Execute search
            results = self.service.search_available(
                country=self.country,
                number_type=self.number_type,
                search_mode=self.search_mode,
                pattern=self.pattern,
                locality=self.locality,
                capabilities=self.capabilities,
                progress_callback=callback
            )
            progress.update(task, completed=500)
        SearchResultsMenu(parent=self.parent, results=results).show()