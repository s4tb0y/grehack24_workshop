# grehack24_workshop

## Install docker binary

https://docs.docker.com/engine/install/binaries/

## Build and run docker container

clone repository and execute command inside directory

`docker build -t workshop_env .`

`docker run -it --rm workshop_env`

## Use case: Dumping firmware of the GL-MT300N-V2 Mango with flashreader CH341A

If you want to run docker with flash reader for example:

```
╭─ ~/Projects/Grehack24_Workshop/container ▓▒░░▒▓ 
╰─ lsusb                  
Bus 003 Device 008: ID 1a86:5512 QinHeng Electronics CH341 in EPP/MEM/I2C mode, EPP/I2C adapter

╭─ ~/Projects/Grehack24_Workshop/container ▓▒░░▒▓ 
╰─ ls /dev/bus/usb/003/008 
/dev/bus/usb/003/008

╭─ ~/Projects/Grehack24_Workshop/container ▓▒░░▒▓ 
╰─ docker run -it --rm --device=/dev/bus/usb/003/008 workshop_env

root@92414891bddb:/workspace# flashrom -V -p ch341a_spi -c "W25Q128.V" -r dump.bin
```

## Depthcharge scripts for GL-MT300N-V2 Mango Target

You can find inside depthcharge_script directory two examples of automated tasks regarding the device GL-MT300N-V2 Mango.
