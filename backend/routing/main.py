import build_transfer_file
from GTFS_wrapper import gtfs2db
from build_transfer_file import build_transfer
from RAPTOR.std_raptor import raptor
def main():
  NETWORK_NAME = "sfo"
  READ_PATH = f'./Data/GTFS/{NETWORK_NAME}/gtfs_o'
  SAVE_PATH = f'./Data/GTFS/{NETWORK_NAME}/'
  #gtfs2db(NETWORK_NAME, 20250830)
  build_transfer(NETWORK_NAME)
  raptor()
main()