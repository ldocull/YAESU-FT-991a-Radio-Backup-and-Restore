import serial
import serial.tools.list_ports
import time
import glob
import sys
import os

# Configuration
BAUD = 38400
DELAY = 0.1  # 100ms delay between lines
FILE_PATTERN = "Setting_*.txt"

def get_selection(items, name):
    """Displays a list and returns the user's choice."""
    if not items:
        print(f"No {name} found.")
        return None

    print(f"\nAvailable {name}:")
    for i, item in enumerate(items, 1):
        print(f"{i}- {item}")

    while True:
        try:
            choice = input(f"Select {name} index (1-{len(items)}) or 'q' to quit: ")
            if choice.lower() == 'q': return None
            idx = int(choice) - 1
            if 0 <= idx < len(items):
                return items[idx]
            print("Invalid index.")
        except ValueError:
            print("Please enter a valid number.")

def run_script():
    # Safeguard against 'lost sys.stdin' error in compiled exe
    if sys.stdin is None:
        print("Error: Please compile as a 'Console Application' to allow input.")
        return

    # 1) Select COM Port
    available_ports = [p.device for p in serial.tools.list_ports.comports()]
    selected_port = get_selection(available_ports, "COM Port")
    if not selected_port: return

    # 2) Select File from current directory
    available_files = glob.glob(FILE_PATTERN)
    selected_file = get_selection(available_files, "File")
    if not selected_file: return

    # 3) Open port and send contents line by line
    try:
        # Port closes automatically when 'with' block ends
        with serial.Serial(selected_port, BAUD, timeout=1) as ser:
            print(f"\nSending {selected_file} via {selected_port}...")
            
            with open(selected_file, "r") as f:
                for line in f:
                    # Strip whitespace and add newline back for transmission
                    data = line.strip() + "\n"
                    ser.write(data.encode('ascii'))
                    print(data.encode('ascii'))
                    
                    # 100ms delay between lines
                    time.sleep(DELAY)
                    
            print("Transfer complete.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_script()
    # Keeps the console window open after finishing
    input("\nPress Enter to exit...")
