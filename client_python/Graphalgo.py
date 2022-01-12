from queue import PriorityQueue
import json
from client_python.DiGraph import DiGraph
from client_python.Pokemon import Pokemon
from client_python.Agent import Agent
class GraphAlgo:
    def __init__(self, g=None):
        if not g:
            self.graph = DiGraph()
            self.pokemons = []
            self.agents = []
        else:
            self.graph = g

    def get_graph(self):
        return self.graph

    def load_graph(self, graph: dict) -> bool:
        for n in graph["Nodes"]:
            posi = n['pos'].split(",")
            self.graph.add_node(n["id"], (float(posi[0]), float(posi[1])))

        for i in graph["Edges"]:
            self.graph.add_edge(int(i["src"]), int(i["dest"]), i["w"])
        return True
        raise NotImplementedError

    def load_pokemons(self, poks) -> bool:
        self.pokemons = []
        pok_js = json.loads(poks)
        for i in pok_js["Pokemons"]:
            value = i["Pokemon"]["value"]
            type = i["Pokemon"]["type"]
            pos = i["Pokemon"]["pos"].split(',')
            pos_x = float(pos[0])
            pos_y = float(pos[1])
            self.pokemons.append(Pokemon(value, type, pos_x, pos_y))
        return True

    def load_agents(self, agents) -> bool:
        self.agents = []
        agents_js = json.loads(agents)
        for i in agents_js["Agents"]:
            id = i["Agent"]["id"]
            value = i["Agent"]["value"]
            src = i["Agent"]["src"]
            dest = i["Agent"]["dest"]
            speed = i["Agent"]["speed"]
            pos = i["Agent"]["pos"].split(',')
            pos_x = float(pos[0])
            pos_y = float(pos[1])
            self.agents.append(Agent(id, value, src, dest, speed, pos_x, pos_y))
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        paths = dict()
        dis = {}
        v = {}
        for i in self.graph.nodes.keys():
            paths[i] = list()
            dis[i] = float('inf')
        dis[id1] = 0
        v[id1] = True
        pq = PriorityQueue()
        pq.put(id1)
        while not pq.empty():
            cur_id = pq.get()
            v[cur_id] = True
            path = []
            for i in paths.get(cur_id):
                path.append(i)
            path.append(cur_id)

            paths[cur_id] = path
            for i in self.graph.all_out_edges_of_node(cur_id).items():
                if i[0] not in v:
                    old_cost = dis[i[0]]
                    new_cost = dis[cur_id] + i[1]
                    if old_cost > new_cost:
                        pq.put(i[0])
                        dis[i[0]] = new_cost
                        paths[i[0]] = paths[cur_id]

        return dis[id2], paths[id2]
