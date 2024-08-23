import pyhackrf
import time
from scapy.all import *

def hackrf_callback(data, length, context):
    # Przetwarzaj odebrane dane
    print(f"Odebrano {length} bajtów danych")
    
    # Kod do analizy pakietów Bluetooth
    # Przykład: analiza danych za pomocą Scapy
    packets = Raw(data)
    for packet in packets:
        if packet.haslayer(Bluetooth):
            bt_layer = packet.getlayer(Bluetooth)
            print(f"Znaleziono urządzenie Bluetooth: {bt_layer.addr}")

    return 0

def initialize_hackrf(frequency):
    # Inicjalizacja urządzenia HackRF
    hackrf = pyhackrf.HackRF()
    hackrf.open()

    # Ustaw częstotliwość odbioru (w Hz)
    hackrf.set_freq(frequency)

    # Ustaw inne parametry, np. próbkowanie, wzmocnienie itp.
    hackrf.set_sample_rate(20e6)  # 20 MHz
    hackrf.set_lna_gain(16)       # Wzmocnienie LNA
    hackrf.set_vga_gain(20)       # Wzmocnienie VGA

    # Rozpocznij odbiór danych
    hackrf.start_rx_mode(hackrf_callback)

    # Odbieraj dane przez określony czas (np. 10 sekund)
    time.sleep(10)

    # Zatrzymaj odbiór i zamknij urządzenie
    hackrf.stop_rx_mode()
    hackrf.close()

# Przykład użycia funkcji
initialize_hackrf(2402e6)  # Ustaw częstotliwość na 2402 MHz (początek pasma Bluetooth)