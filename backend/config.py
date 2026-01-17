
import os
from routing.config import DATA_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")
ROUTING_DIR = os.path.join(BASE_DIR, "routing")
ROUTING_DATA_DIR = os.path.join(ROUTING_DIR, DATA_PATH)