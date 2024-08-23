import subprocess

def is_hackrf_connected():
    try:
        result = subprocess.run(["hackrf_info"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode()
        if "Found HackRF" in output:
            return True
        return False
    except subprocess.CalledProcessError:
        return False

# Przykład użycia
if is_hackrf_connected():
    print("HackRF is connected.")
else:
    print("HackRF is not connected.")