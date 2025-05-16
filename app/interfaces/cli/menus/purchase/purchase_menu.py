from app.interfaces.cli.menus.base_menu import BaseMenu
from app.use_cases.purchase_flow import PurchaseFlow

class PurchaseMenu(BaseMenu):
    def show(self):
        PurchaseFlow(parent=self).run()