init starting dots -> [[x1, y2]
                       [x2, y2]]
calculate voronoi with pts
calculate centroids with voronoi
replace pts with centroids

calculate cell size
compare cell size to grayscale value of image:
  cell size distribution is ordered from smallest first (delete those first)
  too small -> delete point
  too big -> split into two new & delete original
