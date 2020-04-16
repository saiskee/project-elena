import React, { Component } from "react";
import "./styles/App.css";
import UserInput from "./components/UserInput";

import MapView from "./components/MapView";

import Container from "react-bootstrap/Container";

class App extends Component {
	state = {
		data: [],
		viewport: {
			latitude: 42.3505,
			longitude: -71.1054,
			zoom: 13,
			bearing: 0,
			pitch: 0,
		},
	};

	updateData = (d) => {
		console.log("update")
		const resp = []
		resp.push(d)
		this.setState({ data: resp })
		
		const coordinates = d.path[0];

		console.log(coordinates)

		let viewport = this.state.viewport;

		viewport["latitude"] = coordinates[1];
		viewport["longitude"] = coordinates[0];

		this.setState({ viewport: viewport })

		console.log(this.state)	
	};

	

	render() {
		return (
			<div className="App" style={margin}>
				<UserInput updateData={this.updateData} payload={this.state} />
				<Container style={center}>
					<MapView style={margin} data={this.state.data} viewport={this.state.viewport} />
				</Container>
			</div>
		);
	}
}



const center = {
	display: "flex",
	justifyContent: "center",
	textAlign: "center",
};

const margin = {
	marginTop: "15px",
	marginBottom: "15px",
	paddingBottom: "1em",
};

export default App;
