import os
import collections
import time
import heapq
from heapq import heappush, heappop
import sys

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def find_goal(state):
    return(''.join(sorted(state.replace('.', '')))+".")


def swap_characters(s, i1, i2):
    stringList = list(s)
    stringList[i1], stringList[i2] = stringList[i2], stringList[i1]
    return "".join(stringList)


def get_children(state, size):
    boards = []

    index = state.index('.')

    # To the left
    if ((index) % int(size)) != 0:
        boards.append(swap_characters(state, index, index - 1))

    # To the right
    if ((index + 1) % int(size)) != 0:
        boards.append(swap_characters(state, index, index + 1))

    # Swap . with down
    if (index + int(size) < len(state)):
        boards.append(swap_characters(state, index, index + int(size)))

    # Swap . with up
    if (index - int(size) > -1):
        boards.append(swap_characters(state, index, index - int(size)))

    return boards


def get_children_app(state, size):
    boards = {}

    index = state.index('.')

    # To the left
    if ((index) % int(size)) != 0:
        boards['left'] = swap_characters(state, index, index - 1)

    # To the right
    if ((index + 1) % int(size)) != 0:
        boards['right'] = (swap_characters(state, index, index + 1))

    # Swap . with down
    if (index + int(size) < len(state)):
        boards['down'] = (swap_characters(state, index, index + int(size)))

    # Swap . with up
    if (index - int(size) > -1):
        boards['up'] = (swap_characters(state, index, index - int(size)))

    return boards


def bfs_shortest_path(board_state, size):
    fringe = collections.deque()
    visited = set()

    parents = {
        board_state.replace('\n', ''): "start"
    }

    fringe.append(board_state.replace('\n', ''))
    visited.add(board_state.replace('\n', ''))

    goal_state = find_goal(board_state).replace('\n', '')
    while(fringe):
        current = fringe.pop()
        if(current == goal_state):
            steps = path(current, parents, size)
            steps.insert(0, board_state.replace('\n', ''))
            return steps
        for board in get_children(current, size):
            if board not in visited:
                fringe.appendleft(board)
                visited.add(board)
                parents[board] = current

    return None


def path(board_state, parents, size):
    listmoves = []
    while parents[board_state] != "start":
        listmoves.append(board_state)
        board_state = parents[board_state]
    listmoves = listmoves[::-1]
    # for move in listmoves:
    #     print_puzzle(move, size)
    #     print()
    return listmoves


def a_star(board_state, size):
    goal = find_goal(board_state.replace("\n", ""))

    closed = set()
    parents = {
        board_state.replace('\n', ''): "start"
    }

    start_node = (a_star_heuristic(board_state, size), board_state, 0)
    heap = []
    heappush(heap, start_node)

    while heap:
        current = heappop(heap)
        # print(current)
        if current[1] == goal:
            # print('made it to goal')
            # steps = dfs_path(current[1], parents, size)

            return current[2]

        if current[1] not in closed:
            closed.add(current[1])
            for board in get_children(current[1], size):
                heappush(heap, (current[2] + a_star_heuristic(board, size), board, current[2] + 1))
                if board not in parents:
                    parents[board] = current[1]

    return None


def a_star_heuristic(board_state, size):
    goal = find_goal(board_state.replace("\n", ""))
    inversions = 0
    for letter in board_state:
        if letter != '.':
            total_inv = abs((board_state.find(letter) // size) - (goal.find(letter) // size))
            total_inv += abs((board_state.find(letter) % size) - (goal.find(letter) % size))
            inversions += total_inv

    return inversions
