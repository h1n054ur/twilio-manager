from app.interfaces.cli.menus.base_menu import BaseMenu
from app.interfaces.cli.menus.purchase.locality_input_menu import LocalityInputMenu
from app.interfaces.cli.menus.purchase.search_progress_menu import SearchProgressMenu
from app.services.number_service import NumberService
from app.models.country_data import COUNTRY_DATA

class PurchaseFlow:
    def __init__(self, parent: BaseMenu):
        self.parent = parent
        self.menu = parent
        self.service = NumberService()
        self.country = None
        self.number_type = None
        self.search_mode = None
        self.pattern = None
        self.locality = None
        self.capabilities = []

    def run(self):
        # 1. Select Country
        self.country = self.menu.select_country()
        if not self.country:
            return

        # 2. Select Number Type
        self.number_type = self.menu.select_number_type(self.country)
        if not self.number_type:
            return

        # 3. Search Mode
        self.search_mode, self.pattern, self.locality = self.menu.select_search_mode(self.country)
        if not self.search_mode:
            return

        # 4. Capabilities
        self.capabilities = self.menu.select_capabilities()
        if not self.capabilities:
            return

        # 5. Execute Search & Progress
        SearchProgressMenu(
            parent=self.parent,
            country=self.country,
            number_type=self.number_type,
            search_mode=self.search_mode,
            pattern=self.pattern,
            locality=self.locality,
            capabilities=self.capabilities
        ).show()