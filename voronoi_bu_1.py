from scipy.spatial import Voronoi, voronoi_plot_2d
#import cv2
from PIL import Image, ImageDraw
import numpy as np
import random
import matplotlib.pyplot as plt


# import ref Image
# random 2 init dots
# calculte


def main():
    pts = np.array([[0, 0]])
    qty = 8
    r = 5

    def open():
        #img = cv2.imread('./gradient.jpg')
        img = Image.open('./gradient.jpg')
        artboard = ImageDraw.Draw(img)
        return img, artboard

    def init_dots(img, artboard, pts, qty, r):
        for p in range(qty):
            pX = random.randrange(0, img.size[0])
            pY = random.randrange(0, img.size[1])
            pts = np.append(pts, [[pX, pY]], axis=0)
            # pts = np.append([int(pX), int(pY)])
        # for pt in pts:
        #    artboard.ellipse((pt[0]-r, pt[1]-r, pt[0] + r, pt[1] + r), fill=(255, 0, 100))
        print(pts)
        return artboard, pts

    def create_Voronoi(pts):
        vor = Voronoi(pts)
        voronoi_plot_2d(vor)
        print(vor.vertices)
        plt.show()

    img, artboard = open()
    artboard, pts = init_dots(img, artboard, pts, qty, r)
    create_Voronoi(pts)
    # img.show()

    # vor = Voronoi(pts)
    # fig = voronoi_plot_2d(vor, show_vertices=True, line_colors='orange',
    #                      line_width = 2, line_alpha = 0.6, point_size = 2)
    # plt.show()


if __name__ == '__main__':
    main()
