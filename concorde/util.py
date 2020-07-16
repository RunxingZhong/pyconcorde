import numpy as np

EDGE_WEIGHT_TYPES = {
    "EXPLICIT",
    "EUC_2D",
    "EUC_3D",
    "MAX_2D",
    "MAN_2D",
    "GEO",
    "GEOM",
    "ATT",
    "CEIL_2D",
    "DSJRAND",
}


def write_tsp_file(fp, xs, ys, norm, name, dist_matrix=None):
    """ Write data to a TSPLIB file.
    """
    if dist_matrix is None:
        if len(xs) != len(ys):
            raise ValueError(
                "x and y coordinate vector must have the "
                "same length ({} != {})".format(len(xs), len(ys))
            )
    if norm not in EDGE_WEIGHT_TYPES:
        raise ValueError(
            "Norm {!r} must be one of {}"
            .format(norm, ', '.join(EDGE_WEIGHT_TYPES))
        )

    n_dimension = None 
    if dist_matrix is not None:
        n_dimension = dist_matrix.shape[0]
    else:
        n_dimension = len(xs)

    fp.write("NAME: {}\n".format(name))
    fp.write("TYPE: TSP\n")
    fp.write("DIMENSION: {}\n".format(n_dimension))
    if dist_matrix is None:
        fp.write("EDGE_WEIGHT_TYPE: {}\n".format(norm))
        fp.write("NODE_COORD_SECTION\n")
        for n, (x, y) in enumerate(zip(xs, ys), start=1):
            fp.write("{} {} {}\n".format(n, x, y))
    else:

        # to Integer
        dist_matrix = np.round(dist_matrix, 2)
        dist_matrix *= 100
        dist_matrix = np.ceil(dist_matrix)
        dist_matrix = dist_matrix.astype(int)
        fp.write("EDGE_WEIGHT_TYPE: {}\n".format("EXPLICIT"))
        fp.write("EDGE_WEIGHT_FORMAT: FULL_MATRIX\n")
        # fp.write("NODE_COORD_TYPE : NO_COORDS\n")
        nrows, ncols = dist_matrix.shape 
        fp.write("EDGE_WEIGHT_SECTION\n")
        for i in range(nrows):
            row = dist_matrix[i].tolist()
            edge = " ".join([str(r) for r in row])
            fp.write(" " + edge + "\n")
    fp.write("EOF\n")

def read_tsp_tour(fname):
    has_tour = False
    tour = []
    with open(fname) as fp:
        for line in fp:
            if line.startswith("TOUR_SECTION"):
                has_tour = True
            elif line.startswith("EOF"):
                break
            else:
                if has_tour:
                    tour.extend(int(node) for node in line.split())
    if not tour:
        raise RuntimeError("File {} has no valid TOUR_SECTION".format(fname))
    if tour[-1] == -1:
        tour.pop()
    return np.array(tour)
