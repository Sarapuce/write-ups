# Cheat Sheet for GDB

## Display 

### Get the current instruction
`display/i $rip`

### Read all normal registers 
`i r`

### Read all registers
`i all-registers`

### Examine somewhere in the memory
`x/32x 0x400078`
`x/i $rip`
`x/c ($rax+12)`

## Step

### Start the program
`r`

### Start the program in debug state
`strati`

### Step without entering the fonction
`ni`

### Step with entering the function
`si`

### Run until breakpoint
`c`

### Place a breakpoint
`b *0x40012c`

### Place a hardware breakpoint
`thbreak *0x400220`

## Modify

### Modify value in a address
`set {int}0x400210 = 0x5484a2ff`

## IDA

1. Start gdb with gdb server (attach or create the process)
```
$ gdbserver localhost:1234 gown
$ gdbserver localhost:23947 --attach <PID>
```

2. In IDA, go to Debugger > Start debugger

3. Then Debugger > Start Process
