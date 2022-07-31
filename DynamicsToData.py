import numpy as np
import matplotlib.pyplot as plt

class Dynamicstodata:
    def __init__(self, modes, dynamics, stim, freq=128):
        self.modes = modes
        self.dynamics = dynamics
        self.freq = freq
        self.powers = None
        self.frequencies = None
        self.stim = stim
        self.actiondict = {1: 'Planning',
                           2: 'Measuring',
                           3: 'Simulation',
                           10: 'Left',
                           0: 'Neutral',
                           12: 'Right',
                           21: '1',
                           22: '2',
                           23: '3'}
        self.mode1 = None
        self.mode2 = None
        self.lives1 = None
        self.lives2 = None
        self.action1 = None
        self.action2 = None
        self.score1 = None
        self.score2 = None

    def calc_powers(self):
        temp = []
        for i in range(self.modes.shape[1]):
            temp.append((np.linalg.norm(self.modes[:, i]) ** 2))

        self.powers = np.array(temp)

    def calc_frequencies(self):
        dynamics = np.diagonal(self.dynamics)
        ws = np.log(dynamics) * self.freq
        self.frequencies = np.absolute((ws.imag / (2*np.pi)))

    def get_data(self, index):

        if 1 <= self.stim[1, index] <= 3 and int(self.stim[0, index]) == 1:
            self.mode1 = self.actiondict[self.stim[1, index]]

        elif 21 <= self.stim[1, index] <= 23 and int(self.stim[0, index]) == 1:
            self.lives1 = self.actiondict[self.stim[1, index]]

        elif 10 <= self.stim[1, index] <= 12 and int(self.stim[0, index]) == 2:
            action = self.actiondict[self.stim[1, index]]
            if action == self.action1:
                self.action1 = 'Neutral'
            else:
                self.action1 = action

        elif self.stim[1, index] >= 25 and int(self.stim[0, index]) == 1:
            self.score1 = self.stim[1, index] - 100

        elif int(self.stim[0, index]) == 0:
            pass

        else:
            self.mode1 = 'ERROR'
            self.lives1 = 'ERROR'
            self.action1 = 'ERROR'
            self.score1 = 'ERROR'

    def plot_eigs(self):
        if not self.powers:
            self.calc_powers()

        weights = []
        for x in self.powers:
            weights.append(x * 100000)

        fig = plt.figure(figsize=(10, 10), layout='constrained')

        dynamics = np.diagonal(self.dynamics)
        # extract real part using numpy array
        x = dynamics.real
        # extract imaginary part using numpy array
        y = dynamics.imag

        ax = fig.add_subplot(1, 1, 1)
        circ = plt.Circle((0, 0), radius=1, edgecolor='b', facecolor='None')
        ax.add_patch(circ)

        # plot the complex numbers
        plt.scatter(x, y, s=weights, facecolors='none', edgecolors='r')
        plt.ylabel('Imaginary')
        plt.xlabel('Real')
        plt.title('Eigenvalues')

        return plt

    def plot_spectrum(self):
        if self.frequencies is None:
            self.calc_frequencies()

        if self.powers is None:
            self.calc_powers()

        fig = plt.figure(figsize=(10, 10), layout='constrained')

        dynamics = np.diagonal(self.dynamics)
        # extract real part using numpy array
        x = self.frequencies
        # extract imaginary part using numpy array
        y = self.powers

        # plot the complex numbers
        plt.stem(x, y, linefmt='-')
        plt.ylabel('Amplitude')
        plt.xlabel('Frequency (Hz)')
        plt.title('Spectrum')

        return plt

    def export(self):
        




