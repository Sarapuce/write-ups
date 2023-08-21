# Guide to work with .efi files

This is just a reminder of how I debuged a .efi file. No flag can be found here

## How to start a .efi file with QEMU

### Create a disk image containing the file

```
$ dd if=/dev/zero of=./uefi.img bs=512 count=93750

$ gdisk /path/to/uefi.img
GPT fdisk (gdisk) version 0.8.10

Partition table scan:
  MBR: not present
  BSD: not present
  APM: not present
  GPT: not present

Creating new GPT entries.

Command (? for help): o
This option deletes all partitions and creates a new protective MBR.
Proceed? (Y/N): y

Command (? for help): n
Partition number (1-128, default 1): 1
First sector (34-93716, default = 2048) or {+-}size{KMGTP}: 2048
Last sector (2048-93716, default = 93716) or {+-}size{KMGTP}: 93716
Current type is 'Linux filesystem'
Hex code or GUID (L to show codes, Enter = 8300): ef00
Changed type of partition to 'EFI System'

Command (? for help): w

Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
PARTITIONS!!

Do you want to proceed? (Y/N): y
OK; writing new GUID partition table (GPT) to uefi.img.
Warning: The kernel is still using the old partition table.
The new table will be used at the next reboot.
The operation has completed successfully.


$ sudo losetup --offset 1048576 --sizelimit 46934528 /dev/loop0 ./uefi.img

$ sudo mkdosfs -F 32 /dev/loop0

$ sudo mount /dev/loop0 /mnt

$ sudo cp crackme.efi /mnt/

$ sudo umount /mnt

$ sudo losetup -d /dev/loop0
```

Next, you need to download the OVMF file which can be found on this [repo](https://www.kraxel.org/repos/jenkins/edk2/). You can now start the executable with :

```
$ qemu-system-x86_64 -cpu qemu64 -bios ./OVMF_CODE.fd -drive file=uefi.img,if=ide -nographic -net none
```

### How to debug this file 

Start qemu with this :

```
$ qemu-system-x86_64 -cpu qemu64 -bios ./OVMF_CODE.fd -drive file=uefi.img,if=ide -nographic -net none -s -debugcon file:debug.log -global isa-debugcon.iobase=0x402
```

`-s` stands for `-gdb tcp::1234`

You will have a file called debug.log in your current repository
Start the efi file and then watch the log

```
$ tail debug.log

InstallProtocolInterface: 5B1B31A1-9562-11D2-8E3F-00A0C969723B 64FC2C0
Loading driver at 0x0000647A000 EntryPoint=0x0000647D000
InstallProtocolInterface: BC62157E-3E33-4FEC-9920-2D3B36D750DF 64FCE18
```

The address "Loading driver" 0x0000647A000 is the base addresse of the executable.

Start gdb and run

```
$ gdb crackme.efi
(gdb) remote target :1234
```

(You can add symbol but I don't have them)

You can now go to IDA in text view and place a breakpoint to (base address + the offset). For example :

.text:0000000000003249                 mov     [rbp+var_4], 0

```
(gdb) b *0x0000647D249
```
