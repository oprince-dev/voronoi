import argparse
import random
from math import sqrt

import cv2
import numpy as np
from scipy.spatial import Voronoi


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Voronoi weighted stippler',
        usage='%(prog)s <IMAGE> [-q QUANTITY] [-i ITERATIONS] [-c RADIUS] '
              '[-r RELAX] [-l MIN_DISTANCE] [-u MAX_DISTANCE] [-o OVERLAP]',
    )
    parser.add_argument('Image')
    parser.add_argument(
        '-q', '--quantity',
        help='# of stipples (int)',
        default=1000,
    )
    parser.add_argument(
        '-i', '--iterations',
        help='# of iterations (int)',
        type=int,
        default=5,
    )
    parser.add_argument(
        '-c', '--radius',
        help='Radius of stipples',
        type=int,
        default=0,
    )
    parser.add_argument(
        '-r', '--relax',
        help='# of centroid relaxing iterations (int)',
        type=int,
        default=3,
    )
    parser.add_argument(
        '-l', '--min_distance',
        help='Minimum distance allowed between stipples (int)',
        type=int,
        default=4,
    )
    parser.add_argument(
        '-u', '--max_distance',
        help='Minimum distance allowed between stipples (int)',
        type=int,
        default=100,
    )
    parser.add_argument(
        '-o', '--overlap',
        help='Allow overlapping of stipples',
        action='store_true',
        default=False,
    )

    args = parser.parse_args()

    QTY = args.quantity
    ITER = args.iterations
    RADIUS = args.radius
    COLOR = 255
    RELAX = args.relax
    MAX_DISTANCE = args.max_distance
    MIN_DISTANCE = args.min_distance
    OVERLAP = args.overlap
    IMAGE = args.Image

    def open() -> tuple[np.ndarray, np.ndarray]:
        """
        Loads image file and returns nparray of pixels and a blank canvas with
        the same shape.
        """
        img = cv2.imread(IMAGE, 0)
        try:
            canvas = np.copy(img)
            canvas[0:] = 0
            return img, canvas
        except IndexError:
            raise SystemExit(f'Error loading image: {IMAGE}')

    def initialize_stipples(canvas: np.ndarray, QTY: int) -> np.ndarray:
        """
        Generates initial stipples specified in QTY (Quantity of stipples)
        """
        x = np.random.uniform(0, canvas.shape[1], size=int(QTY))
        y = np.random.uniform(0, canvas.shape[0], size=int(QTY))
        s = np.column_stack((x, y))
        return s

    def centroid(
        canvas: np.ndarray,
        stipples: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculates the centroid of each voronoi region and returns new stipples
        list with updated centroid (X, Y) coordinates. Original stipple points
        are deleted.
        """
        # takes stipples and calculates voronoi & return centroids
        vor = Voronoi(stipples, qhull_options='Qc')
        centroids = np.array([[-1, -1]], np.int16)
        for r in vor.regions:
            if len(r) >= 3:
                p = np.array([[-1, -1]], np.int16)
                for i in r:
                    v = vor.vertices[i]
                    vX = v[0]
                    vY = v[1]
                    p = np.append(p, [[vX, vY]], axis=0)
                    p = np.rint(p)
                p = np.delete(p, 0, axis=0)
                sX, sY = np.sum(p, axis=0)
                n = p.shape[0]
                cX = round(sX / n)
                cY = round(sY / n)
                if 0 <= cX < canvas.shape[1] and 0 <= cY < canvas.shape[0]:
                    centroids = np.append(centroids, [[cX, cY]], axis=0)
                else:
                    x = random.randrange(0, canvas.shape[1])
                    y = random.randrange(0, canvas.shape[0])
                    centroids = np.append(centroids, [[x, y]], axis=0)
        centroids = np.delete(centroids, 0, axis=0)

        return canvas, centroids

    def delete_check(img, canvas, dC, cX, cY):
        """
        Takes pixel value (0-255) and calculates brightness in decimal notation
        (value / 255). The distance between the current pointin iteration and
        its' neighbor is also expressed in decimal notation(dC / MAX_DISTANCE).
        f (brightness) is

        """
        value = img[cY, cX]
        f = value / 255
        p = (dC / MAX_DISTANCE)
        # print(f'{f=}')
        # print(f'{p=}')
        # print('\n')
        if not OVERLAP and dC < MIN_DISTANCE:
            return True

        if p < f**2:
            return True
        elif p >= f**2:
            return False
        else:
            return None

    def create_delete_stipples(
        img: np.ndarray,
        canvas: np.ndarray,
        stipples: np.ndarray,
        RADIUS: int,
    ) -> tuple[np.ndarray, np.ndarray]:
        vor = Voronoi(stipples, qhull_options='Qc')
        for j, pr in enumerate(vor.point_region):
            current_point = vor.points[j]
            current_region_index = vor.point_region[j]
            current_region = vor.regions[current_region_index]

            if -1 in current_region:
                current_region.remove(-1)

            random_vertex_index = random.choice(current_region)
            random_vertex = vor.vertices[random_vertex_index]

            rvX, rvY = random_vertex.astype(int)
            cX, cY = current_point.astype(int)
            dX = rvX - cX
            dY = rvY - cY
            dC = sqrt((dX**2) + (dY**2))

            action = delete_check(img, canvas, dC, cX, cY)
            if action is True:
                x = random.randrange(0, canvas.shape[1])
                y = random.randrange(0, canvas.shape[0])
                stipples = np.delete(stipples, j, 0)
                stipples = np.vstack((stipples, [x, y]))

            elif action is False:
                pt1 = np.array([(cX + (dX / 2)), (cY + (dY / 2))])
                pt2 = np.array([(cX - (dX / 2)), (cY - (dY / 2))])
                stipples = np.delete(stipples, j, 0)
                stipples = np.vstack((stipples, pt1))
                stipples = np.vstack((stipples, pt2))
                if len(stipples) > QTY:
                    for _ in range((len(stipples))-QTY):
                        unlucky = random.randrange(0, len(stipples))
                        stipples = np.delete(stipples, unlucky, 0)
                elif len(stipples) < QTY:
                    for _ in range(QTY-len(stipples)):
                        x = random.randrange(0, canvas.shape[1])
                        y = random.randrange(0, canvas.shape[0])
                        stipples = np.vstack((stipples, [x, y]))

        return canvas, stipples

    img, canvas = open()
    stipples = initialize_stipples(canvas, QTY)
    for q in range(ITER):
        canvas, stipples = centroid(canvas, stipples)
        canvas, stipples = create_delete_stipples(
            img, canvas, stipples, RADIUS,
        )
    for r in range(RELAX):
        canvas, stipples = centroid(canvas, stipples)

    for p in stipples:
        canvas = cv2.circle(
            canvas, (round(p[0]), round(p[1])), RADIUS, COLOR, -1,
        )
    cv2.imshow('canvas', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0


if __name__ == '__main__':
    exit(main())
