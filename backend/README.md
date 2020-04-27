## Backend Software Design/Architecture

To implement the backend, we wanted an approach that would make the design very modular. We wanted to be able to design
each portion of the system individually, and decouple the backend from the front end so they could be developed and
tested individually. We were able to stub a fake route to the frontend to test plotting. We were also able to stub the 
frontend inputs to call the algorithms without starting the frontend.

The backend and the frontend interact through the app.py file located in the backend/ folder. This file starts the flask
web server. The input and output of the flask server was standardized initially so all algorithms could output the same
format of data for the frontend to parse. 

The backend implements a strategy design pattern. By doing this, the routing mechanism can we easily changed on the fly.
The routing object calls a generic function "get_route", which will call the correct routing implementation based on
inputs from the frontend. The strategy method allowed us to easily add more routing algorithms. Each concrete routing
strategy has its own minimization and maximization function. This was done in case those algorithms had to be tuned
based on what kind of routing algorithm was used. This also made it more flexible so that not every algorithm, like BFS,
needed to implement a maximum elevation and minimum elevation function.

To to test the algorithms, we created the route_and_graphs_tests/ folder. Inside, the generate_graph file creates a test
graph. This test graph is used to test all the routing algorithms. The tests for the routing algorithms check that the 
path length of a found route adheres to the length constraint, and the elevation of a found route adheres to the
elevation constraint. All tests are currently passing. The tests can be run by running:


    python3 algorithm_tests.py



