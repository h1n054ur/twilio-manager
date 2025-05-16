from app.interfaces.cli.menus.base_menu import BaseMenu
from app.services.number_service import NumberService

class ConfigMenu(BaseMenu):
    def __init__(self, parent, number):
        super().__init__(parent)
        self.number = number
        self.service = NumberService()

    def show(self):
        self.clear_screen()
        self.render_header(f"Configure {self.number.phone_number}")
        options = {
            '1': ("Configure Voice", lambda: self._voice()),
            '2': ("Configure Messaging", lambda: self._messaging()),
            '3': ("Set Friendly Name", lambda: self._friendly()),
            '0': ("Back", lambda: None)
        }
        choice = self.prompt_choice(options)

    def _voice(self):
        sid = self.prompt_input("Enter Voice App/SIP Trunk SID")
        self.service.update_number_config(self.number.sid, {'voice_application_sid': sid})
        console.input("Press any key to return.")

    def _messaging(self):
        sid = self.prompt_input("Enter Messaging Service SID")
        self.service.update_number_config(self.number.sid, {'messaging_service_sid': sid})
        console.input("Press any key to return.")

    def _friendly(self):
        name = self.prompt_input("Enter new Friendly Name")
        self.service.update_number_config(self.number.sid, {'friendly_name': name})
        console.input("Press any key to return.")