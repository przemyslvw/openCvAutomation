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

# Wybierz fragment danych do wizualizacji (np. pierwsze 10000 próbek)
num_samples_to_plot = min(len(data), 10000)
data_to_plot = data[:num_samples_to_plot]

# Analiza sygnału
N = len(data_to_plot)
sample_rate = 10e6  # Prędkość próbkowania
yf = fft(data_to_plot)
xf = fftfreq(N, 1 / sample_rate)

# Wizualizacja
plt.figure(figsize=(12, 8))

# Wykres danych
plt.subplot(2, 1, 1)
plt.title('Odczytane dane (pierwsze próbki)')
plt.plot(np.real(data_to_plot), label='Realna część')
plt.plot(np.imag(data_to_plot), label='Imaginacyjna część')
plt.xlabel('Próbki')
plt.ylabel('Amplituda')
plt.legend(loc='upper right')

# Wykres spektrum częstotliwości
plt.subplot(2, 1, 2)
plt.title('Spektrum częstotliwości')
plt.plot(xf[:N//2], np.abs(yf[:N//2]))
plt.xlabel('Częstotliwość (Hz)')
plt.ylabel('Amplituda')

plt.tight_layout()
# Zapisz wykresy do plików
plt.savefig('data_plot.png')
plt.savefig('spectrum_plot.png')

# Wyświetl wykresy
print("Wykresy zapisane jako 'data_plot.png' i 'spectrum_plot.png'")
