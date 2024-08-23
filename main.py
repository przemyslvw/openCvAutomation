import subprocess

def is_hackrf_connected():
    try:
        result = subprocess.run(["hackrf_info"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        print("hackrf_info output:")
        print(output)
        if "No HackRF boards found." in output:
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running hackrf_info: {e}")
        print(f"stderr: {e.stderr}")
        return False

def scan_bluetooth_devices():
    if not is_hackrf_connected():
        print("No HackRF device connected.")

    try:
        subprocess.run(["hackrf_sweep", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        print("hackrf_sweep is not installed or there is an issue with running it.")
        print(f"stderr: {e.stderr}")
        return

    try:
        # Używamy precyzyjnych częstotliwości w Hz
        result = subprocess.run(["hackrf_sweep", "-f", "2400000000:2483500000", "-a", "1", "-l", "16", "-g", "20"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        print("Detected Bluetooth devices:")
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error scanning for Bluetooth devices: {e}")
        print(f"stderr: {e.stderr}")

if __name__ == "__main__":
    scan_bluetooth_devices()
