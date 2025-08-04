import math
import numpy as np
import pandas as pd
import sounddevice as sd
import matplotlib.pyplot as plt

fs = 44100 # frequência de amostragem
duration = 0.1  # segundos
recorded = []
frequenciesVector = []
frequenciesMatrix = [[],[]]


def recording():
    try:
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        recorded.append(myrecording)
        sd.wait()
        return 

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

def painting(soundFreqMatrix):
    ## 380(violeta) - 750(vermelho)nm, lambda inverso da frequencia, logo, frequencias menores -> lambdas maiores vice versa 
    try:
        waveLengthMatrix = np.zeros((soundFreqMatrix.shape), dtype=int)
        for i in range(soundFreqMatrix.shape[0]):  
            for j in range(soundFreqMatrix.shape[1]):  
                x = soundFreqMatrix[i, j]
                y = (x-20)/(6000-20)   ####fazer até 6khz ao invs de 20khz, para testes
                waveLengthMatrix[i][j] = int(750 - (y*380))

        ## temos 370nm entre os extremos de cores, vamos dividir em 16 pedaços
        ## site de wavelengths to rgb https://405nm.com/wavelength-to-color/
        size = soundFreqMatrix.shape[0]
        rgbMatrix = np.zeros((size, size, 3), dtype=int)
        ##for i in range(waveLengthMatrix.shape[0]):
            ##for j in range(soundFreqMatrix.shape[1]):
                ##if waveLengthMatrix[i][j] <= 403.125:
                    ##rgbMatrix[i][j] = [123, 0, 145]
                ##elif 403.125 < waveLengthMatrix[i][j] <= 426.25:
                    ##rgbMatrix[i][j] = [120, 0, 233]
                ##elif 426.25 < waveLengthMatrix[i][j] <= 449.375:
                    ##rgbMatrix[i][j] = [23, 0, 255]
                ##elif 449.375 < waveLengthMatrix[i][j] <= 472.5:
                    ##rgbMatrix[i][j] = [0, 123, 255]
                ##elif 472.5 < waveLengthMatrix[i][j] <= 495.625:
                    ##rgbMatrix[i][j] = [0, 230, 255]
                ##elif 495.625 < waveLengthMatrix[i][j] <= 518.75:
                    ##rgbMatrix[i][j] = [0, 255, 56]
                ##elif 518.75 < waveLengthMatrix[i][j] <= 541.875:
                    ##rgbMatrix[i][j] = [94, 255, 0]
                ##elif 541.875 < waveLengthMatrix[i][j] <= 565:
                    ##rgbMatrix[i][j] = [173, 255, 0]
                ##elif 565 < waveLengthMatrix[i][j] <= 588.125:
                    ##rgbMatrix[i][j] = [243, 255, 0]
                ##elif 588.125 < waveLengthMatrix[i][j] <= 611.25:
                    ##rgbMatrix[i][j] = [255, 193, 0]
                ##elif 611.25 < waveLengthMatrix[i][j] <= 634.375:
                    ##rgbMatrix[i][j] = [255, 111, 0]
                ##elif 634.375 < waveLengthMatrix[i][j] <= 657.5: ### aparentemente daqui pra frente, é só vermelho mesmo
                    ##rgbMatrix[i][j] = [254, 0, 0]
                ##elif 657.5 < waveLengthMatrix[i][j] <= 680.625:
                    ##rgbMatrix[i][j] = [233, 0, 0]
                ##elif 680.625 < waveLengthMatrix[i][j] <= 703.75:
                     ##rgbMatrix[i][j] = [213, 0, 0]
                ##else:
                    ##rgbMatrix[i][j] = [150, 0, 0] 
            
        for i in range(soundFreqMatrix.shape[0]):
            for j in range(soundFreqMatrix.shape[1]):
                if soundFreqMatrix[i][j] <= 100:
                    rgbMatrix[i][j] = [255, 0, 0]
                elif 100 < soundFreqMatrix[i][j] <= 200:
                    rgbMatrix[i][j] = [246, 120, 40]
                elif 200 < soundFreqMatrix[i][j] <= 400:
                    rgbMatrix[i][j] = [246, 120, 40]
                elif 400 < soundFreqMatrix[i][j] <= 800:
                    rgbMatrix[i][j] = [0, 128, 0]
                elif 800 < soundFreqMatrix[i][j] <= 1600:
                    rgbMatrix[i][j] = [65, 105, 255]
                elif 1600 < soundFreqMatrix[i][j] <= 3200:
                    rgbMatrix[i][j] = [29, 26, 68]
                else:
                    rgbMatrix[i][j] = [148, 0, 211]
                
        
        

        displayImage(rgbMatrix)
        return 
    
    except Exception as e:
        print("Erro na função painting", e)
    
def displayImage(image):
    plt.imshow(image)
    plt.show()

try:
    while True:
        try:    
            recording()
        except Exception as e:
            print("Erro:", e)

except KeyboardInterrupt:
    try:
        for i in recorded:
            frequenciesVector.append(fourier(i))
        side = int(math.sqrt(len(frequenciesVector))) ##linha e coluna da matriz quadrada de frequencias
        frequenciesMatrix = np.reshape(frequenciesVector[:side*side], (side, side))
        print(frequenciesMatrix)
        painting(frequenciesMatrix)
        print("Parado pelo usuário.")
    except Exception as e:
        print("Erro:", e)
