# -*- coding: utf-8 -*-
#
import numpy


# pylint: disable=too-many-locals, too-many-statements
def _refine(node_coords, edges, cells_nodes, cells_edges):
    '''Canonically refine a mesh by inserting nodes at all edge midpoints
    and make four triangular elements where there was one.
    This is a very crude refinement; don't use for actual applications.
    '''
    num_nodes = len(node_coords)
    num_new_nodes = len(edges)

    # new_nodes = numpy.empty(num_new_nodes, dtype=numpy.dtype((float, 2)))
    node_coords.resize(num_nodes+num_new_nodes, 3, refcheck=False)
    # Set starting index for new nodes.
    new_node_gid = num_nodes

    # After the refinement step, all previous edge-node associations will be
    # obsolete, so record *all* the new edges.
    num_edges = len(edges)
    num_cells = len(cells_nodes)
    assert num_cells == len(cells_edges)
    num_new_edges = 2 * num_edges + 3 * num_cells
    new_edges_nodes = numpy.empty(num_new_edges, dtype=numpy.dtype((int, 2)))

    new_edge_gid = 0

    # After the refinement step, all previous cell-node associations will be
    # obsolete, so record *all* the new cells.
    num_new_cells = 4 * num_cells
    new_cells_nodes = numpy.empty(num_new_cells, dtype=numpy.dtype((int, 3)))
    new_cells_edges = numpy.empty(num_new_cells, dtype=numpy.dtype((int, 3)))
    new_cell_gid = 0

    is_edge_divided = numpy.zeros(num_edges, dtype=bool)
    edge_midpoint_gids = numpy.empty(num_edges, dtype=int)
    edge_newedges_gids = numpy.empty(num_edges, dtype=numpy.dtype((int, 2)))

    # Loop over all elements.
    for cell_id, cell in enumerate(zip(cells_edges, cells_nodes)):
        cell_edges, cell_nodes = cell
        # Divide edges.
        local_edge_midpoint_gids = numpy.empty(3, dtype=int)
        local_edge_newedges = numpy.empty(3, dtype=numpy.dtype((int, 2)))
        local_neighbor_midpoints = [[], [], []]
        local_neighbor_newedges = [[], [], []]
        for k, edge_gid in enumerate(cell_edges):
            edgenodes_gids = edges[edge_gid]
            if is_edge_divided[edge_gid]:
                # Edge is already divided. Just keep records for the cell
                # creation.
                local_edge_midpoint_gids[k] = edge_midpoint_gids[edge_gid]
                local_edge_newedges[k] = edge_newedges_gids[edge_gid]
            else:
                # Create new node at the edge midpoint.
                node_coords[new_node_gid] = \
                    0.5 * (node_coords[edgenodes_gids[0]] +
                           node_coords[edgenodes_gids[1]]
                           )
                local_edge_midpoint_gids[k] = new_node_gid
                new_node_gid += 1
                edge_midpoint_gids[edge_gid] = \
                    local_edge_midpoint_gids[k]

                # Divide edge into two.
                new_edges_nodes[new_edge_gid] = \
                    numpy.array([edgenodes_gids[0],
                                 local_edge_midpoint_gids[k]
                                 ])
                new_edge_gid += 1
                new_edges_nodes[new_edge_gid] = \
                    numpy.array([local_edge_midpoint_gids[k],
                                 edgenodes_gids[1]
                                 ])
                new_edge_gid += 1

                local_edge_newedges[k] = [new_edge_gid-2, new_edge_gid-1]
                edge_newedges_gids[edge_gid] = \
                    local_edge_newedges[k]
                # Do the household.
                is_edge_divided[edge_gid] = True
            # Keep a record of the new neighbors of the old nodes.
            # Get local node IDs.
            edgenodes_lids = [
                numpy.nonzero(cell_nodes == edgenodes_gids[0])[0][0],
                numpy.nonzero(cell_nodes == edgenodes_gids[1])[0][0]
                ]
            local_neighbor_midpoints[edgenodes_lids[0]] \
                .append(local_edge_midpoint_gids[k])
            local_neighbor_midpoints[edgenodes_lids[1]]\
                .append(local_edge_midpoint_gids[k])
            local_neighbor_newedges[edgenodes_lids[0]] \
                .append(local_edge_newedges[k][0])
            local_neighbor_newedges[edgenodes_lids[1]] \
                .append(local_edge_newedges[k][1])

        new_edge_opposite_of_local_node = numpy.empty(3, dtype=int)
        # New edges: Connect the three midpoints.
        for k in range(3):
            new_edges_nodes[new_edge_gid] = local_neighbor_midpoints[k]
            new_edge_opposite_of_local_node[k] = new_edge_gid
            new_edge_gid += 1

        # Create new elements.
        # Center cell:
        new_cells_nodes[new_cell_gid] = local_edge_midpoint_gids
        new_cells_edges[new_cell_gid] = new_edge_opposite_of_local_node
        new_cell_gid += 1
        # The three corner elements:
        for k in range(3):
            new_cells_nodes[new_cell_gid] = \
                numpy.array([cells_nodes[cell_id][k],
                             local_neighbor_midpoints[k][0],
                             local_neighbor_midpoints[k][1]
                             ])
            new_cells_edges[new_cell_gid] = \
                numpy.array([new_edge_opposite_of_local_node[k],
                             local_neighbor_newedges[k][0],
                             local_neighbor_newedges[k][1]
                             ])
            new_cell_gid += 1

    return node_coords, new_edges_nodes, new_cells_nodes, new_cells_edges
