"""
Wallet management core functionality
"""

import os
import time
import hashlib
from datetime import datetime


class CryptoWallet:
    """Main wallet implementation"""

    def __init__(self):
        self.balance = {
            "BTC": 0.0,
            "ETH": 0.0,
            "USDT": 0.0
        }
        self.private_key = None
        self.seed_phrase = None
        self.transactions = []
        self.wallet_id = None

    def create_new_wallet(self):
        """Generate new wallet with keys"""
        print("\n[+] Creating new wallet...")
        print("[+] Generating secure keys...")

        time.sleep(1)

        # Generate private key
        self.private_key = hashlib.sha256(os.urandom(32)).hexdigest()

        # Generate wallet ID
        self.wallet_id = f"PW-{hashlib.md5(self.private_key.encode()).hexdigest()[:12]}"

        # Generate seed phrase
        words = ["abandon", "ability", "able", "about", "above", "absent",
                "absorb", "abstract", "absurd", "abuse", "access", "accident"]
        self.seed_phrase = " ".join(words)

        return {
            "private_key": self.private_key,
            "seed_phrase": self.seed_phrase,
            "wallet_id": self.wallet_id,
            "created_at": datetime.now().isoformat()
        }

    def import_from_key(self, private_key):
        """Import wallet from private key"""
        self.private_key = private_key
        self.wallet_id = f"PW-{hashlib.md5(private_key.encode()).hexdigest()[:12]}"
        return True

    def import_from_seed(self, seed_phrase):
        """Import wallet from seed phrase"""
        self.seed_phrase = seed_phrase
        # Derive private key from seed (simplified)
        self.private_key = hashlib.sha256(seed_phrase.encode()).hexdigest()
        self.wallet_id = f"PW-{hashlib.md5(self.private_key.encode()).hexdigest()[:12]}"
        return True

    def get_balance(self):
        """Get current balance"""
        return self.balance.copy()

    def create_transaction(self, crypto, amount, recipient):
        """Create a new transaction"""
        if crypto not in self.balance:
            return None

        tx = {
            "id": hashlib.sha256(f"{time.time()}{recipient}".encode()).hexdigest(),
            "from": self.wallet_id,
            "to": recipient,
            "crypto": crypto,
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "private_key": self.private_key
        }

        self.transactions.append(tx)
        return tx

    def get_receiving_address(self):
        """Generate receiving address"""
        addr = f"1Phantom{hashlib.md5(str(time.time()).encode()).hexdigest()[:20]}"
        return addr
