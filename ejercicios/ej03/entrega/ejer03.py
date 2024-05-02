import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

##################################################################
# Parámetros PRBS
tipo_binario = True # True = 0 y 1 ; False = -1 y 1
periodo_muestreo = 1/16  # en microsegundos
tiempo_simbolo = 16 * periodo_muestreo  # 1 microsegundo
##################################################################

##################################################################
# Parámetros M1
M = 16


# PRBS (secuencia binaria aleatoria)
# M1 (add sampler agrega ceros a la señal)
# FIR (filtro fir con la forma de nuestro pulso)
# h[k] (canal ideal (delta en 0))
# n[k] ruido aditivo

# Función para generar un número binario según el tipo especificado
def generar_numero_binario(tipo_binario):
    if tipo_binario:
        return random.choice([0, 1])
    else:
        return random.choice([-1, 1])

# Generar 16 números binarios según el tipo especificado
PRBS = [generar_numero_binario(tipo_binario) for _ in range(16)]
print(PRBS)
PRBS = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1]
# PRBS = [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1]
d_k = []

for val in PRBS:
    if val == 1 :
        d_k.append(1.0)
    if val == 0 :
        d_k.append(-1.0)
    d_k.extend([0.0] * (M-1))

d_k = np.array(d_k)

# print(PRBS)
# print(d_k)

def pulso_cuadrado(X):
    # Creamos un vector de tiempo de 0 a X-1
    t = np.arange(X)
    
    # Calculamos el pulso cuadrado
    pulso = np.where((t % 1) < 1 / 2, 1, -1)
    
    descarte = int(np.ceil((M-1)/2))

    return t, pulso, descarte

def pulso_triangular(X):
    # Creamos un vector de tiempo de 0 a X-1
    t = np.arange(X) 
    
    b = 0 if X % 2 == 0 else 0.5
    t2 = t + b

    simetria = 0.5
    pulso = signal.sawtooth(2 * np.pi * (1/X) * (t2), 0.5) / 2 + 0.5 
    
    descarte = int(np.ceil((M-1)/2))
    return t, pulso, descarte


def pulso_seno(X):

    if X % 2 == 0 : # es par
        t = np.linspace(0, np.pi, X + 1 ) # Genera un vector de tiempo de 0 a 2*pi con X muestras
        
        t2 = np.arange(X) 

        pulso = np.sin(t)[:-1]  # Genera el pulso seno
    else : 
        t = np.linspace(0, np.pi, X + 2)  # Genera un vector de tiempo de 0 a 2*pi con X muestras
        pulso = np.cos(t)  # Genera el pulso coseno
        
        t2 = np.arange(X) 
        m= (int)(X/2) + 1
        pulso = pulso[:m]

        pulso = np.concatenate((np.flip(pulso[1:]), pulso))
        
    descarte = int(np.ceil((M-1)/2))
    return t2, pulso, descarte


def pulso_coseno_elevado(X, beta, factor): # X es el numero de muestras por simbolo; factor es el factor multiplicativo (potencia de 2)
    
    num_taps = X * factor - 1
    t = np.arange(num_taps) - (num_taps-1)//2
    t2 = np.arange(num_taps)
    pulso = np.sinc(t/X) * (np.cos(np.pi*beta*t/X) / (1 - (2*beta*t/X)**2) )

    descarte = int((np.ceil(M-1/2)) * 2 - 1)

    return t2, pulso, descarte


t, p_k, dscr = pulso_cuadrado(M)
t, p_k, dscr = pulso_triangular(M)
# t, p_k, dscr = pulso_seno(M)
# t, p_k, dscr = pulso_coseno_elevado(X = M, beta = 0.25, factor = 4)



x_k = np.convolve(d_k, p_k, mode='full')
print(dscr)
x_k = x_k[dscr:]
n_y = np.arange(len(x_k))

# # Graficamos
# plt.figure(figsize=(8, 4))
# plt.plot(t, p_k, 'b-', marker= 'o', linewidth=2)
# plt.title('Pulso Cuadrado')
# plt.xlabel('Muestras')
# plt.ylabel('Amplitud')
# plt.grid(True)

h_k = [1,0,0,0,0,0,0,0]
h_k = np.array(h_k)

xh_k = np.convolve(x_k, h_k, mode='full')

N0 = 0.01  # Varianza del ruido

# Ruido blanco gaussiano aditivo (AWGN)
awgn = np.random.normal(loc=0, scale=np.sqrt(N0), size= len(xh_k))

c_k = xh_k + awgn
# Graficar la convolución resultante

plt.stem(np.arange(len(d_k)), d_k, 'r', markerfmt='bo', basefmt=" ")
# plt.plot(len(d_k), d_k, 'r-', marker= 'o', linewidth=2)
plt.plot(n_y, x_k, 'y-', marker= 'o', linewidth=5)
plt.plot(np.arange(len(c_k)), c_k, 'b-', marker= 'o', linewidth=2)
plt.title('Resultado de la convolución')
plt.xlabel('Índice de tiempo')
plt.ylabel('Amplitud')
plt.grid()
plt.show()
