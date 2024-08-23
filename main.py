import subprocess

def simple_bluetooth_scan():
    try:
        # Check if bluetoothctl is available
        check_result = subprocess.run(["which", "bluetoothctl"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if not check_result.stdout.strip():
            print("bluetoothctl is not installed or not in the PATH.")
            return
        
        # Run the bluetooth scan command
        result = subprocess.run(["bluetoothctl", "scan", "on"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Bluetooth scan started successfully.")
        print(f"stdout: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print("Failed to start Bluetooth scan.")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
    except FileNotFoundError:
        print("bluetoothctl command not found. Please install it and ensure it is in the PATH.")

# Example usage
simple_bluetooth_scan()