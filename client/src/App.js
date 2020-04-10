import React from "react";
import "./styles/App.css";
import UserInput from "./components/UserInput";

import MapView from "./components/MapView";

import Container from "react-bootstrap/Container";

function App() {
	return (
		<div className="App" style={height}>
			<UserInput />
			<Container>
				<MapView />
			</Container>
		</div>
	);
}

const height = {
	height: "120vh",
};

export default App;
