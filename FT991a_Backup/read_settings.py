import serial
import serial.tools.list_ports
import time
from datetime import datetime
import sys

# Configuration
BAUD = 38400
TIMEOUT = 1.0  # Read timeout in seconds
DATE_STR = datetime.now().strftime("%y%m%d")
FILENAME = f"Setting_{DATE_STR}.txt"

def select_com_port():
    """Scans for COM ports and lets the user pick one."""
    ports = [p.device for p in serial.tools.list_ports.comports()]
    
    if not ports:
        print("No COM ports detected.")
        return None

    print("\nAvailable COM Ports:")
    for i, port in enumerate(ports, 1):
        print(f"{i}- {port}")

    while True:
        try:
            choice = input(f"Select Port index (1-{len(ports)}) or 'q' to quit: ")
            if choice.lower() == 'q': return None
            idx = int(choice) - 1
            if 0 <= idx < len(ports):
                return ports[idx]
            print("Invalid index.")
        except ValueError:
            print("Please enter a number.")

def run_serial_sequence():
    # Ensure console is available for input
    if sys.stdin is None:
        print("Error: No console detected. Compile as a Console Application.")
        return

    # 1) Select the COM Port
    selected_port = select_com_port()
    if not selected_port:
        return

    try:
        # Opens selected port at 38400
        with serial.Serial(selected_port, BAUD, timeout=TIMEOUT) as ser:
            print(f"Connected to {selected_port}. Writing to {FILENAME}...")
            
            with open(FILENAME, "w") as f:
                # 2) Sequence from 001 to 154
                for i in range(1, 155):
                    command = f"EX{i:03d};"
#                    command = f"EX010101;"
                    ser.write(command.encode('ascii'))
                    print(command.encode('ascii'))

                    # 3) Wait 100ms
                    time.sleep(0.1)
                    
                    # Read back the response until the terminator ";"
                    response = ser.read_until(b";").decode('ascii').strip()
                    
                    # 4) Save to file
                    if response:
                        f.write(f"{response}\n")
                        print(f"Sent: {command} | Received: {response}")
                    else:
                        print(f"Sent: {command} | No response received.")

        print("\nSequence complete.")

    except serial.SerialException as e:
        print(f"Serial Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_serial_sequence()
    input("\nPress Enter to exit...")
