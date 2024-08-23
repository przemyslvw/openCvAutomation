import os
import subprocess

def scan_bluetooth_devices():
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