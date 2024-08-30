import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import os

# Ścieżka do pliku z danymi
file_path = 'captured_data.bin'

# Sprawdź, czy plik istnieje
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Plik {file_path} nie został znaleziony. Upewnij się, że 'hackrf_transfer' został prawidłowo wykonany.")

# Odczytaj dane z pliku binarnego
def read_binary_file(file_path):
    # Wczytaj dane jako dane o typie np.complex64
    data = np.fromfile(file_path, dtype=np.complex64)
    return data

data = read_binary_file(file_path)

# Sprawdź długość danych
print(f"Liczba próbek: {len(data)}")

# Analiza sygnału
N = len(data)
sample_rate = 10e6  # Prędkość próbkowania
yf = fft(data)
xf = fftfreq(N, 1 / sample_rate)

# Wizualizacja
plt.figure(figsize=(12, 8))

# Wykres danych
plt.subplot(2, 1, 1)
plt.title('Odczytane dane')
plt.plot(np.real(data), label='Realna część')
plt.plot(np.imag(data), label='Imaginacyjna część')
plt.xlabel('Próbki')
plt.ylabel('Amplituda')
plt.legend()

# Wykres spektrum częstotliwości
plt.subplot(2, 1, 2)
plt.title('Spektrum częstotliwości')
plt.plot(xf, np.abs(yf))
plt.xlabel('Częstotliwość (Hz)')
plt.ylabel('Amplituda')

plt.tight_layout()
plt.show()
