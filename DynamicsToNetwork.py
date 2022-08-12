import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import patches
import os
import scipy.signal as sig
import cv2
from matplotlib.gridspec import GridSpec

class Dynamicstonetwork:
    def __init__(self, matrix, stim1, stim2, info1, info2):
        self.threshold = np.nanquantile(matrix, 0.90)
        self.matrix = matrix
        self.stim1 = stim1
        self.stim2 = stim2
        self.info1 = info1
        self.info2 = info2
        self.start1 = self.info1[0, 0]
        self.start2 = self.info2[0, 0]

        self.actiondict = {1: 'Planning',
                      2: 'Measuring',
                      3: 'Simulation',
                      10: 'Left',
                      0: 'Neutral',
                      12: 'Right',
                      21: '1',
                      22: '2',
                      23: '3'}

        self.action_dict = {0: 'Left',
                            1: 'Center',
                            2: 'Right'}

        self.mode1 = None
        self.mode2 = None
        self.lives1 = None
        self.lives2 = None
        self.times1 = 0
        self.action1 = None
        self.action2 = None
        self.score1 = None
        self.score2 = None
        self.times2 = 0

        self.info1_index = 2
        self.info2_index = 2
        self.total_choices1 = 0
        self.total_choices2 = 0
        self.right_choices1 = 0
        self.right_choices2 = 0
        self.left_choices1 = 0
        self.left_choices2 = 0
        self.center_choices1 = 0
        self.center_choices2 = 0

        self.all_info = [['', '', 0, 0, 0], ['', '', 0, 0, 0]]

    def get_data(self, index):

        if 1 <= self.stim1[1, index] <= 3 and int(self.stim1[0, index]) == 1:
            self.mode1 = self.actiondict[self.stim1[1, index]]

        elif 21 <= self.stim1[1, index] <= 23 and int(self.stim1[0, index]) == 1:
            self.lives1 = self.actiondict[self.stim1[1, index]]

        elif 10 <= self.stim1[1, index] <= 12 and int(self.stim1[0, index]) == 2:
            action = self.actiondict[self.stim1[1, index]]
            if action == self.action1 and self.times1 == 1:
                self.action1 = 'Neutral'
                self.times1 = 0
            else:
                self.action1 = action
                self.times1 = 1

        elif self.stim1[1, index] >= 25 and int(self.stim1[0, index]) == 1:
            self.score1 = str(self.stim1[1, index] - 100)

        elif int(self.stim1[0, index]) == 0:
            pass



        if 1 <= self.stim2[1, index] <= 3 and int(self.stim2[0, index]) == 1:
            self.mode2 = self.actiondict[self.stim2[1, index]]

        elif 21 <= self.stim2[1, index] <= 23 and int(self.stim2[0, index]) == 1:
            self.lives2 = self.actiondict[self.stim2[1, index]]

        elif 10 <= self.stim2[1, index] <= 12 and int(self.stim2[0, index]) == 2:
            action = self.actiondict[self.stim2[1, index]]
            if action == self.action2 and self.times2 == 1:
                self.action2 = 'Neutral'
                self.times2 = 0
            else:
                self.action2 = action
                self.times2 = 1

        elif self.stim2[1, index] >= 25 and int(self.stim2[0, index]) == 1:
            self.score2 = str(self.stim2[1, index] - 100)

        elif int(self.stim2[0, index]) == 0:
            pass



    def get_info(self, index):

        if round(index / 128, 1) == round((self.info1[self.info1_index, 0] - self.start1) - 4, 1):
            if self.info1[self.info1_index, 1] == 1:
                if self.info1_index + 2 < len(self.info1):
                    self.all_info[0][:2] = ['Planning', self.action_dict[self.info1[self.info1_index + 2, 2]]]
                else:
                    self.all_info[0][:2] = ['Planning', '']
            elif self.info1[self.info1_index, 1] == 2:
                if self.info1_index + 1 < len(self.info1):
                    self.all_info[0][:2] = ['Measuring', self.action_dict[self.info1[self.info1_index + 1, 2]]]
                else:
                    self.all_info[0][:2] = ['Measuring', '']
            elif self.info1[self.info1_index, 1] == 3:
                self.total_choices1 += 1
                if self.info1[self.info1_index, 2] == 0:
                    self.left_choices1 += 1
                    self.all_info[0][:2] = ['Simulation', 'Left']
                elif self.info1[self.info1_index, 2] == 1:
                    self.center_choices1 += 1
                    self.all_info[0][:2] = ['Simulation', 'Center']
                elif self.info1[self.info1_index, 2] == 2:
                    self.right_choices1 += 1
                    self.all_info[0][:2] = ['Simulation', 'Right']

            self.info1_index += 1

            self.all_info[0][2:5] = [round(self.left_choices1/self.total_choices1, 3),
                                     round(self.center_choices1/self.total_choices1, 3),
                                     round(self.right_choices1/self.total_choices1, 3)]

        if round(index / 128, 1) == round((self.info2[self.info2_index, 0] - self.start2) - 4, 1):
            if self.info2[self.info2_index, 1] == 1:
                if self.info2_index + 2 < len(self.info2):
                    self.all_info[1][:2] = ['Planning', self.action_dict[self.info2[self.info2_index + 2, 2]]]
                else:
                    self.all_info[1][:2] = ['Planning', '']
            elif self.info2[self.info2_index, 1] == 2:
                if self.info2_index + 1 < len(self.info2):
                    self.all_info[1][:2] = ['Measuring', self.action_dict[self.info2[self.info2_index + 1, 2]]]
                else:
                    self.all_info[1][:2] = ['Measuring', '']
            elif self.info2[self.info2_index, 1] == 3:
                self.total_choices2 += 1
                if self.info2[self.info2_index, 2] == 0:
                    self.left_choices2 += 1
                    self.all_info[1][:2] = ['Simulation', 'Left']
                elif self.info2[self.info2_index, 2] == 1:
                    self.center_choices2 += 1
                    self.all_info[1][:2] = ['Simulation', 'Center']
                elif self.info2[self.info2_index, 2] == 2:
                    self.right_choices2 += 1
                    self.all_info[1][:2] = ['Simulation', 'Right']

            self.info2_index += 1

            self.all_info[1][2:5] = [round(self.left_choices2 / self.total_choices2, 3),
                                     round(self.center_choices2 / self.total_choices2, 3),
                                     round(self.right_choices2 / self.total_choices2, 3)]

    def draw_networks(self):
        self.mode1 = ''
        self.mode2 = ''
        self.lives1 = ''
        self.lives2 = ''
        self.action1 = ''
        self.action2 = ''
        self.score1 = ''
        self.score2 = ''
        self.times1 = 0
        self.times2 = 0

        self.info1_index = 2
        self.info2_index = 2
        self.total_choices1 = 0
        self.total_choices2 = 0
        self.right_choices1 = 0
        self.right_choices2 = 0
        self.left_choices1 = 0
        self.left_choices2 = 0
        self.center_choices1 = 0
        self.center_choices2 = 0

        self.all_info = [['', '', 0, 0, 0], ['', '', 0, 0, 0]]


        for index in range(self.matrix.shape[0]):
            self.get_data(index)
            self.get_info(index)
            self.create_network(index, self.matrix[index],
                                [self.mode1, self.mode2],
                                [self.lives1, self.lives2],
                                [self.action1, self.action2],
                                [self.score1, self.score2],
                                self.all_info)

    def create_network(self, index, matrix, modes, lives, actions, scores, pinfo):
        # plot------------------------------
        # create objects
        fig = plt.figure(figsize=(16, 9))
        gs = GridSpec(5, 4, figure=fig)

        # create sub plots as grid
        ax1 = fig.add_subplot(gs[2:, :])
        # ax2 = fig.add_subplot(gs[0, 0])
        ax3 = fig.add_subplot(gs[0, 1])
        # ax4 = fig.add_subplot(gs[0, 2])
        ax5 = fig.add_subplot(gs[0, 3])


        for i in range(2):
            skew = 8 * i
            xy_center = (skew + 4, 3)
            radius = 2

            # left ear
            circle = patches.Ellipse((skew + 2, 3), width=0.6, height=1.0, angle=0, edgecolor="k", facecolor="w", zorder=0)
            ax1.add_patch(circle)
            # right ear
            circle = patches.Ellipse((skew + 6, 3), width=0.6, height=1.0, angle=0, edgecolor="k", facecolor="w", zorder=0)
            ax1.add_patch(circle)
            # nose
            xy = [[skew + 3.6, 4.6], [skew + 4, 5.3], [skew + 4.4, 4.6]]
            polygon = patches.Polygon(xy=xy, edgecolor="k", facecolor="w", zorder=0)
            ax1.add_patch(polygon)
            # head
            head = patches.Circle(xy_center, radius=radius, edgecolor="k", facecolor="w", zorder=0)
            ax1.add_patch(head)
            # prevent squeeze
            squeeze = patches.Circle((15.9, 5.3), radius=0.1, edgecolor="k", facecolor="w", zorder=0)
            ax1.add_patch(squeeze)
            squeeze = patches.Circle((0.1, 0.1), radius=0.1, edgecolor="k", facecolor="w", zorder=0)
            ax1.add_patch(squeeze)



            ax1.text(1 + (8*i), 8.75, 'Frame: ' + str(index))
            ax1.text(1 + (8*i), 8.5, 'Phase: ' + modes[i])
            ax1.text(1 + (8*i), 8.25, 'Lives: ' + lives[i])
            ax1.text(1 + (8*i), 8, 'Input: ' + actions[i])
            ax1.text(1 + (8*i), 7.75, 'Score: ' + scores[i])

            ax1.text(1 + (8 * i), 7.25, 'Phase: ' + pinfo[i][0])
            ax1.text(1 + (8 * i), 7, 'Action: ' + pinfo[i][1])
            ax1.text(1 + (8 * i), 6.75, 'Left Ratio: ' + str(pinfo[i][2]))
            ax1.text(1 + (8 * i), 6.5, 'Center Ratio: ' + str(pinfo[i][3]))
            ax1.text(1 + (8 * i), 6.25, 'Right Ratio: ' + str(pinfo[i][4]))
            ax1.axis('equal')



        skew = 8
        # nodes
        DG = nx.DiGraph()
        nodes_list = ['1-AF3', '1-F7', '1-F3', '1-FC5', '1-T7', '1-P7', '1-O1',
                      '1-O2', '1-P8', '1-T8', '1-FC6', '1-F4', '1-F8', '1-AF4',
                      '2-AF3', '2-F7', '2-F3', '2-FC5', '2-T7', '2-P7', '2-O1',
                      '2-O2', '2-P8', '2-T8', '2-FC6', '2-F4', '2-F8', '2-AF4',
                      ]

        DG.add_nodes_from(nodes_list)
        pos = {'1-AF3': [3.4, 4.8], '1-F7': [2.3, 4], '1-F3': [3.1, 4.3], '1-FC5': [2.4, 3.5], '1-T7': [2, 3], '1-P7': [2.3, 2],
               '1-O1': [3.4, 1.4], '1-O2': [4.6, 1.4], '1-P8': [5.7, 2], '1-T8': [6, 3], '1-FC6': [5.6, 3.5], '1-F4': [4.9, 4.3],
               '1-F8': [5.7, 4], '1-AF4': [4.6, 4.8],
                '2-AF3': [skew + 3.4, 4.8], '2-F7': [skew + 2.3, 4], '2-F3': [skew + 3.1, 4.3], '2-FC5': [skew + 2.4, 3.5], '2-T7': [skew + 2, 3], '2-P7': [skew + 2.3, 2],
               '2-O1': [skew + 3.4, 1.4], '2-O2': [skew + 4.6, 1.4], '2-P8': [skew + 5.7, 2], '2-T8': [skew + 6, 3], '2-FC6': [skew + 5.6, 3.5], '2-F4': [skew + 4.9, 4.3],
               '2-F8': [skew + 5.7, 4], '2-AF4': [skew + 4.6, 4.8]}

        m_to_norm = matrix - self.threshold
        norm = np.linalg.norm(m_to_norm)
        normalized = (m_to_norm) / norm
        # edges
        for de in range(len(nodes_list)):
            for a in range(len(nodes_list)):
                if matrix[a, de] > self.threshold:
                    DG.add_edge(nodes_list[de], nodes_list[a], weight=(10 * normalized[a, de]))

        # hot nodes
        color_map = []
        for node in DG:
            degree = DG.degree(node)
            if degree < 3:
                color_map.append('yellow')
            elif 3 <= degree <= 6:
                color_map.append('orange')
            else:
                color_map.append('r')

        nx.draw_networkx(DG, pos=pos, with_labels=True, node_color=color_map, edge_color='grey', ax=ax1)
        ax1.text(1, 6, 'Number of Edges: ' + str(DG.number_of_edges()))
        ax1.text(4, 6, 'Average Clustering: ' + str(round(nx.average_clustering(DG), 3)))
        ax1.text(7, 6, 'Transitivity: ' + str(round(nx.transitivity(DG), 3)))
        # plt.text(10, 6, 'Eccentricity: ' + str(nx.eccentricity(DG)))
        # print(nx.clustering(DG))

        ax3.set_title('Center Probability')
        ax3.set_xlim(left=0, right=1)
        ax3.set_ylim(bottom=0, top=1)
        ax3.set_aspect('equal')
        ax3.plot([pinfo[0][3]], [pinfo[1][3]], marker="o", markersize=5)
        ax3.set(xlabel="Player 1", ylabel="Player 2")

        ax5.set_title('Center Probability')
        ax5.set_xlim(left=0, right=1)
        ax5.set_ylim(bottom=0, top=1)
        ax5.set_aspect('equal')
        ax5.plot([pinfo[0][3]], [pinfo[1][3]], marker="o", markersize=5)
        ax5.set(xlabel="Player 1", ylabel="Player 2")

        return plt

    def export(self, export_name, downsp=1):
        # make dir
        new_dir = f'{os.getcwd()}\\DynamicsNetExports\\{export_name}'
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
            os.makedirs(f'{new_dir}\\Chuncks')
        else:
            if not os.path.exists(f'{new_dir}\\Chuncks'):
                os.makedirs(f'{new_dir}\\Chuncks')

        self.mode1 = ''
        self.mode2 = ''
        self.lives1 = ''
        self.lives2 = ''
        self.action1 = ''
        self.action2 = ''
        self.score1 = ''
        self.score2 = ''
        self.times1 = 0
        self.times2 = 0

        self.info1_index = 2
        self.info2_index = 2
        self.total_choices1 = 0
        self.total_choices2 = 0
        self.right_choices1 = 0
        self.right_choices2 = 0
        self.left_choices1 = 0
        self.left_choices2 = 0
        self.center_choices1 = 0
        self.center_choices2 = 0

        self.all_info = [['', '', 0, 0, 0], ['', '', 0, 0, 0]]

        for index in range(self.matrix.shape[0]):
            # print(ch_data.type)
            self.get_data(index)
            self.get_info(index)
            if index % downsp == 0:
                plt = self.create_network(index, self.matrix[index],
                                    [self.mode1, self.mode2],
                                    [self.lives1, self.lives2],
                                    [self.action1, self.action2],
                                    [self.score1, self.score2],
                                    self.all_info)
                pngname = f'{new_dir}\\Chuncks\\{str(index)}.png'
                plt.savefig(pngname, format="PNG", dpi=300)
                plt.close()

        # from PIL import Image
        #
        # frames = []
        #
        # for i in range(len(self.matrix)):
        #     file = f'{new_dir}\\Chuncks\\chunck_{str(i)}.png'
        #     newFrame = Image.open(file)
        #     frames.append(newFrame)
        #
        # Save into a GIF file that loops forever
        # saveFile = f'{new_dir}\\Net_of_{export_name}.gif'
        # frames[0].save(saveFile, format='GIF', append_images=frames[1:],
        #                save_all=True, duration=300, loop=0)

        image_folder = f'{new_dir}\\Chuncks'
        video_name = f'{new_dir}\\Net_of_{export_name}.avi'

        images = []
        for i in range(self.matrix.shape[0]):
            if i % downsp == 0:
                images.append(f'{image_folder}\\{str(i)}.png')
        frame = cv2.imread(images[0])
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 128//downsp, (width, height))

        for image in images:
            video.write(cv2.imread(image))

        cv2.destroyAllWindows()
        video.release()