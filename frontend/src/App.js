import React, { Component } from "react";
import "./styles/App.css";

import UserInput from "./components/UserInput";
import MapView from "./components/MapView";

import Container from "react-bootstrap/Container";
import { FlyToInterpolator } from "@deck.gl/core";

class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			data: [],
			viewport: {
				latitude: 42.390357,
				longitude: -72.527814,
				zoom: 14,
				bearing: 0,
				pitch: 0,
			},
			height: "65vh"
		};
		this._onViewStateChange = this._onViewStateChange.bind(this);
	}

	updateData = (d) => {
		console.log("update")
		const resp = []
		resp.push(d)
		this.setState({ data: resp })

		let len = Math.max(Math.floor((d.path.length - 1)/2), 0);
		const coordinates = d.path[len];
		let viewport = this.state.viewport;

		viewport["latitude"] = coordinates[1];
		viewport["longitude"] = coordinates[0];
		viewport["zoom"] = 12.5;
		viewport["transitionDuration"] = 5000;
		viewport["transitionInterpolator"] = new FlyToInterpolator()

		this.setState({ viewport: viewport })
		console.log(this.state)	

		// Required to update viewport 
		this.updateHeight()
	};

	_onViewStateChange({ viewState }) {
		this.setState({ viewport: viewState });
	}

	updateHeight = () => {
		this.setState({height: "66vh"}) 
	}

	

	render() {
		return (
			<div className="App" style={margin}>
				<UserInput updateData={this.updateData} payload={this.state} />
				<Container style={center}>
					<MapView style={margin} data={this.state.data} viewport={this.state.viewport} _onViewStateChange={this._onViewStateChange} height={this.state.height} />
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
