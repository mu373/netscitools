# netscitools
Network Science tools (netscitools): Python package that includes useful functions for network science.

## Installation
```sh
# Clone the repository from GitHub
git clone https://github.com/mu373/netscitools

# Install package using pip
cd netscitools
pip install .
```


## Usage

### Network tools
```py
from netscitools.network import *
import networkx as nx
import matplotlib.pyplot as plt

G = nx.karate_club_graph()

# Describe the network
describe_network(G)

# Plot degree distribution
G1 = nx.to_undirected(G)
x, y = degree_distribution(G1)
plt.loglog(x, y,marker='o',lw=0);

# Degree preserving randomization
G_random = degree_preserving_randomization(G1)

# Class 7: Depth-first search
explore_queue = [0]
nodes_visited = {0: 0}
dfs(explore_queue, nodes_visited, G)

# Class 7: Breadth-first search
explore_queue = [0]
nodes_visited = {0: 0}
bfs(explore_queue, nodes_visited, G)
```

### Northeastern University Course Prerequisite network
```py
from netscitools.neu_courses import *
import requests

dept_name = "chme"
dept_html = requests.get("https://catalog.northeastern.edu/course-descriptions/{}/".format(dept_name)).text

# Get course information (course title, course description, prerequisite) for the department
courses_info = get_northeastern_course_info(dept_html)

# Turn the course information into networkx graph object
G_prereq = create_course_prerequisite_network(dept_name, courses_info)

# Plot!
nx.draw(G_prereq)
```

### Utilities
```py
from netscitools.util import compare_decimal_places
compare_decimal_places(0.01, 0.01)
compare_decimal_places(0.01111, 0.01111111)
```


## License
MIT