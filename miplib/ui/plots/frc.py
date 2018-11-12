import os

import matplotlib.pyplot as plt
plt.style.use("seaborn-paper")
from matplotlib import rc
from matplotlib.font_manager import FontProperties
from miplib.data.containers.fourier_correlation_data import FourierCorrelationData, FourierCorrelationDataCollection
from miplib.processing.converters import degrees_to_radians
import numpy as np
import miplib.processing.ndarray as arrayops


def plot_resolution_curves(data_to_plot, path, labels=None, to_file=False, size=(3,3), coerce_ticks=False):
    assert isinstance(data_to_plot, FourierCorrelationDataCollection)

    angles = list()
    datasets = list()

    # Sort datasets by angle.
    for dataset in data_to_plot:
        angles.append((int(dataset[0])))
        datasets.append(dataset[1])

    angles, datasets = zip(*sorted(zip(angles, datasets)))

    # Setup labels
    if labels is not None:
        assert len(labels) == len(angles)
    else:
        labels = angles

    # with sns.color_palette("husl", 8):

    fig, ax = plt.subplots(figsize=size)

    # plot threshold
    dataset = datasets[0]
    y = dataset.resolution["threshold"]
    x = dataset.correlation["frequency"]
    if x[-1] < 1.0:
        x = np.append(x, 1.0)
        y = np.append(y, y[-1])

    ax.plot(x, y, linestyle='--', color='#b5b5b3')

    x_axis = arrayops.safe_divide(np.linspace(0.0, 1.0, num=len(ax.get_xticklabels())),
                                  2 * dataset.resolution["spacing"])

    if coerce_ticks is True:
        x_labels = map(lambda n: '%d' % n, x_axis)
    else:
        x_labels = map(lambda n: '%.1f' % n, x_axis)

    ax.set_xticklabels(x_labels)

    if not to_file:
        xlabel = 'Frequency (1/um)'
        ylabel = 'Correlation'
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    for idx, dataset in enumerate(datasets):

        ax.set_ylim([0, 1.2])

        # Plot calculated FRC values as xy scatter.
        y = dataset.correlation["curve-fit"]
        x = dataset.correlation["frequency"]

        ax.plot(x, y, label=labels[idx])

    if to_file:
        plt.savefig(path, dpi=1200, bbox_inches='tight', pad_inches=0, transparent=True)

    return fig

