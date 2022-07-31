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

class Datatodynamicssingle:
    def __init__(self, dataset, s0, s1, samplefreq=128, aug=True):
        self.aug = aug
        self.X1 = dataset[:, (s0):(s1)]
        self.samplefreq = samplefreq

        if self.aug:
            self.Xaug = self.prepare_matrix(self.X1)
        else:
            self.Xaug = self.X1

        self.Xaugp = self.Xaug[:, 1:]
        self.Xaug = self.Xaug[:, :-1]


    def prepare_matrix(self, X):
        # Set up DMD - reference https://www.sciencedirect.com/science/article/pii/S0165027015003829

        h = ((2 * X.shape[1]) // X.shape[0]) + 1
        length = X.shape[1] - h
        Xaug = X[:, 0:length]
        for k in range(1, h):
            Xaug = np.concatenate((Xaug, X[:, k:length + k]), axis=0)
        return Xaug

    def DMD(self, energy=False, plot=False, aspect=1):
        # compute SVD
        U, s, Vh = np.linalg.svd(self.Xaug, full_matrices=False)
        # find Atilde using the SVD and Xaugp
        Atilde = np.linalg.multi_dot([U.conj().T, self.Xaugp, Vh.conj().T]) * np.reciprocal(s)

        # scale Atilde to scale by energy
        if energy:
            Ahat = np.linalg.multi_dot([np.diag(np.power(s, -.5)), Atilde, np.diag(np.power(s, .5))])
        else:
            Ahat = Atilde

        # find eigenvalues and eigenvectors
        self.eigenvalues, self.eigenvectors = np.linalg.eig(Ahat)

        if energy:
            self.eigenvectors = np.diag(np.power(s, .5)).dot(self.eigenvectors)
        # find modes
        self.modes = (self.Xaugp.dot(Vh.conj().T) * np.reciprocal(s)).dot(self.eigenvectors)

        if plot:
            self.plot(np.absolute(self.modes), aspect=aspect, figsize=(20, 16), title='DMD Mode Heatmap (Mag)',
                      cmap='YlOrBr', halfticks=None)
            self.plot(np.angle(self.modes), aspect=aspect, figsize=(20, 16), title='DMD Mode Heatmap (Ang)',
                      cmap='hsv', halfticks=None)

            self.plot(np.absolute(np.diag(self.eigenvalues)), aspect=aspect, figsize=(20, 16), title='DMD Eigenvalue Heatmap (Mag)',
                      cmap='YlOrBr', halfticks=None)
            self.plot(np.angle(np.diag(self.eigenvalues)), aspect=aspect, figsize=(20, 16), title='DMD Eigenvalue Heatmap (Ang)',
                      cmap='hsv', halfticks=None)


    def reconstruct(self, plot=False, aspect=1):
        z = np.linalg.lstsq(self.modes, self.Xaug[:, 0], rcond=None,)[0]
        reconstruction = self.modes.dot(z)
        for i in range(1, self.Xaugp.shape[1]):
            reconstruction = np.column_stack((reconstruction, self.modes.dot(np.power(np.diag(self.eigenvalues), i)).dot(z)))

        if plot:
            color_lims = np.percentile(self.Xaugp, [5, 95])
            self.plot(self.Xaugp, aspect=aspect, figsize=(20, 16), title='Original Xaug\'', halfticks=None, clim=color_lims)
            self.plot(reconstruction.real, aspect=aspect, figsize=(20, 16), title='DMD Reconstruction', halfticks=None, clim=color_lims)
            self.plot(reconstruction.real - self.Xaugp.real, aspect=aspect, figsize=(20, 16), title='Error', halfticks=None, clim=color_lims)

        return reconstruction

    def DMDalt(self, plot=False, aspect=1):
        self.A = numpy.matmul(self.Xaugp, np.linalg.pinv(self.Xaug))

        if plot:
            self.plot(np.absolute(self.A), aspect=aspect, figsize=(20, 16), title='A Matrix (Mag)', halfticks=True, cmap='YlOrBr')
            self.plot(np.angle(self.A), aspect=aspect, figsize=(20, 16), title='A Matrix (Ang)', halfticks=True, cmap='hsv')

    def plot(self, matrix, aspect=1, figsize=(20, 16), title='', cmap='inferno', halfticks=None, clim=()):
        color_lims = np.percentile(matrix, [5, 95])
        if len(clim) > 0:
            color_lims = clim
        f = plt.figure(figsize=figsize)
        plt.matshow(matrix.tolist(), fignum=f.number, clim=color_lims, cmap=cmap, aspect=aspect)
        if halfticks:
            # Major ticks
            ax = plt.gca()
            ax.set_xticks(np.arange(-.5, matrix.shape[1] - .5, matrix.shape[1] / 2))
            ax.set_yticks(np.arange(-.5, matrix.shape[0] - .5, matrix.shape[0] / 2))
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize=14)
        plt.title(title)