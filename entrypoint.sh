#!/bin/bash

echo "Available i2c Bus:"
i2cdetect -l

for bus_name in $(i2cdetect -l | awk -e '/Synopsys DesignWare I2C adapter/{ print $1 }'); do 
  
  # Probe if there is a device on address 0x27 (decimal 39)
  echo "Probing: $bus_name"
  bus_number=$(echo $bus_name | cut -f 2 -d '-')
  if $(i2cdetect -y -r 1 39 39 | grep --quiet 27 ); then 
    BUS=$bus_number
    ADDRESS="27"
done

echo Strarting script with args: $BUS $ADDRESS
exec python3 nas-lcd.py "$BUS" "$ADDRESS"