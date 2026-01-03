import os
# Network name
NETWORK_NAME = "sfo"

# Absolute path of THIS file (child)
APP_DIR = os.path.dirname(os.path.abspath(__file__))



# Absolute paths (safe)
DATA_PATH = os.path.join(
    APP_DIR, "Data", "GTFS", NETWORK_NAME
)

OUTPUT_PATH = os.path.join(
    APP_DIR, "output", NETWORK_NAME
)