class FourierDataPlotter(object):
    def __init__(self, data, path=None):
        assert isinstance(data, FourierCorrelationDataCollection)

        self.data = data

        if len(self.data) < 3:
            self._columns = len(self.data)
        else:
            self._columns = 3

        if len(self.data) % self._columns == 0:
            self._rows = len(self.data) / self._columns
        else:
            self._rows = len(self.data) / self._columns + 1

        if path is not None:
            assert os.path.isdir(path)
            self.path = path

    def plot_all(self, save_fig=False, custom_titles = None, show = True):

        axescolor = '#f6f6f6'

        size = (6, self._rows*2) if save_fig else (12, self._rows * 4)

        fig, plots = plt.subplots(self._rows, self._columns,
                                  figsize=size)
        # rect = fig.patch
        # rect.set_facecolor('white')

        fig.tight_layout(pad=0.4, w_pad=2, h_pad=6)

        angles = list()
        datasets = list()

        # Sort datasets by angle.
        for dataset in self.data:
            angles.append((int(dataset[0])))
            datasets.append(dataset[1])

        angles, datasets = zip(*sorted(zip(angles, datasets)))

        if custom_titles is None:
            titles = list("FRC @ angle %i" % angle for angle in angles)
        else:
            assert len(custom_titles) == len(angles)
            titles = custom_titles

        # Make subplots
        for title, dataset, plot in zip(titles, datasets, plots.flatten()):

            self.__make_frc_subplot(plot, dataset, title)

        if save_fig:
            file_name = os.path.join(self.path, "all_frc_curves.eps")
            plt.savefig(file_name, dpi=1200)

        if show:
            plt.show()

    def plot_all_to_files(self, custom_titles=None, size=(3.3, 3), header=False):
        assert self.path is not None

        fig, plot = plt.subplots(1, 1, figsize=size, tight_layout=True)
        #plot.set(aspect='equal')


        angles = list()
        datasets = list()

        # Sort datasets by angle.
        for dataset in self.data:
            angles.append((int(dataset[0])))
            datasets.append(dataset[1])

        angles, datasets = zip(*sorted(zip(angles, datasets)))

        if custom_titles is None:
            titles = list("FRC @ angle %i" % angle for angle in angles)
        else:
            assert len(custom_titles) == len(angles)
            titles = custom_titles

        # Make subplots
        for title, dataset in zip(titles, datasets):
            self.__make_printable_frc_subplot(plot, dataset, title=(title if header else None))
            file_name = os.path.join(self.path, "{}.eps".format(title))
            plt.savefig(file_name, dpi=1200)
            plt.cla()

    def plot_one(self, angle):

        plt.figure(figsize=(5, 4))
        ax = plt.subplot(111)

        self.__make_frc_subplot(ax, self.data[int(angle)], "FRC at angle %s" % str(angle))

        plt.show()

    def plot_one_to_file(self, angle, filename, title=None, size = (2,2), coerce_ticks=True):
        plt.figure(figsize=size)
        ax = plt.subplot(111)

        self.__make_printable_frc_subplot(ax, self.data[int(angle)], title, coerce_ticks=coerce_ticks)
        file_name = os.path.join(self.path, "{}.eps".format(filename))

        plt.savefig(file_name, dpi=1200, bbox_inches='tight', pad_inches=0, transparent=True)



    def plot_polar(self):
        """
        Show the resolution as a 2D polar plot in which the resolution values are plotted
        as a function of rotatino angle.
        """

        angles = list()
        radii = list()

        for dataset in self.data:
            angles.append(degrees_to_radians(float(dataset[0])))
            radii.append(dataset[1].resolution["resolution"])

        angles, radii = zip(*sorted(zip(angles, radii)))
        angles = list(angles)
        radii = list(radii)
        angles.append(angles[0])
        radii.append(radii[0])

        radii_norm = list(i/max(radii) for i in radii)
        plt.figure(figsize=(4,4))
        ax = plt.subplot(111, projection="polar")
        ax.plot(angles, radii_norm, color='#61a2da')
        ax.set_rmax(1.2)
        r_ticks = np.linspace(0.1, 1.0, 5)
        r_ticks_scale = r_ticks * max(radii)

        x_labels = map(lambda n: '%.2f' % n, r_ticks_scale)

        ax.set_rticks(r_ticks)
        ax.set_yticklabels(x_labels)
        ax.set_rlabel_position(-80)  # get radial labels away from plotted line
        #ax.grid(True)

        #ax.set_title("The image resolution as a function of rotation angle")

        #ax.set_xlabel("XY")
        #ax.set_ylabel("Z")

    def plot_polar_to_file(self, filename, size=(2,2)):
        """
        Show the resolution as a 2D polar plot in which the resolution values are plotted
        as a function of rotatino angle.
        """

        angles = list()
        radii = list()

        for dataset in self.data:
            angles.append(degrees_to_radians(float(dataset[0])))
            radii.append(dataset[1].resolution["resolution"])

        angles, radii = zip(*sorted(zip(angles, radii)))
        angles = list(angles)
        radii = list(radii)
        angles.append(angles[0])
        radii.append(radii[0])

        radii_norm = list(i / max(radii) for i in radii)
        plt.figure(figsize=size)
        ax = plt.subplot(111, projection="polar")
        ax.plot(angles, radii_norm, color='#61a2da')
        ax.set_rmax(1.2)
        r_ticks = np.linspace(0.1, 1.0, 5)
        r_ticks_scale = r_ticks * max(radii)

        print r_ticks_scale
        print max(radii)

        x_labels = map(lambda n: '%.2f' % n, r_ticks_scale)

        print x_labels
        ax.set_rticks(r_ticks)
        ax.set_yticklabels(x_labels)
        ax.set_rlabel_position(-80)  # get radial labels away from plotted line
        # ax.grid(True)

        # ax.set_title("The image resolution as a function of rotation angle")

        # ax.set_xlabel("XY")
        # ax.set_ylabel("Z")

        file_name = os.path.join(self.path, "{}.eps".format(filename))

        plt.savefig(file_name, dpi=1200, bbox_inches='tight', pad_inches=0, transparent=True)

    @staticmethod
    def __make_frc_subplot(ax, frc, title):
        """
        Creates a plot of the FRC curves in the curve_list. Single or multiple vurves can
        be plotted.
        """
        assert isinstance(frc, FourierCorrelationData)

        # # Font setting
        # font0 = FontProperties()
        # font1 = font0.copy()
        # font1.set_size('medium')
        # font = font1.copy()
        # font.set_family('sans')
        # rc('text', usetex=True)

        # Enable grid
        gridLineWidth = 0.2
        #ax.yaxis.grid(True, linewidth=gridLineWidth, linestyle='-', color='0.05')

        # Axis labelling
        xlabel = 'Frequency (1/um)'
        ylabel = 'Correlation'
        #ax.set_xlabel(xlabel, fontsize=12, position=(0.5, -0.2))
        #ax.set_ylabel(ylabel, fontsize=12, position=(0.5, 0.5))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        ax.set_ylim([0, 1.2])

        # Title
        ax.set_title(title)

        # Plot calculated FRC values as xy scatter.
        y = frc.correlation["correlation"]
        x = frc.correlation["frequency"]
        ax.plot(x, y, '^', markersize=6, color='#b5b5b3',
                 label='FRC')

        # Plot polynomial fit as a line plot over the FRC scatter
        y = frc.correlation["curve-fit"]
        ax.plot(x, y, linewidth=3, color='#61a2da',
                 label='Least-squares fit')

        # Plot the resolution threshold curve
        y = frc.resolution["threshold"]
        res_crit = frc.resolution["criterion"]
        if res_crit == 'one-bit':
            label = 'One-bit curve'
        elif res_crit == 'half-bit':
            label = 'Half-bit curve'
        elif res_crit == 'fixed':
            label = 'y = %f' % y[0]
        else:
            label = "Threshold"

        if x[-1] < 1.0:
            x = np.append(x, 1.0)
            y = np.append(y, y[-1])

        ax.plot(x, y, color='#d77186',
                 label=label, lw=2, linestyle='--')

        # Plot resolution point
        y0 = frc.resolution["resolution-point"][0]
        x0 = frc.resolution["resolution-point"][1]

        ax.plot(x0, y0, 'ro', markersize=8, label='Resolution point', color='#D75725')

        verts = [(x0, 0), (x0, y0)]
        xs, ys = zip(*verts)

        ax.plot(xs, ys, 'x--', lw=3, color='#D75725', ms=10)
        #ax.text(x0, y0 + 0.10, 'RESOL-FREQ', fontsize=12)

        resolution = "The resolution is {} um.".format(
            frc.resolution["resolution"])
        ax.text(0.5, -0.3, resolution, ha="center", fontsize=12)

        x_axis = arrayops.safe_divide(np.linspace(0.0, 1.0, num=len(ax.get_xticklabels())),
                                      2*frc.resolution["spacing"])

        x_labels = map(lambda n: '%.1f' % n, x_axis)

        ax.set_xticklabels(x_labels)

        # Add legend
        #ax.legend()

    @staticmethod
    def __make_printable_frc_subplot(ax, frc, title=None, coerce_ticks=True):
        """
        Creates a plot of the FRC curves in the curve_list. Single or multiple vurves can
        be plotted.
        """
        assert isinstance(frc, FourierCorrelationData)

        # # Font setting
        # font0 = FontProperties()
        # font1 = font0.copy()
        # font1.set_size('medium')
        # font = font1.copy()
        # font.set_family('sans')
        #rc('text', usetex=True)

        # Enable grid
        gridLineWidth = 0.2
        # ax.yaxis.grid(True, linewidth=gridLineWidth, linestyle='-', color='0.05')

        # Marker setup
        colorArray = ['blue', 'green', 'red', 'orange', 'brown', 'black', 'violet', 'pink']
        marker_array = ['^', 's', 'o', 'd', '1', 'v', '*', 'p']

        # Axis labelling
        xlabel = 'Frequency'
        ylabel = 'Correlation'
        # ax.set_xlabel(xlabel, fontsize=12, position=(0.5, -0.2))
        # ax.set_ylabel(ylabel, fontsize=12, position=(0.5, 0.5))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        ax.set_ylim([0, 1.2])

        # Title
        if title is not None:
            ax.set_title(title)

        # Plot calculated FRC values as xy scatter.
        y = frc.correlation["correlation"]
        x = frc.correlation["frequency"]
        ax.plot(x, y, marker_array[0], color='#b5b5b3',
                label='FRC')

        # Plot polynomial fit as a line plot over the FRC scatter
        y = frc.correlation["curve-fit"]
        ax.plot(x, y, color='#61a2da',
                label='Least-squares fit')

        # Plot the resolution threshold curve
        y = frc.resolution["threshold"]
        res_crit = frc.resolution["criterion"]
        if res_crit == 'one-bit':
            label = 'One-bit curve'
        elif res_crit == 'half-bit':
            label = 'Half-bit curve'
        elif res_crit == 'fixed':
            label = 'y = %f' % y[0]
        else:
            label = "Threshold"

        if x[-1] < 1.0:
            x = np.append(x, 1.0)
            y = np.append(y, y[-1])

        ax.plot(x, y, color='#d77186',
                label=label, linestyle='--')

        # Plot resolution point
        y0 = frc.resolution["resolution-point"][0]
        x0 = frc.resolution["resolution-point"][1]

        ax.plot(x0, y0, 'ro', label='Resolution point', color='#D75725')

        verts = [(x0, 0), (x0, y0)]
        xs, ys = zip(*verts)

        ax.plot(xs, ys, 'x--', color='#D75725', ms=10)

        x_axis = arrayops.safe_divide(np.linspace(0.0, 1.0, num=len(ax.get_xticklabels())),
                                      2 * frc.resolution["spacing"])

        if coerce_ticks is True:
            x_labels = map(lambda n: '%d' % n, x_axis)
        else:
            x_labels = map(lambda n: '%.1f' % n, x_axis)

        ax.set_xticklabels(x_labels)





