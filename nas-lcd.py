from time import time, sleep
from datetime import datetime
import sys
import subprocess
import os
import psutil
from psutil._common import bytes2human

def raidpool_status():
  zpool_list = subprocess.run(["zpool", "list", "raidpool", "-o", "health,capacity"], capture_output=True, text=True)
  values = zpool_list.stdout.split("\n")[-2].split()
  return values

def system_stats(last_read_bytes, last_write_bytes, last_net_receive, last_net_send):
  read_bytes = psutil.disk_io_counters().read_bytes
  write_bytes = psutil.disk_io_counters().write_bytes
  net_r = psutil.net_io_counters().bytes_recv
  net_w = psutil.net_io_counters().bytes_sent
  data = {
    "cpu_usage": psutil.cpu_percent(),
    "mem_usage": psutil.virtual_memory().percent,
    "disk_io_read_raw": read_bytes,
    "disk_io_write_raw": write_bytes,
    "disk_io_read_bytes": bytes2human(read_bytes - last_read_bytes),
    "disk_io_write_bytes": bytes2human(write_bytes - last_write_bytes),
    "net_io_recv_raw": net_r,
    "net_io_send_raw": net_w,
    "net_io_recv_bytes": bytes2human(net_r - last_net_receive),
    "net_io_send_bytes": bytes2human(net_w - last_net_send),
    "boot_time": int(psutil.boot_time())
  }
  return data

def check_raidpool_online():
  health = raidpool_status()[0]
  lcd.display_string("raidpool: {}".format(health), 2)
  return health == "ONLINE"

def get_lcd():
  if os.environ.get("DEBUG", "off") == "ON":
    import fake_lcd
    return fake_lcd.FakeLcd()

  bus = 0
  address = 0x3f
  if len(sys.argv) > 1:
    address = int(sys.argv[1], 16)
  if len(sys.argv) > 2:
    bus = int(sys.argv[1])
    address = int(sys.argv[2], 16)
  print("Using LCD parameter: bus={} address={}".format(bus, address))
  import lcddriver
  return lcddriver.lcd(bus, address)

# Setup screen
lcd = get_lcd()
lcd.display_string("LCD - ON", 1)
print("Successfully connected to LCD")

### Startup Checks ##########################
print("Running startup Checks...")
# Wait for zfs pool "raidpool" to come online
startup_complete = False
while not startup_complete:
  startup_complete = check_raidpool_online()
  sleep(1)

### Runtime Checks ##########################

last_read_bytes = 0
last_write_bytes = 0
last_net_recv = 0
last_net_send = 0
while True:
  stats = system_stats(last_read_bytes, last_write_bytes, last_net_recv, last_net_send)
  last_read_bytes = stats["disk_io_read_raw"]
  last_write_bytes = stats["disk_io_write_raw"]
  last_net_recv = stats["net_io_recv_raw"]
  last_net_send = stats["net_io_send_raw"]
  uptime = (datetime.now() - datetime.fromtimestamp(stats["boot_time"])).total_seconds() / 86400
  print(stats)

  timeString = datetime.now().strftime('%H:%M:%S')
#  lcd.display_string("01234567890123456789".format(timeString), 5)
  lcd.display_string("{}, {:.2f} days".format(timeString, uptime), 1)
  lcd.display_string("CPU: {}% Mem: {}%".format(stats["cpu_usage"], stats["mem_usage"]), 2)
  lcd.display_string("Disk(R/W): {}/{}".format(stats["disk_io_read_bytes"], stats["disk_io_write_bytes"]), 3)
  lcd.display_string("Net(R/W): {}/{} ".format(stats["net_io_recv_bytes"], stats["net_io_send_bytes"]), 4)
  sleep(60)
