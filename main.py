#!/usr/bin/env python3
import os
from app.gateways.logging_setup import setup_logging
from app.gateways.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from app.interfaces.cli.menus.main_menu import MainMenu

def main():
    setup_logging()
    MainMenu(parent=None).show()

if __name__ == '__main__':
    main()