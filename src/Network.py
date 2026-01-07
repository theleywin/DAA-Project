from src.Tower import Tower
from typing import List


class Network:
    def __init__(self):
        self.towers: List[Tower] = []
        self.adjacency_list: List[List[int]] = [[]]

    def add_tower(self, tower: Tower):
        """Agrega una torre al grafo"""
        if tower not in self.towers:
            self.towers.append(tower)
            self.adjacency_list.append([])
            return True
        return False

    def add_edge(self, tower1_id, tower2_id):
        """Conecta dos torres en el grafo (si son adyacentes)"""
        if tower1_id != tower2_id:
            if tower2_id not in self.adjacency_list[tower1_id]:
                self.adjacency_list[tower1_id].append(tower2_id)
            if tower1_id not in self.adjacency_list[tower2_id]:
                self.adjacency_list[tower2_id].append(tower1_id)
            return True
        return False

    def get_neighbors(self, tower_id):
        """Devuelve las torres vecinas de una torre"""
        if tower_id < len(self.adjacency_list):
            return self.adjacency_list[tower_id]
        else:
            return []
