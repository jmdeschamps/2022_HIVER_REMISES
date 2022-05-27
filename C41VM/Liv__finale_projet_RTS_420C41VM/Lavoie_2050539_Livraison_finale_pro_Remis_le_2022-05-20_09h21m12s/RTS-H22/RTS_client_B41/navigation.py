from math import floor

from helper import Helper

from RTS_modele import *


# fab todo to doc

# A * finds a path from start to goal.
# h is the heuristic function.h(n) estimates the cost to reach goal from node n.
def A_Star(cartecase , start, goal, pos_x, pos_y):
    """target_x, target_y = goal.centre()

    # The set of discovered nodes that may need to be(re -) expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min - heap or priority queue rather than a hash - set.
    open_set = {start}

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    came_from = {}

    # For node n, g_score[n] is the cost of the cheapest path from start to n currently known.
    g_score = {}
    # For node n, f_score[n] := g_score[n] + h(n).f_score[n] represents our current best guess as to
    # how short a path from start to finish can be if it goes through n.
    f_score = {}

    for colone in cartecase:
        for case in colone:
            g_score[case] = float('inf')
            f_score[case] = float('inf')
    g_score[start] = 0
    f_score[start] = start.h(target_x, target_y)

    print("len", len(open_set))
    while len(open_set) != 0:
        # This operation can occur in O(1) time if openSet is a min - heap or a priority queue
        f_score.items()

        temp = filter(lambda x: x[0] in open_set, f_score.items())
        current = min(temp, key=lambda x: x[1])[0]
        if current == goal:
            return reconstruct_path(came_from, current, pos_x, pos_y, start, goal)

        open_set.remove(current)
        for neighbor in current.get_ajacent():
            cost = neighbor[1]
            # d(current, neighbor) is the weight of the edge from current to neighbor
            # tentative_g_score is the distance from start to

            # the neighbor through current
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor[0]]:
                # This path to neighbor is better than any previous one. Record it!
                came_from[neighbor[0]] = current
                g_score[neighbor[0]] = tentative_g_score
                f_score[neighbor[0]] = tentative_g_score + neighbor[0].h(target_x, target_y)
                if neighbor[0] not in open_set:
                    open_set.add(neighbor[0])"""

    # Open set is empty but goal was never reached
    return []


def reconstruct_path(came_from: dict, current, pos_x, pos_y, start, goal):
    total_path = []
    while current in came_from.keys():
        current = came_from[current]
        # total_path.insert(0, current)
        total_path.insert(0, current)

    #last_waypoint_x, last_waypoint_y = goal.caculate_waypoint(last_waypoint_x, last_waypoint_y)
    total_path.append(goal)

    total_path.pop(0)
    out_path = [(pos_x, pos_y)]
    for node in total_path:
        pos_x, pos_y = node.caculate_waypoint(pos_x, pos_y)
        out_path.append((pos_x, pos_y))

    # total_path.insert(0, start)
    return out_path

