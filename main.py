import numpy as np
import math
import pandas as pd
import sounddevice as sd

fs = 44100 # frequência de amostragem
duration = 0.2  # segundos
frequenciesVector = []
frequenciesMatrix = [[],[]]

def record():
    try:
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        return myrecording
    
    except Exception as e:
        print("Erro na função record:", e)

def fourier(recording):
    try: 
        N = len(recording)
        T = 1/fs #Período de amostragem
        freq = np.fft.fftfreq(N, T)[:N//2]  #indices das frequencias de fourier 
        mag = np.abs(np.fft.fft(recording.flatten()))[:N//2] #magnitudes das transformadas de fourier

        ##limitar as frequencias entre 20 e 20khz, pois são as únicas úteis para som
        mask = (freq >= 20) & (freq <= 20000)
        freqFiltered = freq[mask]
        magFiltered = mag[mask]


        domFreqIndex = pd.Series(magFiltered).idxmax() #Pega o index da magnitude máxima
        finalFreq = freqFiltered[domFreqIndex]  #A frequencia maxima do intervalo gravado

        ##print("domFreqIndex:", domFreqIndex)
        ##print(domFreqIndex*freq[1])    se domFreqIndex*freq[1] == finalFreq, tudo certo
        ##print(finalFreq)    

        return finalFreq 

    except Exception as e:
        print("Erro na função fourier:", e)

def painting():
    
    return

try:
    while True:
        recorded = record()
        frequenciesVector.append(fourier(recorded))

except KeyboardInterrupt:
    try:
        side = int(math.sqrt(len(frequenciesVector))) ##linha e coluna da matriz quadrada de frequencias
        frequenciesMatrix = np.reshape(frequenciesVector[:side*side], (side, side))
        print("Parado pelo usuário.")
    except Exception as e:
        print("Erro:", e)