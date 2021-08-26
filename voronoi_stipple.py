import cv2
import numpy as np
from scipy.spatial import Voronoi

def main() -> int:
    qty = 20
    def open() -> np.ndarray:
        img = cv2.imread('./gradient.jpg', 0)
        canvas = np.zeros(img.shape)
        canvas[0:] = 0
        return img, canvas

    def initialize_stipples(canvas: np.ndarray, qty: int) -> np.ndarray:
        """
        Generates initial stipples specified in qty (Quantity of stipples)
        """
        x = np.random.uniform(0, canvas.shape[1], size=int(qty))
        y = np.random.uniform(0, canvas.shape[0], size=int(qty))
        s = np.column_stack((x, y))
        return s

    def voronoi_centroid(stipples: np.ndarray) -> np.ndarray:
        # takes stipples and calculates voronoi & return centroids
        vor = Voronoi(stipples)
        vertices = vor.vertices
        regions = vor.regions
        print(f'{vertices=}')
        print(f'{regions=}')
        return stipples

    img, canvas = open()
    stipples = initialize_stipples(canvas, qty)
    stipples = voronoi_centroid(stipples)

    # print(stipples)
    for p in stipples:
        canvas = cv2.circle(canvas, (round(p[0]), round(p[1])), 1, 255, 1)
    cv2.imshow('canvas', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 0
if __name__ == '__main__':
    exit(main())
