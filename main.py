import numpy as np
import sounddevice as sd

fs = 44100 # frequência de amostragem
duration = 0.2  # segundos

def record():
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return myrecording

def fourier(recording):
    N = len(recording)
    T = 1/fs #Período de amostragem
    freq = np.fft.fftfreq(N, T)[:N//2]
    mag = np.abs(np.fft.fft(recording))
    print(mag[:20])
    return 

recording = record()
fourier(recording)


#try:
    #while True:
        #recorded = record()
#except KeyboardInterrupt:
    #print("Parado pelo usuário.")