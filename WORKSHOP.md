# 1. Hardware Reconnaissance

- Locate datasheets for various components and understand their roles
- Use a multimeter to validate specific connections
- Identify potential pins/ports dedicated to debug protocols

### Picture GL-MT300N-V2 Mango: Back
![[glinet_back.jpg]]
### Picture GL-MT300N-V2 Mango: Front
![[glinet_front.jpg]]

### Datasheets:
- [Mediatek MCU](https://files.seeedstudio.com/products/114992470/MT7628_datasheet.pdf)
- [Winbond Flash](https://www.mouser.com/datasheet/2/949/w25q128jv_revf_03272018_plus-1489608.pdf)
# 2. Firmware Dump

- Quick explanation of how the flash communicates with the MCU via SPI
- Tutorial on using flashrom with the ch341a
- Firmware dumping
- Quick analysis with binwalk / strings / grep
#### Dump with CH341A inside custom docker container:
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
flashrom v1.2 on Linux 6.8.0-48-generic (x86_64)
flashrom is free software, get the source code at https://flashrom.org

flashrom was built with libpci 3.6.4, GCC 9.2.1 20200224, little endian
Command line (7 args): flashrom -V -p ch341a_spi -c W25Q128.V -r dump.bin
Using clock_gettime for delay loops (clk_id: 1, resolution: 1ns).
Initializing ch341a_spi programmer
Device revision is 3.0.4
The following protocols are supported: SPI.
Probing for Winbond W25Q128.V, 16384 kB: probe_spi_rdid_generic: id1 0xef, id2 0x4018
Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) on ch341a_spi.
Chip status register is 0x00.
This chip may contain one-time programmable memory. flashrom cannot read
and may never be able to write it, hence it may not be able to completely
clone the contents of this chip (see man page for details).
Reading flash... 
```
#### Binwalk and Strings/Grep
![[Pasted image 20241113161248.png]]
# 3. Serial connection: UART

- Brief explanation of UART, its purpose for design and debugging
- Tutorial on using USB to TTL and miniterm
- Quick log analysis and gathering info on the boot process

### Analysis of u-boot logs

#### U-boot version, flash ID/Size, autoboot stopkey, boot informations
![[Pasted image 20241113155724.png]]
#### Flash partitions
![[Pasted image 20241113160007.png]]

# 4. U-Boot

- Interrupting the U-Boot autoboot sequence
- Description of available commands (`?` || `help`)
- Overview of various environment variables, especially those dedicated to booting (`printenv`)
- Demonstration of firmware dumping via `md` and cleaning with `xxd`

#### Dump FW with Memory Dump (`md`)

`md` is the command we will use to dump memory located on the flash

#### To log output of miniterm inside a file
```
╭─ ~ ▓▒░                                                         
╰─ miniterm /dev/ttyUSB0 115200 --raw | tee firmware_glinet.txt`
```

#### Once inside U-Boot console:
```
MT7628 # md bc050000 23ea4e
bc050000: 56190527 6369159a 42af3264 4eea2300    '..V..icd2.B.#.N
bc050010: 00000080 00000080 406f3a1a 03020505    .........:o@....
bc050020: 5350494d 65704f20 7472576e 6e694c20    MIPS OpenWrt Lin
bc050030: 352d7875 2e30312e 00363731 00000000    ux-5.10.176.....
bc050040: 8000006d 78973a00 00000000 6f000000    m....:.x.......o
bc050050: a3fffffd f7b97fb7 e6870a79 9be8b5d9    ........y.......
bc050060: 960dd7ad e54d5309 4eafdfdd 6934b678    .....SM....Nx.4i
bc050070: ff352824 9e0145c9 0ef18b22 72daa881    $(5..E.."......r
bc050080: 05279a84 4798cf8a 3dfe578a d23bc526    ..'....G.W.=&.;.
bc050090: cd36fe24 80b5cd5c 8c112fa0 c2466227    $.6.\..../..'bF.
bc0500a0: 9b2473b0 89cbb5c5 ca62566c 5de61366    .s$.....lVb.f..]
bc0500b0: 61598e0d 53b1237b 69f793ec 42aa54fd    ..Ya{#.S...i.T.B
bc0500c0: 1ca4b9be 7bc3be87 d769b8d0 497d1ede    .......{..i...}I
.
.
.
```

Exit serial console and clean `firmware_glinet.txt` to only keep the hexdump
#### Convert hexdump to binary
```
╭─ ~ ▓▒░                                                         
╰─ cut -d' ' -f2-9 firmware_glinet.txt | xxd -r -p > firmware_little_endian.bin
╭─ ~ ▓▒░                                                         
╰─ xxd -e -g4 firmware_little_endian.bin temp.txt
╭─ ~ ▓▒░                    
╰─ xxd -r temp.txt firmware_glinet.bin 
```

#### Read Flash memory with `spi` cmd
```
MT7628 # spi read 1d940 78
read len: 120
62 6f 6f 74 63 6d 64 3d 62 6f 6f 74 6d 20 30 78 62 63 30 35 30 30 30 30 0 62 6f 6f 74 64 65 6c 61 79 3d 35 0 62 61 75 64 72 61 74 65 3d 31 31 35 32 30 30 0 65 74 68 61 64 64 72 3d 22 30 30 3a 41 41 3a 42 42 3a 43 43 3a 44 44 3a 31 30 22 0 69 70 61 64 64 72 3d 31 39 32 2e 31 36 38 2e 31 2e 31 0 73 65 72 76 65 72 69 70 3d 31 39 32 2e 31 36 38 2e 31 2e 32
```


```
>>> a = "62 6f 6f 74 63 6d 64 3d 62 6f 6f 74 6d 20 30 78 62 63 30 35 30 30 30 30 0 62 6f 6f 74 64 65 6c 61 79 3d 35 0 62 61 75 64 72 61 74 65 3d 31 31 35 32 30 30 0 65 74 68 61 64 64 72 3d 22 30 30 3a 41 41 3a 42 42 3a 43 43 3a 44 44 3a 31 30 22 0 69 70 61 64 64 72 3d 31 39 32 2e 31 36 38 2e 31 2e 31 0 73 65 72 76 65 72 69 70 3d 31 39 32 2e 31 36 38 2e 31 2e 32".split(" ")
>>> for c in a:
...     r+=chr(int("0x"+c,16))
... 
>>> r
'bootcmd=bootm 0xbc050000\x00bootdelay=5\x00baudrate=115200\x00ethaddr="00:AA:BB:CC:DD:10"\x00ipaddr=192.168.1.1\x00serverip=192.168.1.2'
```
# 5. Depthcharge

- Overview of Depthcharge’s utility for automating tasks, especially when the U-Boot environment is non-persistent: https://depthcharge.readthedocs.io/en/latest/introduction.html
- Small demo scripts including:
	- Interrupting U-Boot autoboot
	- `printenv`
	- `setenv` / `saveenv`
	- Using `md` to automate firmware extraction, for example

#### Change bootdelay varenv value
![[Pasted image 20241113145630.png]]
#### Dump FW with Memory Dump
![[Pasted image 20241113155026.png]]

# 6. Fast Firmware Analysis

- Extracting different parts of the firmware with `binwalk` and `dd`
- Exploring extracted FS
- Uncompress LZMA data

### Analyse FW with `binwalk`
```bash
╭─ ~/Projects/Grehack24_Workshop/binaries ▓▒░ ░▒▓ ✔ 
╰─ binwalk --signature --term dump.bin 

DECIMAL       HEXADECIMAL     DESCRIPTION
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
96832         0x17A40         U-Boot version string, "U-Boot 1.1.3 (Apr 26 2018 - 15:30:15)"
97147         0x17B7B         HTML document header
98939         0x1827B         HTML document header
100619        0x1890B         HTML document header
102475        0x1904B         HTML document header
103259        0x1935B         HTML document header
104247        0x19737         HTML document header
327680        0x50000         uImage header, header size: 64 bytes, header CRC: 0x15EFA0FD, created: 2018-08-16 07:51:15, image size: 1544522 bytes, Data Address: 0x80000000, Entry Point: 0x80000000, data CRC:
                              0x6EB209C4, OS: Linux, CPU: MIPS, image type: OS Kernel Image, compression type: lzma, image name: "MIPS OpenWrt Linux-4.14.63"
327744        0x50040         LZMA compressed data, properties: 0x6D, dictionary size: 2097152 bytes, uncompressed size: 4873916 bytes
1872266       0x1C918A        Squashfs filesystem, little endian, version 4.0, compression:xz, size: 11388493 bytes, 3385 inodes, blocksize: 262144 bytes, created: 2020-12-07 07:32:54
13303808      0xCB0000        JFFS2 filesystem, little endian

╭─ ~/Projects/Grehack24_Workshop/binaries ▓▒░░▒▓ ✔ 
╰─ dd if=dump.bin of=openwrt.bin.lzma bs=1 skip=327744 count=1544522
1544522+0 records in
1544522+0 records out
1544522 bytes (1,5 MB, 1,5 MiB) copied, 1,15656 s, 1,3 MB/s

# Uncompress extracted LZMA compressed data
╭─ ~/Projects/Grehack24_Workshop/binaries ▓▒░░▒▓ ✔ 
╰─ unlzma openwrt.bin.lzma   
╭─ ~/Projects/Grehack24_Workshop/binaries ▓▒░░▒▓ ✔ 
╰─ ls         
dump.bin  openwrt.bin

# Checking architecture
╭─ ~/Projects/Grehack24_Workshop/binaries ▓▒░░▒▓ ✔ 
╰─ binwalk --opcodes openwrt.bin | head

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
17560         0x4498          MIPSEL instructions, function epilogue
17776         0x4570          MIPSEL instructions, function epilogue
18172         0x46FC          MIPSEL instructions, function epilogue
18236         0x473C          MIPSEL instructions, function epilogue
18242         0x4742          MIPS instructions, function epilogue
19496         0x4C28          MIPSEL instructions, function epilogue
19502         0x4C2E          MIPS instructions, function epilogue

# Extract FileSystem
╭─ ~/Projects/Grehack24_Workshop/binaries ▓▒░░▒▓ ✔ 
╰─ binwalk --extract --quiet dump.bin 

╭─ ~/Projects/Grehack24_Workshop/binaries ▓▒░░▒▓ ✔ 
╰─ ls -la _dump.bin-0.extracted 
total 35356
drwxrwxr-x  4 s4tb0y s4tb0y     4096 nov.  14 12:17 .
drwxrwxr-x  4 s4tb0y s4tb0y     4096 nov.  14 12:17 ..
-rw-rw-r--  1 s4tb0y s4tb0y 11388493 nov.  14 12:17 1C918A.squashfs
-rw-rw-r--  1 s4tb0y s4tb0y  4873916 nov.  14 12:17 50040
-rw-rw-r--  1 s4tb0y s4tb0y 16449472 nov.  14 12:17 50040.7z
-rw-rw-r--  1 s4tb0y s4tb0y  3473408 nov.  14 12:17 CB0000.jffs2
drwxr-xr-x 16 s4tb0y s4tb0y     4096 déc.   7  2020 squashfs-root
drwxrwxr-x  2 s4tb0y s4tb0y     4096 nov.  14 12:17 squashfs-root-0

╭─ ~/Projects/Grehack24_Workshop/binaries ▓▒░░▒▓ ✔
╰─ ls _dump.bin-0.extracted/squashfs-root 
bin  dev  etc  lib  mnt  overlay  proc  rom  root  sbin  sys  tmp  usr  var  www

# Entropy analysis on whole Firmware
╭─ ~/Projects/Grehack24_Workshop ▓▒░░▒▓ ✔ 
╰─ binwalk -E dump.bin                     

DECIMAL       HEXADECIMAL     ENTROPY
--------------------------------------------------------------------------------
0             0x0             Falling entropy edge (0.681420)
327680        0x50000         Rising entropy edge (0.997233)
13254656      0xCA4000        Falling entropy edge (0.839507)
14884864      0xE32000        Rising entropy edge (0.950468)
14909440      0xE38000        Falling entropy edge (0.644406)
16121856      0xF60000        Rising entropy edge (0.993237)
16171008      0xF6C000        Falling entropy edge (0.831642)
16187392      0xF70000        Rising entropy edge (0.994545)
16580608      0xFD0000        Falling entropy edge (0.727547)
16605184      0xFD6000        Falling entropy edge (0.699650)
16629760      0xFDC000        Falling entropy edge (0.825994)
16687104      0xFEA000        Falling entropy edge (0.701434)
16719872      0xFF2000        Rising entropy edge (0.976700)

```
##### Entropy plot
![[Entropy.png]]


