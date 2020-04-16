import React, { Component } from "react";
import "./styles/App.css";

import UserInput from "./components/UserInput";
import MapView from "./components/MapView";

import { FlyToInterpolator } from "@deck.gl/core";

import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			data: [],
			viewport: {
				latitude: 39.537849,
				longitude: 6.682261,
				zoom: 1.3,
				bearing: 0,
				pitch: 0,
			},
			height: "92vh",
			width: "66.6666vw",
			colWid: 4,
		};
		this._onViewStateChange = this._onViewStateChange.bind(this);
	}

	updateData = (d) => {
		console.log("update");
		const resp = [];
		resp.push(d);
		this.setState({ data: resp });

		let len = Math.max(Math.floor((d.path.length - 1) / 2), 0);
		const coordinates = d.path[len];
		let viewport = this.state.viewport;

		viewport["latitude"] = coordinates[1];
		viewport["longitude"] = coordinates[0];
		viewport["zoom"] = 12.5;
		viewport["transitionDuration"] = 5000;
		viewport["transitionInterpolator"] = new FlyToInterpolator();

		this.setState({ viewport: viewport });
		console.log(this.state);

		// Required to update viewport
		this.updateHeight();
	};

	_onViewStateChange({ viewState }) {
		this.setState({ viewport: viewState });
	}

	updateHeight = () => {
		this.setState({ colWid: 3, width: "75vw" });
		// this.setState({ height: "92vh" });
	};

	render() {
		return (
			<div className="App" style={(margin, { background: "#181919" })}>
				<Navbar
					variant="dark"
					style={{ height: "8vh" }}
					className="ml-auto"
				>
					<Navbar.Brand style={{ marginLeft: "15px" }}>
						EleNa: Elevation-based Navigation
					</Navbar.Brand>
					<Nav className="ml-auto">
						<Navbar.Text>
							Created by-
						</Navbar.Text>
						<Nav.Link href="">
							Nilay
						</Nav.Link>
						<Nav.Link href="">
							Max
						</Nav.Link>
						<Nav.Link href="">
							Meghna
						</Nav.Link>
						<Nav.Link href="">
							Sai
						</Nav.Link>
						<Navbar.Text>
							|
						</Navbar.Text>
						<Nav.Link href="https://github.com">Github</Nav.Link>
					</Nav>
				</Navbar>
				<Row style={{ width: "100vw", height: "92vh" }}>
					<Col md={this.state.colWid} bg="dark" style={center}>
						<UserInput
							updateData={this.updateData}
							payload={this.state}
						/>
					</Col>
					<Col style={right}>
						<MapView
							style={margin}
							data={this.state.data}
							viewport={this.state.viewport}
							_onViewStateChange={this._onViewStateChange}
							height={this.state.height}
							width={this.state.width}
						/>
						{/* Hello */}
					</Col>
				</Row>
			</div>
		);
	}
}

const center = {
	display: "flex",
	alignItems: "center",
	justifyContent: "center",
	textAlign: "center",
};

const right = {
	display: "flex",
	justifyContent: "right",
	textAlign: "right",
	// position: "absolute",
	right: "0px",
};

const margin = {
	// marginBottom: "15px",
	// paddingBottom: "1em",
};

export default App;
