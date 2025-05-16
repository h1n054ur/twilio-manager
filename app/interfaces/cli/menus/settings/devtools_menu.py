from app.interfaces.cli.menus.base_menu import BaseMenu
from app.services.account_service import AccountService

class DevToolsMenu(BaseMenu):
    def show(self):
        while True:
            self.clear_screen()
            self.render_header("Developer Tools")
            options = {
                '1': ("List Webhooks", lambda: self._list_hooks()),
                '2': ("Toggle Sandbox Mode", lambda: self._toggle()),
                '3': ("Generate Test Credentials", lambda: self._generate()),
                '0': ("Back", lambda: None)
            }
            choice = self.prompt_choice(options)
            if choice == '0':
                return

    def _list_hooks(self):
        hooks = AccountService().list_webhooks()
        for h in hooks:
            print(h)
        console.input("Press any key to return.")

    def _toggle(self):
        status = AccountService().toggle_sandbox()
        print(f"Sandbox mode {'enabled' if status else 'disabled'}")
        console.input("Press any key to return.")

    def _generate(self):
        creds = AccountService().generate_test_credentials()
        print(creds)
        console.input("Press any key to return.")