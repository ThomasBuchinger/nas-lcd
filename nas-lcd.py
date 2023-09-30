import lcddriver as lcd
from time import time, sleep
from datetime import datetime
import sys
import subprocess

def check_raidpool_online():
  zpool_list = subprocess.run(["zpool", "list", "raidpool", "-o", "health"], capture_output=True)
  health = zpool_list[-1].split("\s")[0]
  lcd.display_string("raidpool: "+health, 1)
  return health == "ONLINE"


# Setup screen
#
bus = 0
address = 0x3f
if len(sys.argv) > 1:
    address = int(argv[1], 16)
if len(sys.argv) > 2:
    bus = int(argv[1])
    address = int(argv[2], 16)
lcd = lcd.lcd(bus, address)

### Startup Checks ##########################

# Wait for zfs pool "raidpool" to come online
while not check_raidpool_online:
  sleep(1)

### Runtime Checks ##########################
while True:
  dateString = datetime.now().strftime('%b %d %y')
  timeString = datetime.now().strftime('%H:%M:%S')
  lcd.display_string(dateString, 3)
  lcd.display_string(timeString, 4)
  sleep(1)