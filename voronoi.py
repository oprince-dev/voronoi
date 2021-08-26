import numpy as np
import random
import cv2
from scipy.spatial import Voronoi


def main():
    min_distance = 20
    max_distance = 200
    pts = np.array([[-1, -1]])
    qty = 100
    radius = 2
    iterations = 1

    def open():
        img = cv2.imread('./gradient.jpg', 0)
        # print(img[0,0])
        canvas = np.zeros(img.shape)
        # img = np.zeros((300, 300))
        canvas[0:] = 0
        print(type(img))
        print(type(canvas))
        return img, canvas

    def init_dots(canvas, pts, qty, radius):
        pts = np.array([[-1, -1]], np.int16)
        for p in range(qty):
            # pX = np.random.uniform(0, canvas.shape[1], None)
            # pY = np.random.uniform(0, canvas.shape[0], None)
            pX = random.randrange(0, canvas.shape[1])
            pY = random.randrange(0, canvas.shape[0])
            pts = np.append(pts, [[pX, pY]], axis=0)
            # cv2.circle(canvas, (pX, pY), radius*2, (255, 0, 255), -1)
        # pts = np.delete(pts, 0, axis=0)
        # pts = np.array([[200, 100],[300, 50],[400, 400],[450, 300],[500,550]])
        # pts = np.array([[ -1,  -1],
        #                 [941, 492],
        #                 [318,  47],
        #                 [941,   0],
        #                 [874, 401],
        #                 [652, 360],
        #                 [671, 513],
        #                 [ 35, 261],
        #                 [786, 252],
        #                 [840,  42],
        #                 [648, 296]])
        print(f'{pts=}')
        return canvas, pts


    def draw_Voronoi_edges(canvas, pts):
        # draws the borders of voronoi cells
        vor = Voronoi(pts)
        vertices = vor.vertices
        regions = vor.regions
        for r in regions:
            if r:
                p = np.array([[-1, -1]], np.int16)
                for i in r:
                    print(f'{i=}')
                    if i != -1:
                        v = vertices[i]
                        vX = v[0]
                        vY = v[1]
                        p = np.append(p, [[vX, vY]], axis=0)
                        p = np.rint(p)
                p = np.delete(p, 0, axis=0)
                print(f'{p=}')

                canvas = cv2.polylines(canvas, np.int32([p]), True, (255, 0, 255))

        # for v in vertices:
        #     vX = round(int(v[0]))
        #     vY = round(int(v[1]))
        #     cv2.circle(canvas, (vX, vY), 6, (255, 255, 0))

        return canvas

    def split_cell():
        pass
        # need a function to find new dot's region and split that cell
    def remove_cell():
        pass
        # function to remove point if value is too dark

    def point_check(pts, img):
        for p in pts:
            value = img[p[1], p[0]]
            # print(f'value at ({p[0]},{p[1]}) is {value}')

    def find_centroids(vor):
        vertices = vor.vertices
        regions = vor.regions
        centroids = np.array([[-1, -1]], np.int16)
        for r in regions:
            if r:
                p = np.array([[-1, -1]], np.int16)
                for i in r:
                    if i != -1:
                        v = vertices[i]
                        vX = v[0]
                        vY = v[1]
                        p = np.append(p, [[vX, vY]], axis=0)
                        p = np.rint(p)
                p = np.delete(p, 0, axis=0)
                s = np.sum(p, axis=0)
                sX = s[0]
                sY = s[1]
                n = p.shape[0]
                cX = round(sX / n)
                cY = round(sY / n)
                centroids = np.append(centroids, [[cX, cY]], axis=0)

        return centroids
        # cv2.circle(canvas, (cX, cY), 2, 255, -1)

    def draw_centroids(canvas, pts):
        for p in pts:
            if (0 < p[0] < canvas.shape[1]) and (0 < p[1] < canvas.shape[0]):
                cv2.circle(canvas, (p[0], p[1]), 2, (255, 0, 255), -1)
        # canvas = cv2.polylines(canvas, np.int32(pts), True, (255, 0, 255))
        return canvas

    def display_image(img, canvas):
        cv2.imshow('canvas', canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    img, canvas = open()
    canvas, pts = init_dots(canvas, pts, qty, radius)
    # new_pts = np.array([[-1, -1]], np.int16)
    for _ in range(iterations):
        vor = Voronoi(pts)
        print(f'{vor=}')
        pts = find_centroids(vor)
        print(f'{pts=}')
    # point_check(pts, img)
    canvas = draw_centroids(canvas, pts)
    canvas = draw_Voronoi_edges(canvas, pts)
    display_image(img, canvas)

    return 0

if __name__ == '__main__':
    exit(main())
