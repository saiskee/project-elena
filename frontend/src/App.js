import React, { Component } from "react";
import "./styles/App.css";

import UserInput from "./components/UserInput";
import MapView from "./components/MapView";

import { FlyToInterpolator } from "@deck.gl/core";

import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";

class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			data: [],
			viewport: {
				latitude: 30.22,
				longitude: -60.13,
				zoom: 1.3,
				bearing: 0,
				pitch: 0,
			},
			height: "99vh",
			width: "100vw",
			marginTop: "1vh"
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
		this.setState({ height: "100vh", marginTop: "0vh" });
	};

	render() {
		return (
			<div
				className="App"
				style={
					
					{ background: "rgb(23, 24, 24)", position: "relative", alignItems: "bottom" }
				}
			>
				<div style={{ zIndex: 0, position: "absolute" }}>
					<MapView
						data={this.state.data}
						viewport={this.state.viewport}
						_onViewStateChange={this._onViewStateChange}
						height={this.state.height}
						width={this.state.width}
						marginTop={this.state.marginTop}
					/>
				</div>
				<div style={{ zIndex: 9, height: "100vh" }}>
					<Navbar
						variant="dark"
						style={{ height: "8vh", background: "rgba(0, 0, 0, 0.5)", }}
						className="ml-auto"
					>
						<Navbar.Brand style={{ marginLeft: "15px" }}>
							EleNa: Elevation-based Navigation
						</Navbar.Brand>
						<Nav className="ml-auto">
							<Navbar.Text>Created by-</Navbar.Text>
							<Nav.Link href="">Nilay</Nav.Link>
							<Nav.Link href="">Max</Nav.Link>
							<Nav.Link href="">Meghna</Nav.Link>
							<Nav.Link href="">Sai</Nav.Link>
							<Nav.Link
								href="https://github.com"
								style={{ borderLeft: "solid 1px grey" }}
							>
								Github
							</Nav.Link>
						</Nav>
					</Navbar>
					<div>
						<UserInput
							className="userInput"
							updateData={this.updateData}
							payload={this.state}
						/>
					</div>
				</div>
			</div>
		);
	}
}




export default App;
