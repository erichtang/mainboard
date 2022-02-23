# mainboard-fw
Pycubed Mainboard Firmware

How-to section works only if the build environment is set up. I used a Windows 10 machine running WSL with Ubuntu 20.04 LTS
[This adafruit guide](https://learn.adafruit.com/building-circuitpython/windows-subsystem-for-linux) has has some information on getting the env setup

## How to build a new bootloader version

clone the uf2-samdx repo:
```
cd your/workspace
git clone github.com/microsoft/uf2-samdx1
```

[move the directory](https://github.com/Sierra-Lobo/mainboard-fw/tree/main/bootloader_build/pycubed_N20) `/bootloader_build/pycubed_N20` into `uf2-samdx1/boards`

next run:
```
make BOARD=name_of_added_directory
```
the build process should spit out .uft and .bin files for specific programming

## How to build a new bootloader version

[follow this guide](https://learn.adafruit.com/building-circuitpython/build-circuitpython)
