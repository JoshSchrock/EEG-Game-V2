import numpy
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import patches
import os
import scipy.signal as sig

class Dynamicstonetwork:
    def __init__(self, matrix):
        self.matrix = matrix.tolist()
        self.threshold = np.nanquantile(self.matrix, 0.8)

    def draw_networks(self):
        for index, matrix in enumerate(self.matrix):
            self.create_network(index, matrix)

    def create_network(self, index, matrix):
        # plot------------------------------
        fig, ax = plt.subplots(figsize=(16, 8))

        for i in range(2):
            skew = 8 * i
            xy_center = [skew + 2, 2]
            radius = 2

            # left ear
            circle = patches.Ellipse(xy=[skew + 0, 2], width=0.4, height=1.0, angle=0, edgecolor="k", facecolor="w", zorder=0)
            ax.add_patch(circle)
            # right ear
            circle = patches.Ellipse(xy=[skew + 4, 2], width=0.4, height=1.0, angle=0, edgecolor="k", facecolor="w", zorder=0)
            ax.add_patch(circle)
            # nose
            xy = [[skew + 1.6, 3.6], [skew + 2, 4.3], [skew + 2.4, 3.6]]
            polygon = patches.Polygon(xy=xy, edgecolor="k", facecolor="w", zorder=0)
            ax.add_patch(polygon)
            # head
            circle = patches.Circle(xy=xy_center, radius=radius, edgecolor="k", facecolor="w", zorder=0)
            ax.add_patch(circle)

        plt.text(1, 1, str(index))

        skew = 8
        # nodes
        G = nx.Graph()
        nodes_list = ['1-AF3', '1-F7', '1-F3', '1-FC5', '1-T7', '1-P7', '1-O1',
                      '1-O2', '1-P8', '1-T8', '1-FC6', '1-F4', '1-F8', '1-AF4',
                      '2-AF3', '2-F7', '2-F3', '2-FC5', '2-T7', '2-P7', '2-O1',
                      '2-O2', '2-P8', '2-T8', '2-FC6', '2-F4', '2-F8', '2-AF4',
                      ]

        G.add_nodes_from(nodes_list)
        pos = {'1-AF3': [1.5, 3.8], '1-F7': [0.4, 3], '1-F3': [1.2, 3.3], '1-FC5': [0.5, 2.5], '1-T7': [0, 2], '1-P7': [0.4, 1],
               '1-O1': [1.5, 0.4], '1-O2': [2.5, 0.4], '1-P8': [3.6, 1], '1-T8': [4, 2], '1-FC6': [3.5, 2.5], '1-F4': [2.8, 3.3],
               '1-F8': [3.6, 3], '1-AF4': [2.5, 3.8],
                '2-AF3': [skew + 1.5, 3.8], '2-F7': [skew + 0.4, 3], '2-F3': [skew + 1.2, 3.3], '2-FC5': [skew + 0.5, 2.5], '2-T7': [skew + 0, 2], '2-P7': [skew + 0.4, 1],
               '2-O1': [skew + 1.5, 0.4], '2-O2': [skew + 2.5, 0.4], '2-P8': [skew + 3.6, 1], '2-T8': [skew + 4, 2], '2-FC6': [skew + 3.5, 2.5], '2-F4': [skew + 2.8, 3.3],
               '2-F8': [skew + 3.6, 3], '2-AF4': [skew + 2.5, 3.8]}

        # edges
        for i in range(len(nodes_list)):
            for j in range(len(nodes_list)):
                if i < j:
                    edge = [(nodes_list[i], nodes_list[j])]
                    if matrix[i][j] > self.threshold:
                        G.add_edges_from(edge)
                        nx.draw_networkx_edges(G, pos=pos, edgelist=edge,
                                               width=min(10, (1000 ** (matrix[i][j] - self.threshold))), edge_color='grey')

        # hot nodes
        color_map = []
        for node in G:
            degree = G.degree(node)
            if degree < 3:
                color_map.append('yellow')
            elif 3 <= degree <= 6:
                color_map.append('orange')
            else:
                color_map.append('r')

        nx.draw(G, pos=pos, with_labels=True, node_color=color_map, edge_color='grey')

        return plt

    def export(self, export_name):
        # make dir
        new_dir = f'{os.getcwd()}\\DynamicsNetExports\\{export_name}'
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
            os.makedirs(f'{new_dir}\\Chuncks')
        else:
            if not os.path.exists(f'{new_dir}\\Chuncks'):
                os.makedirs(f'{new_dir}\\Chuncks')

        for index, matrix in enumerate(self.matrix):
            # print(ch_data.type)
            plt = self.create_network(index, matrix)
            pngname = f'{new_dir}\\Chuncks\\chunck_{str(index)}.png'
            plt.savefig(pngname, format="PNG", bbox_inches='tight')

        from PIL import Image

        frames = []

        for i in range(len(self.matrix)):
            file = f'{new_dir}\\Chuncks\\chunck_{str(i)}.png'
            newFrame = Image.open(file)
            frames.append(newFrame)

        # Save into a GIF file that loops forever
        saveFile = f'{new_dir}\\Net_of_{export_name}.gif'
        frames[0].save(saveFile, format='GIF', append_images=frames[1:],
                       save_all=True, duration=300, loop=0)