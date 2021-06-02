import cv2
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import matplotlib.widgets as wdt
import numpy as np
import os
import tkinter
from tkinter import filedialog as tkFileDialog


class ColorPicker():

    def __init__(self):

        # Image file path
        self.file_path = None

        # RGB image
        # OpenCV values - R-G-B = [0-255]
        self.image_rgb = None

        # HSV image
        # OpenCV values - H = [0-180] - S = [0-255] - V = [0-255]
        self.image_hsv = None

        # Picked pixels HSV values
        # OpenCV values - H = [0-180] - S = [0-255] - V = [0-255]
        self.pxs_hsv = None

        # Figure

        fig = plt.figure()
        fig.canvas.mpl_connect("button_press_event", self.on_click_figure)

        gs_buttons = GridSpec(10, 1, left=0.01, right=0.10)
        gs_charts = GridSpec(1, 2, left=0.15, right=0.99)

        # Charts

        self.ax_image_rgb = fig.add_subplot(gs_charts[:,0])
        self.show_image_rgb()

        self.ax_hsv = fig.add_subplot(gs_charts[:,1])    
        self.show_hsv_plot()

        # Buttons

        ax_btn_import = fig.add_subplot(gs_buttons[0,:])

        btn_import_file = wdt.Button(ax_btn_import, "Import File")
        btn_import_file.on_clicked(self.on_click_btn_import_file)

        ax_btn_reset = fig.add_subplot(gs_buttons[1,:])

        btn_reset = wdt.Button(ax_btn_reset, "Reset")
        btn_reset.on_clicked(self.on_click_btn_reset)


        # Show figure

        plt.show()


    # ----- CALLBACKS ----- #

    def on_click_btn_import_file(self, e):

        root = tkinter.Tk().withdraw()
        self.file_path = tkFileDialog.askopenfilename()

        # BRG image
        # OpenCV values - B-R-G = [0-255]
        image_bgr = cv2.imread(self.file_path)

        # RGB image
        # OpenCV values - R-G-B = [0-255]
        self.image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) # 

        # HSV image
        # OpenCV values - H = [0-180] - S = [0-255] - V = [0-255]
        self.image_hsv = cv2.cvtColor(self.image_rgb, cv2.COLOR_RGB2HSV)

        self.show_image_rgb()


    def on_click_btn_reset(self, e):

        self.reset_plots()


    def on_click_figure(self, e):

        # Check if chart clicked on was the RGB image
        if e.inaxes == self.ax_image_rgb:

            # Index of pixels just clicked on
            # 
            # Pixel coordinate frame
            #    -> origing = (top, left)
            #    -> axis 1 = down (rows), axis 2 = right (cols)
            #    -> int
            # Data coordinate frame (for image)
            #    -> origin = (top, left)
            #    -> axis 1 = right (cols), axis 2 = down (rows)
            #    -> float
            
            px_row = int(e.ydata)
            px_col = int(e.xdata)

            px = np.array([px_row, px_col])

            # HSV values of pixel
            
            px_hsv = np.array(self.image_hsv[px_row, px_col, :], dtype=np.int)

            # Add pixel value to list of all pixel values

            if self.pxs_hsv is None:
                
                self.pxs_hsv = np.array([px_hsv])
               
            else:
                self.pxs_hsv = np.append(self.pxs_hsv, [px_hsv], axis=0) 

            self.show_hsv_plot()


    # ----- DRAWING METHODS ----- #

    def reset_plots(self):

        self.file_path = None
        self.image_rgb = None
        self.show_image_rgb()

        self.pxs_hsv = None
        self.show_hsv_plot()


    def show_hsv_plot(self):            

        ax = self.ax_hsv
        ax.clear()

        if self.pxs_hsv is not None:

            h = self.pxs_hsv[:,0]
            s = self.pxs_hsv[:,1]
            v = self.pxs_hsv[:,2]

            ax.violinplot([h, s, v])
            
        ax.set_title("H-S-V values")

        ax.set_xlim([0,4])
        ax.set_xticks([1,2,3])
        ax.set_xticklabels(["H", "S", "V"])

        ax.set_ylim([0,260])
        ax.set_yticks(np.linspace(0,260,27))

        ax.grid(which="major", axis="y", linestyle="-") 

        f = plt.gcf()
        f.canvas.draw()


    def show_image_rgb(self):
        
        ax = self.ax_image_rgb
        ax.clear()

        if (self.file_path is None) or (self.image_rgb is None):

            ax.xaxis.set_ticks([])
            ax.yaxis.set_ticks([])

        else:

            ax.imshow(self.image_rgb)

            file_name = os.path.basename(self.file_path)
            ax.set_title(file_name)


# ----- MAIN ----- #

if __name__ == "__main__":

    color_picker = ColorPicker()







