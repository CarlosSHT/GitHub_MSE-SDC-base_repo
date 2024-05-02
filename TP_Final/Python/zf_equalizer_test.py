from numpy import pi,log
from pylab import *
from scipy import signal
# design zero-forcing equalizer for given channel and get tap weights and
# filter the input through the equalizer find equalizer co-effs for given CIR
from equalizers import zeroForcing

nSamp=5 #%Number of samples per symbol determines baud rate Tsym
Fs=100 # Sampling Frequency of the system
Fs=16000000 # Sampling Frequency of the system
Ts=1/Fs # Sampling time
Tsym=nSamp*Ts # symbol time period


t = np.arange(start=0,stop=20 * Ts,step=Ts)

h_t = np.array([532, 483, 0, 0, 223, 366, 0, 0, 425, -487, 0, 0, 55, 0, 0, 0, 0, 22, 0, 0])

h_k = h_t[0::nSamp] # downsampling to represent symbol rate sampler
t_inst=t[0::nSamp] # symbol sampling instants

# Equalizer Design Parameters
N = 12 # Desired number of taps for equalizer filter
delay = None

zf = zeroForcing(N) #initialize ZF equalizer (object) of length N
mse = zf.design(h=h_k,delay=delay) #design equalizer and get Mean Squared Error
w = zf.w # get the tap coeffs of the designed equalizer filter

r_k=h_k # Test the equalizer with the sampled channel response as input
d_k=zf.equalize(r_k) # filter input through the eq
h_sys=zf.equalize(h_k) # overall effect of channel and equalizer


zf_weights= (np.round(w * (2**25),0)).astype(int)
np.savetxt('coeff.txt', zf_weights, fmt='%d')

print('\n\nZF equalizer integer weights:{}'.format(zf_weights))

# Respuesta al impulso del filtro FIR
respuesta_impulso = np.zeros(len(zf_weights)+10)
respuesta_impulso[0:len(zf_weights)] = zf_weights

# Respuesta en frecuencia del filtro FIR
frecuencia, respuesta_frecuencia = signal.freqz(zf_weights, fs=Fs)

Omega_1, H_F  =signal.freqz(h_k, fs=Fs) # frequency response of channel
Omega_2, W =signal.freqz(w, fs=Fs) # frequency response of equalizer
Omega_3, H_sys =signal.freqz(h_sys, fs=Fs) # frequency response of overall system



fig, ((a1,a2), (a3, a4)) = plt.subplots(nrows=2,ncols =2)

a1.plot(t,h_t,label='continuous-time model') #response at sampling instants

# channel response at symbol sampling instants
a1.stem(t_inst,h_k,'r',label='discrete-time model')
a1.set_title('Channel impulse response')
a1.set_xlabel('Time (s)')
a1.set_ylabel('Amplitude')

a2.plot(Omega_1/pi,20*log(abs(H_F)/max(abs(H_F))),'b',label='channel')
a2.plot(Omega_2/pi,20*log(abs(W)/max(abs(W))),'r',label='ZF equalizer')
a2.plot(Omega_3/pi,20*log(abs(H_sys)/max(abs(H_sys))),'k',label='overall system')
a2.set_title('Frequency response');
a2.set_ylabel('Magnitude(dB)');
a2.set_xlabel('Normalized frequency(x $\pi$ rad/sample)');

a3.stem(respuesta_impulso)
a3.set_title('Respuesta al impulso del Filtro FIR escalado')
a3.set_xlabel('Muestras')
a3.set_ylabel('Amplitud')

a4.plot(frecuencia, 20 * np.log10(np.abs(respuesta_frecuencia)))
a4.set_title('Espectro en frecuencia del Canal')
a4.set_xlabel('Frecuencia (Hz)')
a4.set_ylabel('Magnitud (dB)')
a4.grid()
show()