import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

class Dynamicstodata:
    def __init__(self, modes, dynamics, freq=128):
        self.modes = modes
        self.dynamics = dynamics
        self.freq = freq
        self.powers = None
        self.frequencies = None
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

    def plot_eigs(self, show=True):
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

        if show:
            plt.show()

        return plt

    def plot_spectrum(self, show=True):
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

        if show:
            plt.show()

        return plt

    def plot_modes(self, freqlow, freqhigh, number=None, rows=2, show=True, arr='power'):
        if self.frequencies is None:
            self.calc_frequencies()

        if self.powers is None:
            self.calc_powers()

        modes_indexes = []
        frequencies = []
        for i, x in enumerate(self.frequencies):
            if freqlow <= x <= freqhigh:
                modes_indexes.append(i)
                frequencies.append(x)

        modes = np.zeros((self.modes.shape[0], len(modes_indexes)), dtype=complex)
        powers = []
        for i, x in enumerate(modes_indexes):
            modes[:, i] = self.modes[:, x]
            powers.append(self.powers[x])

        modes = np.concatenate(([powers], modes), axis=0)
        modes = np.concatenate(([frequencies], modes), axis=0)

        if arr == 'frequency':
            sorting_indexes = np.argsort(modes[0])
        elif arr == 'power':
            sorting_indexes = np.argsort(modes[1])
        else:
            return print('Arg Error')
        modes = modes[:, sorting_indexes]
        modes = np.flip(modes, axis=1)

        if number:
            end = min(number, modes.shape[1])
        else:
            end = modes.shape[1]

        plots = []
        alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
        rowlist = []
        for i in range(rows):
            rowlist.append(str(i))

        for i in range(end):
            matrixabs = np.absolute(modes[2:(14*rows) + 2, i])
            matrixabs = np.reshape(matrixabs, (-1, 14))
            color_lims = np.percentile(matrixabs, [0, 100])
            figure = plt.figure(figsize=(15, 5), frameon=False)
            ax1 = figure.add_subplot(211)
            ax1.set_title(f'Mode Energy - {i}: Frequency {modes[0, i]} Hz, Power {modes[1, i]}')
            caxes = ax1.matshow(matrixabs.tolist(), clim=color_lims, cmap='YlOrRd', aspect=1)
            cb1 = figure.colorbar(caxes)
            cb1.ax.tick_params(labelsize=14)
            ax1.xaxis.set_major_locator(MultipleLocator(1))
            ax1.set_xticklabels([''] + alphabets)
            ax1.yaxis.set_major_locator(MultipleLocator(1))
            ax1.set_yticklabels([''] + rowlist)

            matrixangle = np.angle(modes[2:(14*rows) + 2, i])
            matrixangle = np.reshape(matrixangle, (rows, 14))
            color_lims = np.percentile(matrixangle, [0, 100])
            ax2 = figure.add_subplot(212)
            ax2.set_title(f"Mode Angle - {i}: Frequency {modes[0, i]} Hz, Power {modes[1, i]}")
            caxes = ax2.matshow(matrixangle.tolist(), clim=color_lims, cmap='hsv', aspect=1)
            cb2 = figure.colorbar(caxes)
            cb2.ax.tick_params(labelsize=14)
            ax2.xaxis.set_major_locator(MultipleLocator(1))
            ax2.set_xticklabels([''] + alphabets)
            ax2.yaxis.set_major_locator(MultipleLocator(1))
            ax2.set_yticklabels([''] + rowlist)

            plots.append(plt)

        return plots


        




