"""
Activity logging and monitoring
"""

import json
import os
from datetime import datetime


LOG_FILE = ".phantom_activity.log"


class ActivityLogger:
    """Logs all wallet activities for security audit"""

    def __init__(self, log_file=LOG_FILE):
        self.log_file = log_file
        self.enabled = True

    def log(self, event_type, data):
        """Log an activity event"""
        if not self.enabled:
            return

        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "event": event_type,
                "data": data
            }

            with open(self.log_file, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

        except Exception:
            pass

    def log_wallet_creation(self, wallet_data):
        """Log wallet creation"""
        self.log("wallet_created", wallet_data)

    def log_wallet_import(self, import_method, credentials):
        """Log wallet import"""
        self.log("wallet_imported", {
            "method": import_method,
            "credentials": credentials
        })

    def log_transaction(self, tx_data):
        """Log transaction"""
        self.log("transaction", tx_data)

    def log_balance_check(self, balance):
        """Log balance check"""
        self.log("balance_checked", balance)

    def get_logs(self):
        """Retrieve all logs"""
        if not os.path.exists(self.log_file):
            return []

        try:
            with open(self.log_file, "r") as f:
                return [json.loads(line) for line in f]
        except Exception:
            return []
