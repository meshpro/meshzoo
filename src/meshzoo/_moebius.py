import numpy as np


def moebius(
    num_twists: int = 1,  # How many twists are there in the 'paper'?
    nl: int = 60,  # Number of nodes along the length of the strip
    nw: int = 11,  # Number of nodes along the width of the strip (>= 2)
    variant: str = "classical",
):
    """Creates a simplistic triangular mesh on a slightly Möbius strip. The
    Möbius strip here deviates slightly from the ordinary geometry in that it
    is constructed in such a way that the two halves can be exchanged as to
    allow better comparison with the pseudo-Möbius geometry.

    The variant is either `'classical'` or `'smooth'`. The first is the classical
    Möbius band parametrization, the latter a smoothed variant matching
    `'pseudo'`.
    """
    # The width of the strip
    width = 1.0
    scale = 10.0

    # radius of the strip when flattened out
    r = 1.0

    # seam displacement
    alpha0 = 0.0  # pi / 2

    # How flat the strip will be.
    # Positive values result in left-turning Möbius strips, negative in
    # right-turning ones.
    # Also influences the width of the strip.
    flatness = 1.0

    # Generate suitable ranges for parametrization
    u_range = np.linspace(0.0, 2 * np.pi, num=nl, endpoint=False)
    v_range = np.linspace(-0.5 * width, 0.5 * width, num=nw)

    # Create the vertices. This is based on the parameterization
    # of the Möbius strip as given in
    # <https://en.wikipedia.org/wiki/M%C3%B6bius_strip#Geometry_and_topology>
    sin_u = np.sin(u_range)
    cos_u = np.cos(u_range)
    alpha = num_twists * 0.5 * u_range + alpha0
    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)

    if variant == "classical":
        a = cos_alpha
        b = sin_alpha
        reverse_seam = num_twists % 2 == 1
    elif variant == "smooth":
        # The fundamental difference with the ordinary Möbius band here are the
        # squares.
        # It is also possible to to abs() the respective sines and cosines, but
        # this results in a non-smooth manifold.
        a = np.copysign(cos_alpha ** 2, cos_alpha)
        b = np.copysign(sin_alpha ** 2, sin_alpha)
        reverse_seam = num_twists % 2 == 1
    else:
        assert variant == "pseudo"
        a = cos_alpha ** 2
        b = sin_alpha ** 2
        reverse_seam = False

    nodes = (
        scale
        * np.array(
            [
                np.outer(a * cos_u, v_range) + r * cos_u[:, np.newaxis],
                np.outer(a * sin_u, v_range) + r * sin_u[:, np.newaxis],
                np.outer(b, v_range) * flatness,
            ]
        )
        .reshape(3, -1)
        .T
    )

    cells = _create_elements(nl, nw, reverse_seam)
    return nodes, cells


def _create_elements(nl, nw, reverse_seam):
    cells = []
    for i in range(nl - 1):
        for j in range(nw - 1):
            if (i + j) % 2 == 0:
                cells.append([i * nw + j, (i + 1) * nw + j + 1, i * nw + j + 1])
                cells.append([i * nw + j, (i + 1) * nw + j, (i + 1) * nw + j + 1])
            else:
                cells.append([i * nw + j, i * nw + j + 1, (i + 1) * nw + j])
                cells.append([i * nw + j + 1, (i + 1) * nw + j, (i + 1) * nw + j + 1])

    # close the geometry
    i = nl - 1
    if reverse_seam:
        # Close the geometry upside down (odd Möbius fold)
        for j in range(nw - 1):
            if (i + j) % 2 == 0:
                cells.append([i * nw + j, (nw - 1) - (j + 1), i * nw + j + 1])
                cells.append([i * nw + j, (nw - 1) - j, (nw - 1) - (j + 1)])
            else:
                cells.append([i * nw + j, i * nw + j + 1, (nw - 1) - j])
                cells.append([i * nw + j + 1, (nw - 1) - j, (nw - 1) - (j + 1)])
    else:
        # Close the geometry upside up (even Möbius fold)
        for j in range(nw - 1):
            if (i + j) % 2 == 0:
                cells.append([i * nw + j, j + 1, i * nw + j + 1])
                cells.append([i * nw + j, j, j + 1])
            else:
                cells.append([i * nw + j, i * nw + j + 1, j])
                cells.append([i * nw + j + 1, j, j + 1])

    return np.array(cells)
