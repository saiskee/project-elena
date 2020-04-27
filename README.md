
# Elevation-based Navigation: The Extended Stack
EleNa (Elevation-based Navigation) is a routing software that calculates routes based on your preference of route elevation. For example, if you wanted to get from the base of a hill to the top on a bicycle, standard shortest-path routes would make you take the steepest (but shortest) path up the hill. EleNa offers more control over the routing process, by allowing you to decide whether you want to take an easy route.

## Running Instructions
### Quick Start
In order to run Project Elena, install the required python dependencies using `pip install -r requirements.txt` in the `backend/src` directory.
- The following dependencies are needed to run EleNa:
	- osmnx
	- networkx

You must also run the `download-graphs.sh` script in the root of the project to download the required graph cache files. Alternatively, you can also download it here- [cached-graphs.zip](https://www.dropbox.com/s/fgxt8y9eegkyqs7/cached_graphs.zip?dl=0), unzip the file, and place all 3 pickle files in the `backend/data` directory.

Once dependencies have finished installing and you download the cached graphs, navigate to the `backend/src` directory and run `flask run` to start the backend server. The backend server serves both the api for EleNa's processing and the frontend of the webapp.

### Developing the Frontend
The frontend for EleNa is a React app. If wish to run the frontend individually in dev mode, you need to go to the `frontend` directory, then install the dependencies and run the React app. You can use the following commands to do so-
```
yarn install
yarn start
```
Once the development server has started, the webapp development version will open in your default browser.

**Note:** If you wish to build the latest version of the frontend and run it with the Flask app, simply run the `build-frontend.sh` script from the root of the directory.



## How to use EleNa
  
![Screenshot of Elena System](images/elena-screenshot.png)
<p align="center"> <i>Figure 1. The Elena Webapp Graphical User Interface</i></p>

Elena includes a host of features that allow for maximum end user control. These include:
- Algorithm choice: Choose between A Star, Breadth First Search, or Dijkstra Search for your routing algorithm
	- _Note: Breadth First Search does not allow for elevation preferences, as it will simply find a short path to your destination_
- Control over the route through 4 preferences:
	- Maximum/Minimum Steepness: Finds a route with the highest/lowest average grade (steepness) along your path
	- Maximum/Minimum Elevation: Finds a route with the highest/lowest elevation changes in between nodes
- Deviation Limit: Choose how much you would like to deviate from the shortest path to match your route preference
	- A deviation limit of < 5% will just give you the shortest path!
- 3 Choices for Transportation Method:
	- Drive
	- Bike
	- Walk
- A colored route that shows you the parts of the route with steepest ascent _(colored in red)_

Just input a start destination and end destination and generate your route with <b>your</b> preferences
