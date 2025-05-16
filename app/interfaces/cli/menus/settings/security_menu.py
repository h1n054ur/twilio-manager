from app.interfaces.cli.menus.base_menu import BaseMenu
from app.services.account_service import AccountService

class SecurityMenu(BaseMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = AccountService()

    def show(self):
        while True:
            self.clear_screen()
            self.render_header("Security & Compliance")
            options = {
                '1': ("List API Keys", lambda: self._list_keys()),
                '2': ("Create API Key", lambda: self._create_key()),
                '3': ("Delete API Key", lambda: self._delete_key()),
                '4': ("Manage IP ACLs", lambda: self._ip_acls()),
                '0': ("Back", lambda: None)
            }
            choice = self.prompt_choice(options)
            if choice == '0':
                return

    def _list_keys(self):
        keys = self.service.list_api_keys()
        for k in keys:
            print(k)
        console.input("Press any key to return.")

    def _create_key(self):
        name = self.prompt_input("Enter key friendly name")
        key = self.service.create_api_key(name)
        print(f"Created API Key SID {getattr(key, 'sid', '')}")
        console.input("Press any key to return.")

    def _delete_key(self):
        sid = self.prompt_input("Enter API Key SID to delete")
        self.service.delete_api_key(sid)
        console.input("Press any key to return.")

    def _ip_acls(self):
        while True:
            self.clear_screen()
            self.render_header("IP ACL Management")
            options = {
                '1': ("List IP ACLs", lambda: self._list_acls()),
                '2': ("Add IP ACL", lambda: self._add_acl()),
                '3': ("Remove IP ACL", lambda: self._remove_acl()),
                '0': ("Back", lambda: None)
            }
            choice = self.prompt_choice(options)
            if choice == '0':
                return

    def _list_acls(self):
        acls = self.service.list_ip_acls()
        for ip in acls:
            print(ip)
        console.input("Press any key to return.")

    def _add_acl(self):
        ip = self.prompt_input("Enter IP to whitelist")
        self.service.add_ip_acl(ip)
        console.input("Press any key to return.")

    def _remove_acl(self):
        ip = self.prompt_input("Enter IP to remove")
        self.service.remove_ip_acl(ip)
        console.input("Press any key to return.")