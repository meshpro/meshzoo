import numpy as np


def triangle(n: int):
    # Create the mesh in barycentric coordinates
    bary = np.hstack(
        [
            [
                np.full(n - i + 1, i / n),
                # np.arange(n - i + 1) / n:
                np.linspace(0.0, (n - i + 1) / n, n - i + 1, endpoint=False),
            ]
            for i in range(n + 1)
        ]
    )
    bary = np.array([1.0 - bary[0] - bary[1], bary[1], bary[0]])

    # Some applications don't accept values like -1.4125e-16.
    bary[bary < 0.0] = 0.0
    bary[bary > 1.0] = 1.0

    cells = []
    k = 0
    for i in range(n):
        j = np.arange(n - i)
        cells.append(np.column_stack([k + j, k + j + 1, k + n - i + j + 1]))
        #
        j = j[:-1]
        cells.append(np.column_stack([k + j + 1, k + n - i + j + 2, k + n - i + j + 1]))
        k += n - i + 1

    cells = np.vstack(cells)
    return bary, cells
