
from maze import *
from heapq import *

# search closest path to flag
def solve(maze):
  # reset alle node distances and prev nodes
  maze.reset_solve()

  # init
  start_node = maze.get_player_node()
  start_node.set_dist(0)
  target = maze.get_flag_node()

  visited = set()
  next_nodes = [(start_node.get_dist(), start_node)]

  while target not in visited:
    # current node is always the one with the shortest dist to start
    _, current_node = heappop(next_nodes)

    neighbours = maze.get_actions(only_directions=False, pos=current_node.get_pos())
    for direction, neighbour in neighbours:

      # check if the new way is shorter
      new_dist = current_node.get_dist() + 1

      if new_dist < neighbour.get_dist():
        neighbour.set_dist(new_dist)
        neighbour.set_prev(direction, current_node)
        heappush(next_nodes, (neighbour.get_dist(), neighbour))

    if current_node == target:
      print()

    visited.add(current_node)  # now all neighbours are visited, no more changes to current node

  # backtrack directions
  way = []
  node = maze.get_flag_node()
  while node is not start_node:
    d, node = node.get_prev()
    way.append(d)

  return ''.join(reversed(way))


if __name__ == "__main__":
  from maze import Maze

  m = Maze(verbose=False)
  directions = solve(m)

  m.show_solve(directions)
  print(directions)
