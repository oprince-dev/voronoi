import numpy as np
import random
import cv2
from scipy.spatial import Voronoi


def main():
    pts = np.array([[-1, -1]])
    qty = 6
    radius = 2

    def open():
        img = cv2.imread('./gradient.jpg', 0)
        canvas = np.zeros((img.shape))
        canvas[0:] = (255)
        return img, canvas

    def init_dots(canvas, pts, qty, radius):
        for p in range(qty):
            pX = random.randrange(0, canvas.shape[1])
            pY = random.randrange(0, canvas.shape[0])
            pts = np.append(pts, [[pX, pY]], axis=0)
            cv2.circle(canvas, (pX, pY), radius*2, (0), -1)
        pts = np.delete(pts, 0, axis=0)
        return canvas, pts

    def create_Voronoi(canvas, pts):
        vor = Voronoi(pts)
        vertices = vor.vertices
        regions = vor.regions
        print(regions)
        for r in regions:
            print("current Region: " + str(r))
            if r:
                p = np.array([[-1, -1]], np.int32)
                for i in r:
                    v = vertices[i]
                    vX = v[0]
                    vY = v[1]
                    p = np.append(p, [[vX, vY]], axis=0)
                    p = np.rint(p)
                p = np.delete(p, 0, axis=0)
                print("P: " + str(p))

                canvas = cv2.polylines(canvas, np.int32([p]), True, (0, 0, 0))

        for v in vertices:
            vX = round(int(v[0]))
            vY = round(int(v[1]))
            cv2.circle(canvas, (vX, vY), 5, (0))

        return canvas

    def split_cell():
        pass
        # need a function to find new dot's region and split that cell

    def display_image(canvas):
        cv2.imshow('canvas', canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    img, canvas = open()
    canvas, pts = init_dots(canvas, pts, qty, radius)
    canvas = create_Voronoi(canvas, pts)
    # canvas = cv2.polylines(canvas, [pts], True, (0, 0, 0))

    display_image(canvas)


if __name__ == '__main__':
    main()
