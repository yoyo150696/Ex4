from client_python.client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from client_python.Graphalgo import GraphAlgo
from client_python.button import button

WIDTH, HEIGHT = 1000, 720

bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
pygame.font.init()
font = pygame.font.SysFont('Constantia', 30)

pok_ls = {}
destlist = []

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()

client = Client()
client.start_connection(HOST, PORT)
pokemons = client.get_pokemons()
a = json.loads(client.get_graph())
graph_al = GraphAlgo()
graph_al.load_graph(a)
graph = graph_al.graph

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object


# get data proportions
list_x = []
list_y = []
for n in graph.nodes.values():
    list_x.append(n.pos[0])
    list_y.append(n.pos[1])
min_x = min(list_x)
min_y = min(list_y)
max_x = max(list_x)
max_y = max(list_y)


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15
s = 4
graph_al.load_pokemons(client.get_pokemons())

for j in graph.nodes.keys():
    for i in graph.all_out_edges_of_node(j).items():
        # find the edge nodes

        # scaled positions
        src_x = my_scale(graph.nodes[j].pos[0], x=True)
        src_y = my_scale(graph.nodes[j].pos[1], y=True)
        dest_x = my_scale(graph.nodes[i[0]].pos[0], x=True)
        dest_y = my_scale(graph.nodes[i[0]].pos[1], y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))
        for p in graph_al.pokemons:
            poc_x = my_scale(p.x, x=True)
            poc_y = my_scale(p.y, y=True)
            sum_ed = pow(pow(src_x - dest_x, 2) + (pow(src_y - dest_y, 2)), 0.5)
            sum_pok = pow(pow(src_x - poc_x, 2) + pow(src_y - poc_y, 2), 0.5) + pow(
                pow(poc_x - dest_x, 2) + pow(poc_y - dest_y, 2), 0.5)

            if abs(sum_ed - sum_pok) < 10:
                if (graph.nodes[j].id - graph.nodes[i[0]].id) > 0:
                    if (p.type > 0):
                        p.src = graph.nodes[i[0]].id
                    else:
                        p.src = graph.nodes[j].id
                else:
                    if (p.type > 0):
                        p.src = graph.nodes[j].id
                    else:
                        p.src = graph.nodes[i[0]].id

dis = 1000
node = 0
max = 0

info = json.loads(client.get_info())["GameServer"]
ls = graph_al.pokemons
for j in range(info["agents"]):
    pop = 0
    i = 0
    for p in ls:
        if p.value > max:
            max = p.value
            po = i
        i = i + 1
    ag = ls.pop(pop)
    client.add_agent("{\"id\":" + str(ag.src) + "}")

graph_al.load_agents(client.get_agents())

# this commnad starts the server - the game is running now
client.start()
"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""





while client.is_running() == 'true':
    graph_al.load_pokemons(client.get_pokemons())
    graph_al.load_agents(client.get_agents())
    info = json.loads(client.get_info())["GameServer"]

    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.nodes.values():
        x = my_scale(n.pos[0], x=True)
        y = my_scale(n.pos[1], y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for j in graph.nodes.keys():
        for i in graph.all_out_edges_of_node(j).items():
            # find the edge nodes

            # scaled positions
            src_x = my_scale(graph.nodes[j].pos[0], x=True)
            src_y = my_scale(graph.nodes[j].pos[1], y=True)
            dest_x = my_scale(graph.nodes[i[0]].pos[0], x=True)
            dest_y = my_scale(graph.nodes[i[0]].pos[1], y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126),
                             (src_x, src_y), (dest_x, dest_y))
            for p in graph_al.pokemons:
                poc_x = my_scale(p.x, x=True)
                poc_y = my_scale(p.y, y=True)
                sum_ed = pow(pow(src_x - dest_x, 2) + (pow(src_y - dest_y, 2)), 0.5)
                sum_pok = pow(pow(src_x - poc_x, 2) + pow(src_y - poc_y, 2), 0.5) + pow(
                    pow(poc_x - dest_x, 2) + pow(poc_y - dest_y, 2), 0.5)
                if abs(sum_ed - sum_pok) < 1:
                    if (graph.nodes[j].id - graph.nodes[i[0]].id) > 0:
                        if (p.type > 0):
                            p.src = graph.nodes[i[0]].id
                            p.dest = graph.nodes[j].id
                        else:
                            p.src = graph.nodes[j].id
                            p.dest = graph.nodes[i[0]].id
                    else:
                        if (p.type > 0):
                            p.src = graph.nodes[j].id
                            p.dest = graph.nodes[i[0]].id

                        else:
                            p.src = graph.nodes[i[0]].id
                            p.dest = graph.nodes[j].id

    # draw agents
    for agent in graph_al.agents:
        x = my_scale(agent.x, x=True)
        y = my_scale(agent.y, y=True)
        pygame.draw.circle(screen, red, (int(x), int(y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in graph_al.pokemons:
        x = my_scale(p.x, x=True)
        y = my_scale(p.y, y=True)
        pygame.draw.circle(screen, Color(0, 255, 255), (int(x), int(y)), 10)

    exit_button = button(0, 0, "STOP")
    exit_button.draw()

    for event in pygame.event.get():
        pos = mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if exit_button.draw():
            client.stop_connection()
            pygame.quit()
            exit(0)
    clock.tick(10)

    text_move = font.render("moves - " + str(info["moves"]), True, white)
    text_grade = font.render("grade - " + str(info["grade"]), True, white)
    text_time = font.render("time left - " + str(client.time_to_end()), True, white)
    screen.blit(text_move, (10, 70))
    screen.blit(text_grade, (10, 100))
    screen.blit(text_time, (10, 135))
    display.update()

    if int(client.time_to_end()) < 200:
        print(client.get_info())
        screen.blit(pygame.font.SysFont('Constantia', 100).render("game over", True, red), (200, 200))
        display.update()

        for i in range(1000):
            for event in pygame.event.get():
                if exit_button.draw():
                    client.stop_connection()
                    pygame.quit()
                    exit(0)
            time.wait(30)
        client.stop_connection()

    for agent in graph_al.agents:
        pop = 0
        i = 0
        max_val = 1000
        for p in graph_al.pokemons:
            path = graph_al.shortest_path(agent.src, p.src)
            if path[0] < max_val:
                max_val = path[0]
                pop = i
            i = i + 1
        pok = graph_al.pokemons.pop(pop)
        sh = graph_al.shortest_path(agent.src, pok.src)
        if len(sh[1]) > 1:
            next_node = (sh[1][1])
        else:
            next_node = pok.dest

        client.choose_next_edge(
            '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')

    client.move()
