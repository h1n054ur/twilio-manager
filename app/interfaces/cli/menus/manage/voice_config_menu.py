from app.interfaces.cli.menus.base_menu import BaseMenu
from app.services.number_service import NumberService

class VoiceConfigMenu(BaseMenu):
    def __init__(self, parent, number):
        super().__init__(parent)
        self.number = number
        self.service = NumberService()

    def show(self):
        self.clear_screen()
        self.render_header(f"Configure Voice for {self.number.phone_number}")
        options = {
            '1': ("Enter Voice URL", lambda: self._url()),
            '2': ("Choose TwiML App SID", lambda: self._twiml()),
            '3': ("Choose SIP Trunk SID", lambda: self._sip()),
            '0': ("Back", lambda: None)
        }
        choice = self.prompt_choice(options)

    def _url(self):
        url = self.prompt_input("Enter URL")
        self.service.update_number_config(self.number.sid, {'voice_url': url})
        console.input("Press any key to return.")

    def _twiml(self):
        sid = self.prompt_input("Enter TwiML App SID")
        self.service.update_number_config(self.number.sid, {'voice_application_sid': sid})
        console.input("Press any key to return.")

    def _sip(self):
        sid = self.prompt_input("Enter SIP Trunk SID")
        self.service.update_number_config(self.number.sid, {'trunk_sid': sid})
        console.input("Press any key to return.")