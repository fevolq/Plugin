import os

# -----------------------------SYSTEM----------------------------------
LOG_PATH = ''
PORT = 8008
LOG_SERVER = os.getenv('LOG_SERVER', '')
CHROME_PATH = os.getenv('CHROME_PATH', None)  # chrome路径
# ---------------------------------------------------------------------

# -------------------------------DB------------------------------------
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PWD = os.getenv('REDIS_PWD', '')
REDIS_DB = {
    '': 0,
}

MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PWD = os.getenv('MYSQL_PWD', 'root')
MYSQL_DB = os.getenv('MYSQL_DB', 'plugin')
# ---------------------------------------------------------------------

try:
    from local_config import *
except:
    pass
