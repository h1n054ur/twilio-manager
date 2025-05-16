from app.interfaces.cli.menus.base_menu import BaseMenu
from app.services.number_service import NumberService

class MessagingConfigMenu(BaseMenu):
    def __init__(self, parent, number):
        super().__init__(parent)
        self.number = number
        self.service = NumberService()

    def show(self):
        self.clear_screen()
        self.render_header(f"Configure Messaging for {self.number.phone_number}")
        options = {
            '1': ("Enter Messaging URL", lambda: self._url()),
            '2': ("Choose Messaging Service SID", lambda: self._sid()),
            '0': ("Back", lambda: None)
        }
        choice = self.prompt_choice(options)

    def _url(self):
        url = self.prompt_input("Enter URL")
        self.service.update_number_config(self.number.sid, {'messaging_url': url})
        console.input("Press any key to return.")

    def _sid(self):
        sid = self.prompt_input("Enter Messaging Service SID")
        self.service.update_number_config(self.number.sid, {'messaging_service_sid': sid})
        console.input("Press any key to return.")