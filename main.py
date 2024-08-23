import os
import subprocess

def is_hackrf_connected():
    try:
        result = subprocess.run(["hackrf_info"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        if "No HackRF boards found." in output:
            return False
        return True
    except subprocess.CalledProcessError:
        return False

def scan_bluetooth_devices():
    # Check if HackRF is connected
    if not is_hackrf_connected():
        print("No HackRF device connected.")
        return

    # Ensure hackrf_sweep is installed
    try:
        subprocess.run(["hackrf_sweep", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("hackrf_sweep is not installed. Please install it first.")
        return

    # Run hackrf_sweep to scan for Bluetooth devices
    try:
        result = subprocess.run(["hackrf_sweep", "-f", "2400:2483.5", "-a", "1", "-l", "16", "-g", "20"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        print("Detected Bluetooth devices:")
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error scanning for Bluetooth devices: {e}")
        print(f"stderr: {e.stderr.decode('utf-8')}")

if __name__ == "__main__":
    scan_bluetooth_devices()