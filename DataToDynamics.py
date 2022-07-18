import mne_connectivity
import mne
import numpy
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import patches
import os
import scipy.signal as sig
from pydmd import DMD
from pydmd import MrDMD
from pydmd import SpDMD
from pydmd import FbDMD
import scipy.integrate

class Datatodynamics:
    def __init__(self, dataset1, dataset2, t0, t1, samplefreq=128):
        self.rawdataset1 = dataset1[:, (t0*samplefreq):(t1*samplefreq)]
        self.rawdataset2 = dataset2[:, (t0*samplefreq):(t1*samplefreq)]

        prepd1 = self.prepare_matrix(self.rawdataset1)
        prepd2 = self.prepare_matrix(self.rawdataset2)

        self.X = self.combine_data(prepd1, prepd2)

        self.atilde = self.DMD(self.X)

    def prepare_matrix(self, X):
        # Set up DMD - reference https://www.sciencedirect.com/science/article/pii/S0165027015003829

        print(X.shape)
        h = (2 * X.shape[1]) // X.shape[0]
        length = X.shape[1] - h
        Xaug = X[:, 0:length]
        for k in range(1, h):
            Xaug = np.concatenate((Xaug, X[:, k:length + k]), axis=0)
        print(Xaug.shape)
        return Xaug

    def combine_data(self, X1, X2):
        return np.concatenate((X1, X2), axis=0)

    def DMD(self, X, svd=-1):
        self.dmd = DMD(svd_rank=svd)
        self.dmd.fit(X)
        return self.dmd.atilde

    def plot(self):
        color_lims = np.percentile(self.atilde, [5, 95])
        f = plt.figure(figsize=(20, 16))
        plt.matshow(self.atilde.real.tolist(), fignum=f.number, clim=color_lims)
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize=14)
        plt.title('Correlation matrix')

        fig, axs = plt.subplots(3, figsize=(18, 16))
        fig.suptitle('X, Xhat, and error')
        color_lims = np.percentile(self.X[0:self.rawdataset1.shape[1]], [5, 95])
        f = axs[0].matshow(self.X[0:self.rawdataset1.shape[1]].tolist(), clim=color_lims, aspect=10)
        cb = fig.colorbar(f, ax=axs[0])
        cb.ax.tick_params(labelsize=14)
        matrix = np.array(self.dmd.reconstructed_data.real[0:self.rawdataset1.shape[1]])
        f = axs[1].matshow(matrix[0:self.rawdataset1.shape[1]].tolist(), clim=color_lims, aspect=10)
        cb = fig.colorbar(f, ax=axs[1])
        cb.ax.tick_params(labelsize=14)
        diff = self.X[0:self.rawdataset1.shape[1]] - matrix
        f = axs[2].matshow(diff.tolist(), clim=color_lims, aspect=10)
        cb = fig.colorbar(f, ax=axs[2])
        cb.ax.tick_params(labelsize=14)
        self.dmd.plot_eigs(show_axes=True, show_unit_circle=True, figsize=(8, 8))

