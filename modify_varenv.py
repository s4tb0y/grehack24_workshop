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

    # Printin varenvs
    log.info("Printing varenvs...") 
    env_output = console.send_command('printenv')

    # Print U-Boot varenvs 
    for line in env_output.splitlines():
        print(line)
    
    # Set varenv bootcmd to gain root shell
    log.info("Setting bootdelay to 8s...")
    new_cmd = '8'
    console.send_command("setenv bootdelay "+new_cmd)

    # Printin varenvs
    log.info("Printing varenvs...") 
    env_output = console.send_command('printenv')

    # Print U-Boot varenvs 
    for line in env_output.splitlines():
        print(line)

if __name__ == "__main__":
    modify_and_printenv()