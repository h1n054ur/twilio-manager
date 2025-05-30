from app.interfaces.cli.base_menu import BaseMenu
from app.core.settings import SettingsFlow

class SettingsMenu(BaseMenu):
    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings or SettingsFlow()

    def show(self):
        while True:
            # Get current settings from core module
            settings = self.settings.get_account_settings()
            
            options = [
                "1. Usage & Billing",
                "2. Security & Compliance",
                "3. Subaccount Management", 
                "4. Developer Tools",
                "5. Account Logs",
                "6. Advanced Search",
                "7. Configuration Management",
                "8. Logs & Diagnostics",
                "0. Back"
            ]
            self.show_panel(
                title="Settings & Admin",
                subtitle="Global and diagnostic tools",
                options=options
            )
            choice = self.prompt()
            if choice == "1":  # Usage & Billing
                # Get billing summary from use case
                billing = self.settings.get_billing_summary()
                options = [
                    "Current Usage:",
                    f"Active Numbers: {billing['active_numbers']}",
                    f"Price per Number: ${billing['price_per_number']:.2f}",
                    f"Monthly Recurring: ${billing['monthly_recurring']:.2f}",
                    "",
                    "Billing Settings:",
                    f"Spend Limit: ${billing['spend_limit']:.2f}",
                    f"Current Usage: ${billing['current_usage']:.2f}",
                    f"Billing Cycle: {billing['billing_cycle']}",
                    f"Next Bill Date: {billing['next_bill_date']}",
                    "",
                    "0. Back"
                ]
                self.show_panel(
                    title="Usage & Billing",
                    subtitle="View usage and cost estimates",
                    options=options
                )
                choice = self.prompt()
                if choice == "0":
                    continue

            elif choice == "2":  # Security & Compliance
                while True:
                    # Get current security settings
                    result = self.settings.get_security_settings()
                    if "error" in result:
                        self.show_panel(
                            title="Error",
                            subtitle="Failed to get security settings",
                            options=[
                                f"Error: {result['error']}",
                                "",
                                "Press any key to continue"
                            ]
                        )
                        self.prompt()
                        break
                        
                    settings = result["settings"]
                    options = [
                        "Current Security Settings:",
                        f"Account Status: {settings['account_status']}",
                        f"Auth Type: {settings['auth_type']}",
                        "",
                        "IP Access Rules:",
                        *[f"- {rule['friendly_name']} ({rule['sid']})" for rule in settings["ip_access_rules"]],
                        "",
                        "Credential Lists:",
                        *[f"- {cred['friendly_name']} ({cred['sid']})" for cred in settings["credential_lists"]],
                        "",
                        "Actions:",
                        "1. Update Security Settings",
                        "2. Manage IP Access Rules",
                        "3. Manage Credential Lists",
                        "4. View Security Logs",
                        "0. Back"
                    ]
                    self.show_panel(
                        title="Security & Compliance",
                        subtitle="Manage security settings",
                        options=options
                    )
                    sec_choice = self.prompt()
                    if sec_choice == "0":
                        break
                        
                    elif sec_choice == "1":  # Update Security Settings
                        # Show current settings and get updates
                        self.show_panel(
                            title="Update Security Settings",
                            subtitle="Enter new values (or press Enter to keep current)",
                            options=[
                                "Current Settings:",
                                f"Account Status: {settings['account_status']}",
                                f"Auth Type: {settings['auth_type']}",
                                "",
                                "Enter new account status (active/suspended/closed):"
                            ]
                        )
                        status = self.prompt()
                        
                        self.show_panel(
                            title="Update Security Settings",
                            subtitle="Enter new values",
                            options=[
                                "Enter new auth type (basic/api_key):"
                            ]
                        )
                        auth_type = self.prompt()
                        
                        # Update settings
                        new_settings = {
                            "status": status if status else settings["account_status"],
                            "auth_type": auth_type if auth_type else settings["auth_type"]
                        }
                        
                        result = self.settings.update_security_settings(new_settings)
                        if result.get("success"):
                            self.show_panel(
                                title="Success",
                                subtitle="Security settings updated",
                                options=["Press any key to continue"]
                            )
                        else:
                            self.show_panel(
                                title="Error",
                                subtitle="Failed to update settings",
                                options=[
                                    f"Error: {result.get('error', 'Unknown error')}",
                                    "",
                                    "Press any key to continue"
                                ]
                            )
                        self.prompt()
                        
                    elif sec_choice == "2":  # Manage IP Access Rules
                        while True:
                            # Show current rules
                            options = [
                                "Current IP Access Rules:",
                                *[f"{i+1}. {rule['friendly_name']} ({rule['sid']})" 
                                  for i, rule in enumerate(settings["ip_access_rules"])],
                                "",
                                "Actions:",
                                "a. Add New Rule",
                                "r. Remove Rule",
                                "0. Back"
                            ]
                            self.show_panel(
                                title="IP Access Rules",
                                subtitle="Manage IP access control",
                                options=options
                            )
                            rule_choice = self.prompt()
                            
                            if rule_choice == "0":
                                break
                            elif rule_choice.lower() == "a":
                                # Add new rule
                                self.show_panel(
                                    title="Add IP Access Rule",
                                    subtitle="Enter rule details",
                                    options=["Enter friendly name:"]
                                )
                                name = self.prompt()
                                
                                result = self.settings.update_security_settings({
                                    "ip_access_rules": [{"friendly_name": name}]
                                })
                                if result.get("success"):
                                    print("\nRule added successfully")
                                else:
                                    print(f"\nError: {result.get('error', 'Unknown error')}")
                                    
                            elif rule_choice.lower() == "r":
                                # Remove rule
                                self.show_panel(
                                    title="Remove IP Access Rule",
                                    subtitle="Enter rule number to remove:",
                                    options=options[:len(settings["ip_access_rules"])+1]
                                )
                                try:
                                    idx = int(self.prompt()) - 1
                                    if 0 <= idx < len(settings["ip_access_rules"]):
                                        rule = settings["ip_access_rules"][idx]
                                        result = self.settings.update_security_settings({
                                            "ip_access_rules": [{"sid": rule["sid"], "delete": True}]
                                        })
                                        if result.get("success"):
                                            print("\nRule removed successfully")
                                        else:
                                            print(f"\nError: {result.get('error', 'Unknown error')}")
                                except ValueError:
                                    print("Invalid selection")
                                    
                    elif sec_choice == "3":  # Manage Credential Lists
                        while True:
                            # Show current credential lists
                            options = [
                                "Current Credential Lists:",
                                *[f"{i+1}. {cred['friendly_name']} ({cred['sid']})" 
                                  for i, cred in enumerate(settings["credential_lists"])],
                                "",
                                "Actions:",
                                "a. Add New List",
                                "r. Remove List",
                                "0. Back"
                            ]
                            self.show_panel(
                                title="Credential Lists",
                                subtitle="Manage SIP credentials",
                                options=options
                            )
                            cred_choice = self.prompt()
                            
                            if cred_choice == "0":
                                break
                            elif cred_choice.lower() == "a":
                                # Add new credential list
                                self.show_panel(
                                    title="Add Credential List",
                                    subtitle="Enter list details",
                                    options=["Enter friendly name:"]
                                )
                                name = self.prompt()
                                
                                result = self.settings.update_security_settings({
                                    "credential_lists": [{"friendly_name": name}]
                                })
                                if result.get("success"):
                                    print("\nCredential list added successfully")
                                else:
                                    print(f"\nError: {result.get('error', 'Unknown error')}")
                                    
                            elif cred_choice.lower() == "r":
                                # Remove credential list
                                self.show_panel(
                                    title="Remove Credential List",
                                    subtitle="Enter list number to remove:",
                                    options=options[:len(settings["credential_lists"])+1]
                                )
                                try:
                                    idx = int(self.prompt()) - 1
                                    if 0 <= idx < len(settings["credential_lists"]):
                                        cred = settings["credential_lists"][idx]
                                        result = self.settings.update_security_settings({
                                            "credential_lists": [{"sid": cred["sid"], "delete": True}]
                                        })
                                        if result.get("success"):
                                            print("\nCredential list removed successfully")
                                        else:
                                            print(f"\nError: {result.get('error', 'Unknown error')}")
                                except ValueError:
                                    print("Invalid selection")
                                    
                    elif sec_choice == "4":  # View Security Logs
                        result = self.settings.get_security_logs()
                        if "error" in result:
                            self.show_panel(
                                title="Error",
                                subtitle="Failed to get security logs",
                                options=[
                                    f"Error: {result['error']}",
                                    "",
                                    "Press any key to continue"
                                ]
                            )
                            self.prompt()
                            continue
                            
                        logs = result["logs"]
                        columns = [
                            {"header": "Timestamp", "key": "timestamp"},
                            {"header": "Alert Text", "key": "alert_text"},
                            {"header": "Error Code", "key": "error_code"},
                            {"header": "Log Level", "key": "log_level"},
                            {"header": "Request Method", "key": "request_method"},
                            {"header": "Request URL", "key": "request_url"}
                        ]
                        
                        current_page = 1
                        while True:
                            self.show_table(
                                data=logs,
                                columns=columns,
                                title="Security Logs",
                                subtitle="View security events",
                                page=current_page,
                                options_text="\nOptions: [j] Save JSON, [c] Save CSV, or '0' to go back"
                            )
                            nav_choice = self.prompt()
                            if nav_choice == "0":
                                break
                            elif nav_choice.lower() == "n" and current_page * 10 < len(logs):
                                current_page += 1
                            elif nav_choice.lower() == "p" and current_page > 1:
                                current_page -= 1
                            elif nav_choice.lower() == "j":
                                # Export logs as JSON
                                log_data = self.settings.export_logs(format='json')
                                print("\nExported logs to JSON format")
                                print(log_data)
                            elif nav_choice.lower() == "c":
                                # Export logs as CSV
                                log_data = self.settings.export_logs(format='csv')
                                print("\nExported logs to CSV format")
                                print(log_data)

            elif choice == "3":  # Subaccount Management
                while True:
                    # Get subaccounts from settings core
                    subaccounts = self.settings.get_subaccounts()
                    
                    options = [
                        "1. List Subaccounts",
                        "2. Create Subaccount",
                        "3. Switch Active Account",
                        "4. Close Subaccount",
                        "0. Back"
                    ]
                    self.show_panel(
                        title="Subaccount Management",
                        subtitle="View, switch, and create subaccounts",
                        options=options
                    )
                    sub_choice = self.prompt()
                    if sub_choice == "0":
                        break
                    elif sub_choice == "1":  # List Subaccounts
                        if not subaccounts:
                            self.show_panel(
                                title="No Subaccounts",
                                subtitle="No subaccounts found",
                                options=["Press any key to continue"]
                            )
                            self.prompt()
                            continue
                            
                        columns = [
                            {"header": "SID", "key": "sid"},
                            {"header": "Friendly Name", "key": "friendly_name"},
                            {"header": "Status", "key": "status"},
                            {"header": "Date Created", "key": "date_created"}
                        ]
                        self.show_table(
                            data=subaccounts,
                            columns=columns,
                            title="Subaccounts",
                            subtitle="Active subaccounts",
                            options_text="\nPress '0' to go back"
                        )
                        self.prompt()
                        
                    elif sub_choice == "2":  # Create Subaccount
                        self.show_panel(
                            title="Create Subaccount",
                            subtitle="Enter details for new subaccount",
                            options=["Enter friendly name:", "0. Back"]
                        )
                        friendly_name = self.prompt()
                        if friendly_name != "0":
                            result = self.settings.create_subaccount(friendly_name)
                            if result.get("success"):
                                self.show_panel(
                                    title="Success",
                                    subtitle="Subaccount created successfully",
                                    options=[
                                        f"SID: {result['sid']}",
                                        f"Auth Token: {result['auth_token']}",
                                        "",
                                        "Press any key to continue"
                                    ]
                                )
                            else:
                                self.show_panel(
                                    title="Error",
                                    subtitle="Failed to create subaccount",
                                    options=[
                                        f"Error: {result.get('error', 'Unknown error')}",
                                        "",
                                        "Press any key to continue"
                                    ]
                                )
                            self.prompt()
                            
                    elif sub_choice == "3":  # Switch Active Account
                        if not subaccounts:
                            self.show_panel(
                                title="No Subaccounts",
                                subtitle="No subaccounts available to switch to",
                                options=["Press any key to continue"]
                            )
                            self.prompt()
                            continue
                            
                        options = ["Select account to switch to:"]
                        for i, account in enumerate(subaccounts, 1):
                            options.append(f"{i}. {account['friendly_name']} ({account['sid']})")
                        options.extend(["", "0. Back"])
                        
                        self.show_panel(
                            title="Switch Account",
                            subtitle="Select account to switch to",
                            options=options
                        )
                        switch_choice = self.prompt()
                        if switch_choice == "0":
                            continue
                            
                        try:
                            idx = int(switch_choice) - 1
                            if 0 <= idx < len(subaccounts):
                                result = self.settings.switch_account(subaccounts[idx]['sid'])
                                if result.get("success"):
                                    self.show_panel(
                                        title="Success",
                                        subtitle="Account switched successfully",
                                        options=[
                                            f"Now using: {subaccounts[idx]['friendly_name']}",
                                            "",
                                            "Press any key to continue"
                                        ]
                                    )
                                else:
                                    self.show_panel(
                                        title="Error",
                                        subtitle="Failed to switch account",
                                        options=[
                                            f"Error: {result.get('error', 'Unknown error')}",
                                            "",
                                            "Press any key to continue"
                                        ]
                                    )
                                self.prompt()
                        except ValueError:
                            print("Invalid selection")
                            
                    elif sub_choice == "4":  # Close Subaccount
                        if not subaccounts:
                            self.show_panel(
                                title="No Subaccounts",
                                subtitle="No subaccounts available to close",
                                options=["Press any key to continue"]
                            )
                            self.prompt()
                            continue
                            
                        options = ["Select account to close:"]
                        for i, account in enumerate(subaccounts, 1):
                            options.append(f"{i}. {account['friendly_name']} ({account['sid']})")
                        options.extend(["", "0. Back"])
                        
                        self.show_panel(
                            title="Close Account",
                            subtitle="Select account to close",
                            options=options
                        )
                        close_choice = self.prompt()
                        if close_choice == "0":
                            continue
                            
                        try:
                            idx = int(close_choice) - 1
                            if 0 <= idx < len(subaccounts):
                                # Confirm closure
                                self.show_panel(
                                    title="Confirm Closure",
                                    subtitle=f"Are you sure you want to close {subaccounts[idx]['friendly_name']}?",
                                    options=[
                                        "This action cannot be undone!",
                                        "",
                                        "1. Yes, close account",
                                        "0. No, cancel"
                                    ]
                                )
                                confirm = self.prompt()
                                if confirm == "1":
                                    result = self.settings.close_subaccount(subaccounts[idx]['sid'])
                                    if result.get("success"):
                                        self.show_panel(
                                            title="Success",
                                            subtitle="Account closed successfully",
                                            options=["Press any key to continue"]
                                        )
                                    else:
                                        self.show_panel(
                                            title="Error",
                                            subtitle="Failed to close account",
                                            options=[
                                                f"Error: {result.get('error', 'Unknown error')}",
                                                "",
                                                "Press any key to continue"
                                            ]
                                        )
                                    self.prompt()
                        except ValueError:
                            print("Invalid selection")

            elif choice == "4":  # Developer Tools
                while True:
                    options = [
                        "1. API Credentials",
                        "2. Webhook Settings",
                        "3. Test Credentials",
                        "4. Sandbox Settings",
                        "5. API Keys",
                        "0. Back"
                    ]
                    self.show_panel(
                        title="Developer Tools",
                        subtitle="API and development settings",
                        options=options
                    )
                    dev_choice = self.prompt()
                    if dev_choice == "0":
                        break
                    elif dev_choice == "1":  # API Credentials
                        # Get current credentials
                        creds = self.settings.get_api_credentials()
                        self.show_panel(
                            title="API Credentials",
                            subtitle="Current API credentials",
                            options=[
                                "Account SID:",
                                creds.get('account_sid', 'Not available'),
                                "",
                                "Auth Token:",
                                creds.get('auth_token', 'Not available'),
                                "",
                                "Press any key to continue"
                            ]
                        )
                        self.prompt()
                        
                    elif dev_choice == "2":  # Webhook Settings
                        while True:
                            # Get current webhook settings
                            webhooks = self.settings.get_webhook_settings()
                            options = [
                                "Current Webhook Settings:",
                                f"Voice URL: {webhooks.get('voice_url', 'Not set')}",
                                f"SMS URL: {webhooks.get('sms_url', 'Not set')}",
                                f"Status URL: {webhooks.get('status_url', 'Not set')}",
                                "",
                                "1. Set Voice Webhook",
                                "2. Set SMS Webhook",
                                "3. Set Status Webhook",
                                "0. Back"
                            ]
                            self.show_panel(
                                title="Webhook Settings",
                                subtitle="Configure default webhooks",
                                options=options
                            )
                            webhook_choice = self.prompt()
                            if webhook_choice == "0":
                                break
                            elif webhook_choice in ["1", "2", "3"]:
                                webhook_type = {
                                    "1": "voice",
                                    "2": "sms",
                                    "3": "status"
                                }[webhook_choice]
                                
                                self.show_panel(
                                    title=f"Set {webhook_type.title()} Webhook",
                                    subtitle="Enter webhook URL",
                                    options=["Enter URL:", "0. Back"]
                                )
                                url = self.prompt()
                                if url != "0":
                                    result = self.settings.set_webhook(webhook_type, url)
                                    if result.get("success"):
                                        print(f"\n{webhook_type.title()} webhook updated successfully")
                                    else:
                                        print(f"\nError updating webhook: {result.get('error', 'Unknown error')}")
                                    
                    elif dev_choice == "3":  # Test Credentials
                        # Get test credentials
                        test_creds = self.settings.get_test_credentials()
                        self.show_panel(
                            title="Test Credentials",
                            subtitle="Test account credentials",
                            options=[
                                "Test Account SID:",
                                test_creds.get('test_sid', 'Not available'),
                                "",
                                "Test Auth Token:",
                                test_creds.get('test_token', 'Not available'),
                                "",
                                "Test Numbers:",
                                *[f"- {num}" for num in test_creds.get('test_numbers', [])],
                                "",
                                "Press any key to continue"
                            ]
                        )
                        self.prompt()
                        
                    elif dev_choice == "4":  # Sandbox Settings
                        while True:
                            # Get current sandbox settings
                            sandbox = self.settings.get_sandbox_settings()
                            options = [
                                "Current Sandbox Settings:",
                                f"Environment: {sandbox.get('environment', 'production')}",
                                f"Debug Mode: {'Enabled' if sandbox.get('debug', False) else 'Disabled'}",
                                f"Test Mode: {'Enabled' if sandbox.get('test_mode', False) else 'Disabled'}",
                                "",
                                "1. Toggle Debug Mode",
                                "2. Toggle Test Mode",
                                "3. Switch Environment",
                                "0. Back"
                            ]
                            self.show_panel(
                                title="Sandbox Settings",
                                subtitle="Configure development environment",
                                options=options
                            )
                            sandbox_choice = self.prompt()
                            if sandbox_choice == "0":
                                break
                            elif sandbox_choice in ["1", "2"]:
                                setting = "debug" if sandbox_choice == "1" else "test_mode"
                                current = sandbox.get(setting, False)
                                result = self.settings.update_sandbox_setting(setting, not current)
                                if result.get("success"):
                                    print(f"\n{setting.replace('_', ' ').title()} {'disabled' if current else 'enabled'}")
                                else:
                                    print(f"\nError updating setting: {result.get('error', 'Unknown error')}")
                            elif sandbox_choice == "3":
                                self.show_panel(
                                    title="Switch Environment",
                                    subtitle="Select environment",
                                    options=[
                                        "1. Production",
                                        "2. Staging",
                                        "3. Development",
                                        "0. Cancel"
                                    ]
                                )
                                env_choice = self.prompt()
                                env_map = {
                                    "1": "production",
                                    "2": "staging",
                                    "3": "development"
                                }
                                if env_choice in env_map:
                                    result = self.settings.update_sandbox_setting("environment", env_map[env_choice])
                                    if result.get("success"):
                                        print(f"\nEnvironment switched to {env_map[env_choice]}")
                                    else:
                                        print(f"\nError switching environment: {result.get('error', 'Unknown error')}")
                                        
                    elif dev_choice == "5":  # API Keys
                        while True:
                            # Get current API keys
                            api_keys = self.settings.get_api_keys()
                            options = ["Current API Keys:"]
                            if api_keys:
                                for key in api_keys:
                                    options.extend([
                                        f"SID: {key['sid']}",
                                        f"Name: {key['friendly_name']}",
                                        f"Created: {key['date_created']}",
                                        ""
                                    ])
                            else:
                                options.append("No API keys found")
                                
                            options.extend([
                                "",
                                "1. Create New API Key",
                                "2. Revoke API Key",
                                "0. Back"
                            ])
                            
                            self.show_panel(
                                title="API Keys",
                                subtitle="Manage API keys",
                                options=options
                            )
                            key_choice = self.prompt()
                            if key_choice == "0":
                                break
                            elif key_choice == "1":  # Create API Key
                                self.show_panel(
                                    title="Create API Key",
                                    subtitle="Enter key details",
                                    options=["Enter friendly name:", "0. Back"]
                                )
                                name = self.prompt()
                                if name != "0":
                                    result = self.settings.create_api_key(name)
                                    if result.get("success"):
                                        self.show_panel(
                                            title="API Key Created",
                                            subtitle="Save these credentials",
                                            options=[
                                                "SID:",
                                                result['sid'],
                                                "",
                                                "Secret:",
                                                result['secret'],
                                                "",
                                                "WARNING: The secret will not be shown again",
                                                "",
                                                "Press any key to continue"
                                            ]
                                        )
                                    else:
                                        self.show_panel(
                                            title="Error",
                                            subtitle="Failed to create API key",
                                            options=[
                                                f"Error: {result.get('error', 'Unknown error')}",
                                                "",
                                                "Press any key to continue"
                                            ]
                                        )
                                    self.prompt()
                            elif key_choice == "2" and api_keys:  # Revoke API Key
                                options = ["Select key to revoke:"]
                                for i, key in enumerate(api_keys, 1):
                                    options.append(f"{i}. {key['friendly_name']} ({key['sid']})")
                                options.extend(["", "0. Cancel"])
                                
                                self.show_panel(
                                    title="Revoke API Key",
                                    subtitle="Select key to revoke",
                                    options=options
                                )
                                revoke_choice = self.prompt()
                                if revoke_choice != "0":
                                    try:
                                        idx = int(revoke_choice) - 1
                                        if 0 <= idx < len(api_keys):
                                            # Confirm revocation
                                            self.show_panel(
                                                title="Confirm Revocation",
                                                subtitle=f"Revoke {api_keys[idx]['friendly_name']}?",
                                                options=[
                                                    "This action cannot be undone!",
                                                    "",
                                                    "1. Yes, revoke key",
                                                    "0. No, cancel"
                                                ]
                                            )
                                            confirm = self.prompt()
                                            if confirm == "1":
                                                result = self.settings.revoke_api_key(api_keys[idx]['sid'])
                                                if result.get("success"):
                                                    print("\nAPI key revoked successfully")
                                                else:
                                                    print(f"\nError revoking key: {result.get('error', 'Unknown error')}")
                                    except ValueError:
                                        print("Invalid selection")

            elif choice == "5":  # Account Logs
                while True:
                    options = [
                        "1. System Logs",
                        "2. API Logs",
                        "3. Security Logs",
                        "0. Back"
                    ]
                    self.show_panel(
                        title="Account Logs",
                        subtitle="Select log type to view",
                        options=options
                    )
                    log_choice = self.prompt()
                    if log_choice == "0":
                        break
                        
                    # Get logs based on type
                    if log_choice == "1":  # System Logs
                        result = self.settings.get_system_logs()
                        if "error" in result:
                            self.show_panel(
                                title="Error",
                                subtitle="Failed to get system logs",
                                options=[
                                    f"Error: {result['error']}",
                                    "",
                                    "Press any key to continue"
                                ]
                            )
                            self.prompt()
                            continue
                            
                        logs = result["logs"]
                        columns = [
                            {"header": "Timestamp", "key": "timestamp"},
                            {"header": "Event Type", "key": "event_type"},
                            {"header": "Description", "key": "description"},
                            {"header": "Actor Type", "key": "actor_type"},
                            {"header": "Resource Type", "key": "resource_type"}
                        ]
                    elif log_choice == "2":  # API Logs
                        result = self.settings.get_api_logs()
                        if "error" in result:
                            self.show_panel(
                                title="Error",
                                subtitle="Failed to get API logs",
                                options=[
                                    f"Error: {result['error']}",
                                    "",
                                    "Press any key to continue"
                                ]
                            )
                            self.prompt()
                            continue
                            
                        logs = result["logs"]
                        columns = [
                            {"header": "Timestamp", "key": "timestamp"},
                            {"header": "Category", "key": "category"},
                            {"header": "Count", "key": "count"},
                            {"header": "Price", "key": "price"},
                            {"header": "Usage", "key": "usage"},
                            {"header": "Usage Unit", "key": "usage_unit"}
                        ]
                    elif log_choice == "3":  # Security Logs
                        result = self.settings.get_security_logs()
                        if "error" in result:
                            self.show_panel(
                                title="Error",
                                subtitle="Failed to get security logs",
                                options=[
                                    f"Error: {result['error']}",
                                    "",
                                    "Press any key to continue"
                                ]
                            )
                            self.prompt()
                            continue
                            
                        logs = result["logs"]
                        columns = [
                            {"header": "Timestamp", "key": "timestamp"},
                            {"header": "Alert Text", "key": "alert_text"},
                            {"header": "Error Code", "key": "error_code"},
                            {"header": "Log Level", "key": "log_level"},
                            {"header": "Request Method", "key": "request_method"},
                            {"header": "Request URL", "key": "request_url"}
                        ]
                    else:
                        continue
                    
                    current_page = 1
                    while True:
                        self.show_table(
                            data=logs,
                            columns=columns,
                            title="Account Logs",
                            subtitle="View account activity",
                            page=current_page,
                            options_text="\nOptions: [j] Save JSON, [c] Save CSV, or '0' to go back"
                        )
                        nav_choice = self.prompt()
                        if nav_choice == "0":
                            break
                        elif nav_choice.lower() == "n" and current_page * 10 < len(logs):
                            current_page += 1
                        elif nav_choice.lower() == "p" and current_page > 1:
                            current_page -= 1
                        elif nav_choice.lower() == "j":
                            # Export logs as JSON
                            log_data = self.settings.export_logs(format='json')
                            print("\nExported logs to JSON format")
                            print(log_data)
                        elif nav_choice.lower() == "c":
                            # Export logs as CSV
                            log_data = self.settings.export_logs(format='csv')
                            print("\nExported logs to CSV format")
                            print(log_data)

            elif choice == "6":  # Advanced Search
                # Get country pricing info for search options
                countries = [
                    ('US', self.settings.get_country_pricing('US')),
                    ('CA', self.settings.get_country_pricing('CA')),
                    ('GB', self.settings.get_country_pricing('GB')),
                    ('AU', self.settings.get_country_pricing('AU'))
                ]
                
                options = ["Available Search Options:"]
                for code, pricing in countries:
                    if pricing:
                        options.append(f"\n{pricing['country_name']}:")
                        for type_name, price in pricing['number_types'].items():
                            options.append(f"- {type_name.title()}: ${price:.2f}")
                        options.append(f"- {pricing['regions_count']} regions available")
                options.extend(["", "0. Back"])
                
                self.show_panel(
                    title="Advanced Search",
                    subtitle="Deep number filtering (type, location, price)",
                    options=options
                )
                choice = self.prompt()
                if choice == "0":
                    continue

            elif choice == "7":  # Configuration Management
                while True:
                    options = [
                        "1. Export Configuration",
                        "2. Import Configuration",
                        "0. Back"
                    ]
                    self.show_panel(
                        title="Configuration Management",
                        subtitle="Import/export configuration",
                        options=options
                    )
                    config_choice = self.prompt()
                    if config_choice == "0":
                        break
                        
                    elif config_choice == "1":  # Export Configuration
                        # Choose export format
                        self.show_panel(
                            title="Export Configuration",
                            subtitle="Select export format",
                            options=[
                                "1. JSON",
                                "2. CSV",
                                "0. Back"
                            ]
                        )
                        format_choice = self.prompt()
                        if format_choice == "0":
                            continue
                            
                        format_map = {
                            "1": "json",
                            "2": "csv"
                        }
                        if format_choice in format_map:
                            result = self.settings.export_config(format=format_map[format_choice])
                            if result.get("success"):
                                self.show_panel(
                                    title="Configuration Exported",
                                    subtitle=f"Configuration exported in {format_map[format_choice].upper()} format",
                                    options=[
                                        "Configuration:",
                                        "",
                                        result["config"],
                                        "",
                                        "Press any key to continue"
                                    ]
                                )
                            else:
                                self.show_panel(
                                    title="Error",
                                    subtitle="Failed to export configuration",
                                    options=[
                                        f"Error: {result.get('error', 'Unknown error')}",
                                        "",
                                        "Press any key to continue"
                                    ]
                                )
                            self.prompt()
                            
                    elif config_choice == "2":  # Import Configuration
                        # Choose import format
                        self.show_panel(
                            title="Import Configuration",
                            subtitle="Select import format",
                            options=[
                                "1. JSON",
                                "2. CSV",
                                "0. Back"
                            ]
                        )
                        format_choice = self.prompt()
                        if format_choice == "0":
                            continue
                            
                        format_map = {
                            "1": "json",
                            "2": "csv"
                        }
                        if format_choice in format_map:
                            self.show_panel(
                                title="Import Configuration",
                                subtitle=f"Paste {format_map[format_choice].upper()} configuration",
                                options=[
                                    "Enter configuration:",
                                    "0. Back"
                                ]
                            )
                            config_data = self.prompt()
                            if config_data == "0":
                                continue
                                
                            result = self.settings.import_config(
                                config_data=config_data,
                                format=format_map[format_choice]
                            )
                            if result.get("success"):
                                self.show_panel(
                                    title="Success",
                                    subtitle="Configuration imported successfully",
                                    options=[
                                        result.get("message", "Import completed"),
                                        "",
                                        "Press any key to continue"
                                    ]
                                )
                            else:
                                self.show_panel(
                                    title="Error",
                                    subtitle="Failed to import configuration",
                                    options=[
                                        f"Error: {result.get('error', 'Unknown error')}",
                                        "",
                                        "Press any key to continue"
                                    ]
                                )
                            self.prompt()

            elif choice == "8":  # Logs & Diagnostics
                # Get activity logs for diagnostics
                logs = self.settings.get_activity_logs()
                
                options = [
                    "Diagnostic Summary:",
                    f"Total Log Entries: {len(logs)}",
                    "",
                    "Actions:",
                    "1. View Detailed Logs",
                    "2. Export Logs (JSON)",
                    "3. Export Logs (CSV)",
                    "0. Back"
                ]
                self.show_panel(
                    title="Logs & Diagnostics",
                    subtitle="View system logs and diagnostics",
                    options=options
                )
                choice = self.prompt()
                if choice == "0":
                    continue
                elif choice == "2":
                    log_data = self.settings.export_logs(format='json')
                    print("\nExported logs to JSON format")
                    print(log_data)
                elif choice == "3":
                    log_data = self.settings.export_logs(format='csv')
                    print("\nExported logs to CSV format")
                    print(log_data)

            elif choice == "0":  # Back
                return