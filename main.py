import subprocess

def simple_bluetooth_scan():
    try:
        result = subprocess.run(["bluetoothctl", "scan", "on"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Bluetooth scan started successfully.")
        print(f"stdout: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print("Failed to start Bluetooth scan.")
        print(f"stderr: {e.stderr}")

# Example usage
simple_bluetooth_scan()