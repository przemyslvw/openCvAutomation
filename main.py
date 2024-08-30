import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq

# Ustawienia odbioru
frequency = 915e6  # Częstotliwość odbioru (915 MHz)
sample_rate = 10e6  # Prędkość próbkowania (10 MS/s)
duration = 5  # Czas trwania w sekundach

# Komenda do odbioru sygnału
os.system(f'hackrf_transfer -r captured_data.bin -f {frequency} -s {sample_rate} -t {duration}')

# Odczytaj dane z pliku binarnego
def read_binary_file(file_path):
    data = np.fromfile(file_path, dtype=np.complex64)
    return data

data = read_binary_file('captured_data.bin')

# Analiza sygnału
N = len(data)
yf = fft(data)
xf = fftfreq(N, 1 / sample_rate)

# Wizualizacja
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.title('Odczytane dane')
plt.plot(np.real(data))
plt.plot(np.imag(data))
plt.xlabel('Próbki')
plt.ylabel('Amplituda')

plt.subplot(2, 1, 2)
plt.title('Spektrum częstotliwości')
plt.plot(xf, np.abs(yf))
plt.xlabel('Częstotliwość (Hz)')
plt.ylabel('Amplituda')

plt.tight_layout()
plt.show()
