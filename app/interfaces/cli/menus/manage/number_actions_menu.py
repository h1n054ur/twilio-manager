from app.interfaces.cli.menus.base_menu import BaseMenu
from app.interfaces.cli.menus.manage.call_menu import CallMenu
from app.interfaces.cli.menus/manage.sms_menu import SmsMenu
from app.interfaces.cli.menus/manage.logs_menu import LogsMenu
from app.interfaces.cli.menus/manage.config_menu import ConfigMenu
from app.interfaces.cli.menus/manage/release_menu import ReleaseMenu

class NumberActionsMenu(BaseMenu):
    def __init__(self, parent, number):
        super().__init__(parent)
        self.number = number

    def show(self):
        while True:
            self.clear_screen()
            self.render_header(f"Actions for {self.number.phone_number}")
            options = {
                '1': ("Make a Call", lambda: CallMenu(parent=self, number=self.number).show()),
                '2': ("Send SMS", lambda: SmsMenu(parent=self, number=self.number).show()),
                '3': ("View Logs", lambda: LogsMenu(parent=self, number=self.number).show()),
                '4': ("Configure Number", lambda: ConfigMenu(parent=self, number=self.number).show()),
                '5': ("Release Number", lambda: ReleaseMenu(parent=self, number=self.number).show()),
                '0': ("Back", lambda: None)
            }
            choice = self.prompt_choice(options)
            if choice == '0':
                return