import numpy as np

class Waveform:
    def __init__(self, name, srate = 48000, freq=1000, ampl=1, offs=0,
            limit=(1,-1)):
        self.name = name
        self.srate = srate
        self.freq = freq
        self.ampl = ampl
        self.offs = offs
        self.limit = limit
        self.bsize = 0

    def GetName(self):
        return self.name

    def GetSampleRate(self):
        return self.srate

    def GetFrequeency(self):
        return self.frq

    def GetAmplitude(self):
        return self.ampl

    def GetOffset(self):
        return self.offs

    def SetName(self, name):
        self.name = name

    def SetSampleRate(self, srate):
        self.srate = srate

    def SetFrequency(self, freq):
        self.freq = freq

    def SetAmplitude(self, ampl):
        self.ampl = ampl

    def SetOffset(self, offs):
        self.offs = offs

    def GetBlockSize(self):
        return self.bsize

    def GetData(self, dur):
        return None


class CyclicWaveform(Waveform):

    def __init(self, *args, **kwgs):
        Waveform.__init(self, *args, **kwgs)
        self.ComputeBlockSize()

    def SetSampleRate(self, srate):
        self.srate = srate
        self.ComputeBlockSize()

    def SetFrequency(self, freq):
        self.freq = freq
        self.ComputeBlockSize()

    def ComputeBlockSize(self, minsize=10, maxsize=None):
        '''
        Compute the block size that yields the best approximation for the
        given frequency and the sample rate
        '''
        if maxsize is None:
            # maximun block size is 1 sec of data
            maxsize = self.srate

        # initial guess
        self.delta = self.freq

        # derive min_k and max_k
        min_k = max(1, int(minsize * self.freq / self.srate))
        max_k = int(self.freq)

        # find the block size that yields minimum difference
        for k in range(min_k, max_k + 1):

            tmp = (k * self.srate) / self.freq
            delta  = abs(tmp - int(tmp))

            if delta == 0:

                self.delta = 0.
                self.bsize = tmp
                self.cycle = k
                break

            elif delta < self.delta:

                self.delta = delta
                self.bsize = int(self.srate * k) / self.freq
                self.cycle = k


class SineWave(CyclicWaveform):
    '''
    Sine wave
    '''
    def __init__(self, name = 'Sine', **kwgs):
        CyclicWaveform.__init__(self, name, **kwgs)


    def GetData(self, dur=None):
        '''
        Return waveform data as (t,f(x)) pair. Argument dur specifies the
        data size in time variable, sec.
        '''

        if dur is None:
            # one block size of data will be returned
            dur = self.bsize / self.srate

        t = np.arange(0, dur, 1 / self.srate)
        wform = (self.ampl * np.sin(2 * np.pi * self.freq * t) + self.offs)
    
        if self.limit is not None:
            wform[wform > self.limit[0]] = self.limit[0]
            wform[wform < self.limit[1]] = self.limit[1]

        return (t, wform)


class TriangleWave(CyclicWaveform):
    '''
    Triangle wave
    '''
    def __init__(self, name = 'Triangle', **kwgs):
        CyclicWaveform.__init__(self, name, **kwgs)

    def GetData(self, dur=None):
        '''
        Return waveform data as (t,f(x)) pair. Argument dur specifies the
        data size in time variable, sec.
        '''

        if dur is None:
            # one block size of data will be returned
            dur = self.bsize / self.srate

        t = np.arange(0, dur, 1 / self.srate)

        temp = self.freq * np.mod(t, 1/self.freq)
        wform = np.zeros_like(temp)
        wform[temp < 0.5] = self.ampl * (-1 + 4 * temp[temp < 0.5])
        wform[temp == 0.5] = self.ampl
        wform[temp > 0.5] = self.ampl * (1 - 4 * (temp[temp > 0.5] - 0.5))

        wform = wform + self.offs

        if self.limit is not None:
            wform[wform > self.limit[0]] = self.limit[0]
            wform[wform < self.limit[1]] = self.limit[1]

        return (t, wform)


