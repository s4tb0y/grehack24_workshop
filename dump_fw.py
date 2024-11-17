from depthcharge import Console, log

def modify_and_printenv():
    # Create a Depthcharge session
    print("Creating Depthcharge session")
    console = Console("/dev/ttyUSB0", baudrate=115200)
    log.set_level('DEBUG')

    # Cancel autoboot
    log.info("Cancelling autoboot...")
    console.interrupt(interrupt_str="gl")
    log.info("Autoboot cancelled !")

    # To get rid of the remaining gls
    console.send_command('?')

    # Dumping memory
    log.info("Dumping memory...") 
    memory_output = console.send_command('md 0xbc050000 0x1000')

    # Save the output to a file
    with open("memory_dump.txt", "w") as f:
        f.write(memory_output)


if __name__ == "__main__":
    modify_and_printenv()