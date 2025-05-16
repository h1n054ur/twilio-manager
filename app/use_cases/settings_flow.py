from rich.console import Console
from app.interfaces.cli.menus.base_menu import BaseMenu
from app.interfaces.cli.menus.settings.billing_menu import BillingMenu
from app.interfaces.cli.menus.settings.security_menu import SecurityMenu
from app.interfaces.cli.menus.settings.subaccount_menu import SubaccountMenu
from app.interfaces.cli.menus.settings.devtools_menu import DevToolsMenu
from app.interfaces.cli.menus.settings.account_logs_menu import AccountLogsMenu
from app.interfaces.cli.menus.settings.advanced_search_menu import AdvancedSearchMenu
from app.interfaces.cli.menus.settings.config_management_menu import ConfigManagementMenu
from app.interfaces.cli.menus.settings.diagnostics_menu import DiagnosticsMenu

console = Console()

class SettingsFlow(BaseMenu):
    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        self.clear_screen()
        self.render_header("Settings & Admin")
        self.prompt_choice({
            '1': ("Usage & Billing", lambda: BillingMenu(parent=self).show()),
            '2': ("Security & Compliance", lambda: SecurityMenu(parent=self).show()),
            '3': ("Subaccount Management", lambda: SubaccountMenu(parent=self).show()),
            '4': ("Developer Tools", lambda: DevToolsMenu(parent=self).show()),
            '5': ("Account Logs", lambda: AccountLogsMenu(parent=self).show()),
            '6': ("Advanced Search", lambda: AdvancedSearchMenu(parent=self).show()),
            '7': ("Configuration Management", lambda: ConfigManagementMenu(parent=self).show()),
            '8': ("Diagnostics", lambda: DiagnosticsMenu(parent=self).show())
        })