class SawtoothWave(CyclicWaveform):
    '''
    Sawtooth wave
    '''
    def __init__(self, name = 'Sawtooth', **kwgs):
        CyclicWaveform.__init__(self, name, **kwgs)

    def GetData(self, dur=None):
        '''
        Return waveform data as (t,f(x)) pair. Argument dur specifies the
        data size in time variable, sec.
        '''

        if dur is None:
            # one block size of data will be returned
            dur = self.bsize / self.srate

        t = np.arange(0, dur, 1 / self.srate)

        wform = (self.offs + 2 * self.ampl * 
                (self.freq * np.mod(t, 1/self.freq) - 0.5)) 

        if self.limit is not None:
            wform[wform > self.limit[0]] = self.limit[0]
            wform[wform < self.limit[1]] = self.limit[1]

        return (t, wform)


class SquareWave(CyclicWaveform):
    '''
    Square wave
    '''
    def __init__(self, name = 'Square', **kwgs):
        CyclicWaveform.__init__(self, name, **kwgs)


    def GetData(self, dur=None):
        '''
        Return waveform data as (t,f(x)) pair. Argument dur specifies the
        data size in time variable, sec.
        '''

        if dur is None:
            # one block size of data will be returned
            dur = self.bsize / self.srate

        t = np.arange(0, dur, 1 / self.srate)

        temp = self.freq * np.mod(t, 1/self.freq) - 0.5
        wform = np.zeros_like(temp)
        wform[temp < 0] = self.ampl
        wform[temp > 0] = -self.ampl

        # do not combine this with above
        wform = wform + self.offs

        if self.limit is not None:
            wform[wform > self.limit[0]] = self.limit[0]
            wform[wform < self.limit[1]] = self.limit[1]

        return (t, wform)


class Chirp(Waveform):
    '''
    Chirp waveform
    '''
    def __init__(self, name = 'Exponential Chirp', **kwgs):
        Waveform.__init__(self, name, **kwgs)
        self.SetSweep(10, 1000)

    def SetMode(self, mode):
        if mode == 'Linear':
            self.name = 'Linear Chirp'
        elif mode == 'Exponential':
            self.name = 'Exponential Chirp'

    def SetSweep(self, f0, k):
        self.f0 = f0
        self.k = k

    def SetFrequency(self, frequency):
        self.k = frequency

    def GetMode(self):
        return self.name[:self.name.rfind('Chirp')]

    def GetSweep(self):
        return (self.f0, self.k)

    def GetFrequency(self):
        return self.k

    def GetData(self, t):
        if 'Linear' in self.name:
            wform = self.amplitude * np.sin(2 * np.pi * (
                    self.f0 * t + 0.5 * self.k * t * t)) + self.offset

        elif 'Exponential' in self.name:
            wform = self.amplitude * np.sin(2 * np.pi * self.f0 * (
                    (self.k** t - 1) / np.log(self.k))) + self.offset

        else:
            return None

        if self.llimit is not None:
            wform[wform < self.llimit] = self.llimit

        if self.ulimit is not None:
            wform[wform > self.ulimit] = self.ulimit

        return wform


class PseudoNoise(Waveform):
    '''
    Pseudo Noise, normal distribution unit magnitude
    '''
    def __init__(self, name = 'Pseudo Noise', **kwgs):
        Waveform.__init__(self, name, **kwgs)

    def GetData(self, t):
        wform =  np.random.standard_normal(t.size)

        # note that it is only an approximation
        if self.llimit is not None:
            wform[wform < self.llimit] = self.llimit

        if self.ulimit is not None:
            wform[wform > self.ulimit] = self.ulimit

        return wform

if __name__ == "__main__":

    a = SineWave(srate=48000, freq=237)

    print('Name: ', a.name)
    print('Frequency: ', a.freq)
    print('Amplitude: ', a.ampl)
    print('SampleRate: ', a.srate)

    a.ComputeBlockSize()

