import random
from collections import deque
import numpy as np

class MazeGenerator:
    def __init__(self, size):
        self.size = size
        self.generated_maze = None

    def generate(self):
        self.generated_maze = None
        while self.generated_maze is None or not self.bfs(self.generated_maze, (0, 0), (self.size[0] - 1, self.size[1] - 1)):
            self.generated_maze = np.ones(self.size, dtype=int)
            self.generated_maze[0][0] = 0
            self.generated_maze[self.size[0] - 1][self.size[1] - 1] = 0
            self.dfs(self.generated_maze, (0, 0), set())
            
            # Randomly place walls while ensuring there's always a path from start to end
            random.seed()
            rows, cols = self.size
            for x in range(rows):
                for y in range(cols):
                    if (x, y) != (0, 0) and (x, y) != (rows - 1, cols - 1):
                        self.generated_maze[x][y] = random.randint(0, 1)

    def generate_text(self, maze):
        rows, cols = self.size
        teks = ""
        teks += "\n----------\n"
        for x in range(rows):
            for y in range(cols):
                if maze[x][y] == 1:
                    teks += "##"
                elif (x, y) == (0, 0):
                    teks += "S "
                elif (x, y) == (rows - 1, cols - 1):
                    teks += "E "
                else:
                    teks += "  "

        teks_lines = [teks[i:i+cols*2] for i in range(0, len(teks), cols*2)]
        teks = "\n".join(teks_lines)
        
        teks += "\n----------\n"
        return teks

    def solve_maze(self):
        if self.generated_maze is None:
            return "Maze belum dibuat. Silakan jalankan metode generate terlebih dahulu."
        
        start = (0, 0)
        end = (self.size[0] - 1, self.size[1] - 1)
        solusi = self.bfs(self.generated_maze, start, end)
        if solusi is None:
            return "Maze tidak dapat diselesaikan."
        else:
            teks = "Langkah untuk menyelesaikan maze:\n"
            for i, step in enumerate(solusi):
                teks += f"{i+1}. {step}\n"
            return teks
        
    def dfs(self, maze, node, visited):
        visited.add(node)
        x, y = node
        maze[x][y] = 0  # Change visited point to wall
        rows, cols = self.size
        neighbors = [(x+dx, y+dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= x+dx < rows and 0 <= y+dy < cols and maze[x+dx][y+dy]]
        for neighbor in neighbors:
            if neighbor not in visited:
                self.dfs(maze, neighbor, visited)

    def bfs(self, maze, awal, akhir):
        rows, cols = self.size
        antrian = deque([awal])
        visited = set([awal])  # Initialize visited set with the start node
        parent = {}

        while antrian:
            node = antrian.popleft()
            x, y = node
            
            # Check if the current node is the target node
            if node == akhir:
                path = []
                while node != awal:
                    path.append(node)
                    node = parent[node]
                path.append(awal)
                path.reverse()
                return path
            
            # Explore neighbors
            neighbors = [(x+dx, y+dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= x+dx < rows and 0 <= y+dy < cols]
            for neighbor in neighbors:
                nx, ny = neighbor
                if neighbor not in visited and not maze[nx][ny]:  # Check if neighbor is not visited and not a wall
                    antrian.append(neighbor)
                    parent[neighbor] = node
                    visited.add(neighbor)  # Add visited status here to avoid re-visiting
                    if neighbor == akhir:
                        # If the target node node is found during exploration, return the path
                        path = []
                        while neighbor != awal:
                            path.append(neighbor)
                            neighbor = parent[neighbor]
                        path.append(awal)
                        path.reverse()
                        return path
        return None

