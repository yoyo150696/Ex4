#   Welcome to the Pokemon Game!!
![](https://cdn.custom-cursor.com/collections/129/cover-pokemon-preview.png)
## Game Description-
the game recieve a graph with a list of pokemons and agents that are on the edges of the graph,the main goal is that the agents need to achieve the much posibble pokemons in less time and moves.
## alghoritems
### shortest path
https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
the algorithm create a priority queue and enter the src node to the queue. then he goes over every node in the queue. for each node he check all its neighbors. for each neighbor it calculate the distance of the curr node and the distance bitween them. and check if the neighbor dosent have a distance or if the distance is bigger then the cur distance. if it dose it replace the distance of the neighbor with cur distance and replace the path of neighbor with the path of the cur node plus the cur node. it add the neighbor to the priority queue. the algorithm end when the priority queue is empty. the algorithm return the distance and path of the dest node.

we use the shortest path alghoritem as a greedy alghorithem that each agent searh where is the closes pokemon to him and the agent go to the pokemon accord the shortestpath path-if there more than one agent we do that the agents cant go to same pokemon,so each agent hade a unique pokemon.
## clases
### DiGraph
this class has two properties. the first is a liabery called nodes. that it keys are the id of the nodes, and it values are of type Node. the second one is MC tjet counts the number of changes.

### GraphAlgo
this class has one property, called graph from type DiGraph.

### Node
this class has 3 properties. the first one is ID. the second one is pos. the last one is a libery called edges that represent all the edges coming out of the curr node.

### edges
this class has 3 properties. the first one is src. the second one is dest. the last one is w that represent the weight of the edge.


##video
![](https://im3.ezgif.com/tmp/ezgif-3-160954bcd4.gif)
