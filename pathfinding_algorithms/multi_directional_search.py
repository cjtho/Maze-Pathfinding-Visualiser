from .abstract_search import AbstractSearch
from collections import deque
import heapq


class MultiDirectionalSearch(AbstractSearch):
    COLOR_SCANNING = "khaki1"

    def __init__(self, maze):
        super().__init__(maze)
        self.history = []
        self.clusters = [Cluster(self.start), Cluster(self.end)]
        self.global_visited = set()

    def add_clusters(self, cells):
        new_clusters = list(map(lambda x: Cluster(x), cells))
        self.clusters.extend(new_clusters)
        middle_point = (self.start[0] + self.end[0]) // 2, (self.start[1] + self.end[1]) // 2
        self.clusters.sort(key=lambda x: self.manhattan_distance(x.origin, middle_point))

    def solve(self):
        while not self.start_end_met():  # currently really botched
            for cluster in self.clusters:
                if not cluster.emptied:
                    self.expand_cluster(cluster)

        self.search_connected_region()
        path = self.reconstruct_path()
        for cell in path:
            self.history.append((MultiDirectionalSearch.COLOR_PATH, cell))
        return self.history

    def expand_cluster(self, cluster):
        # default BFS behaviour
        if cluster.frontier_queue:
            current = cluster.pop_from_frontier()

            if current in cluster.visited:
                return

            cluster.visited.add(current)
            self.history.append((MultiDirectionalSearch.COLOR_VISITED, current))

            # for efficiency, have global visited set that checks first
            if other_cluster := self.is_cell_in_other_cluster(current, cluster):
                self.merge_clusters(cluster, other_cluster)
                return

            for neighbor in self.get_neighbors(current):
                if neighbor not in cluster.visited and neighbor not in cluster.frontier_set:
                    cluster.add_to_frontier(neighbor)
                    self.history.append((MultiDirectionalSearch.COLOR_FRONTIER, neighbor))

    def is_cell_in_other_cluster(self, cell, cluster):
        for other_cluster in self.clusters:
            if other_cluster.origin != cluster.origin:
                if cell in other_cluster.frontier_set or cell in other_cluster.visited:
                    return other_cluster

        return False

    def merge_clusters(self, cluster_a, cluster_b):
        # Case 1: merging 'start' and 'end' clusters
        if cluster_a.origin in [self.start, self.end] and cluster_b.origin in [self.start, self.end]:
            # merge frontiers and visited sets
            while cluster_b.frontier_queue:
                node = cluster_b.pop_from_frontier()
                cluster_a.add_to_frontier(node)
            cluster_a.visited.update(cluster_b.visited)

            # remove cluster_b and add a new final cluster
            self.clusters.remove(cluster_b)
            final_cluster = Cluster(self.start, cluster_a.frontier_queue, cluster_a.visited)
            self.clusters.clear()
            self.clusters.append(final_cluster)
            return

        # Case 2: merging a regular cluster with 'start' or 'end'
        if cluster_b.origin in [self.start, self.end]:
            cluster_a, cluster_b = cluster_b, cluster_a

        # merge the frontiers and visited sets of the two clusters
        while cluster_b.frontier_queue:
            node = cluster_b.pop_from_frontier()
            if not cluster_a.add_to_frontier(node):
                self.history.append((MultiDirectionalSearch.COLOR_VISITED, node))
        cluster_a.visited.update(cluster_b.visited)

        # mark cluster_b as emptied
        cluster_b.set_emptied(True)

    def start_end_met(self):
        return len(self.clusters) == 1

    def search_connected_region(self):
        def heuristic(point_a, point_b):
            return self.euclidean_distance(point_a, point_b)

        final_cluster = self.clusters.pop()
        visited_nodes = final_cluster.visited

        open_list = []
        heapq.heappush(open_list, (0, self.start))
        g_score = {self.start: 0}
        while open_list:
            current = heapq.heappop(open_list)[1]
            self.history.append((MultiDirectionalSearch.COLOR_SCANNING, current))

            if current == self.end:
                return

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited_nodes:
                    continue
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    self.came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, self.end)

                    if not any(neighbor == n[1] for n in open_list):
                        heapq.heappush(open_list, (f_score, neighbor))

        raise RuntimeError("Path not found")


class Cluster:
    def __init__(self, origin, frontier=None, visited=None):
        self.origin = origin
        self.emptied = False
        self.visited = set() if visited is None else visited

        if frontier is None:
            self.frontier_set = {origin}
            self.frontier_queue = deque([origin])
        else:
            self.frontier_set = set(frontier)
            self.frontier_queue = deque(frontier)

    def add_to_frontier(self, node):
        if node not in self.frontier_set:
            self.frontier_set.add(node)
            self.frontier_queue.append(node)
            return True
        return False

    def pop_from_frontier(self):
        if self.frontier_queue:
            node = self.frontier_queue.popleft()
            self.frontier_set.remove(node)
            return node
        return None

    def set_emptied(self, state):
        self.emptied = state

    def __repr__(self):
        return (f"Cluster(origin={self.origin}, "
                f"frontier_size={len(self.frontier_queue)}, "
                f"visited_count={len(self.visited)}, "
                f"emptied={self.emptied})")
