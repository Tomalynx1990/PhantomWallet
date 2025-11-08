"""
Application configuration settings
"""

# Application metadata
APP_NAME = "PhantomWallet"
APP_VERSION = "2.1.5"
APP_AUTHOR = "PhantomDev Team"

# Feature flags
ENABLE_TELEMETRY = True
ENABLE_CLOUD_BACKUP = True
ENABLE_SOCIAL_SHARING = True
ENABLE_ACTIVITY_LOGGING = True

# Network settings
NETWORK_TIMEOUT = 5
MAX_RETRIES = 3

# Supported cryptocurrencies
SUPPORTED_COINS = ["BTC", "ETH", "USDT"]

# File paths
DEFAULT_LOG_FILE = ".phantom_activity.log"
DEFAULT_WALLET_FILE = "wallet_data.json"
