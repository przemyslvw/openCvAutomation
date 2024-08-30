from hackrf import HackRF
from pylab import psd, xlabel, ylabel, show

# Initialize HackRF device
with HackRF() as hrf:
    # Set sample rate and center frequency
    hrf.sample_rate = 20e6
    hrf.center_freq = 88.5e6

    # Read samples from HackRF
    samples = hrf.read_samples(2e6)

    # Use matplotlib to estimate and plot the PSD
    psd(samples, NFFT=1024, Fs=hrf.sample_rate/1e6, Fc=hrf.center_freq/1e6)
    xlabel('Frequency (MHz)')
    ylabel('Relative power (dB)')
    show()