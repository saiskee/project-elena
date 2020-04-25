import React, { Component } from "react";
import "./styles/App.css";

import UserInput from "./components/UserInput";
import RouteData from "./components/RouteData";
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
				latitude: 42.20515744581611,
				longitude: -72.19204888633023,
				zoom: 7.5,
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

		let zoom = this.calculateZoom(d.path);

		viewport["latitude"] = coordinates[1];
		viewport["longitude"] = coordinates[0];
		viewport["zoom"] = zoom;
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
		if(this.state.height === "100vh") {
			this.setState({ height: "99vh", marginTop: "1vh" });
		}
		else {
			this.setState({ height: "100vh", marginTop: "0vh" });
		}
	};

	calculateZoom = (path) => {
		let start = path[0]
		let end = path[path.length - 1]

		let dist = this.haversine(start[1], start[0], end[1], end[0]);

		console.log(dist);

		if(dist <= 1500) {
			return 14.5;
		}
		if(dist <= 5000) {
			return 13;
		}
		if(dist <= 15000) {
			return 12;
		}
		
		return 10;
	}



	haversine = (lat1, lon1, lat2, lon2) => {
		let R = 6371e3; // metres
		let φ1 = lat1 * Math.PI / 180;
		let φ2 = lat2 * Math.PI / 180;
		let Δφ = (lat2-lat1) * Math.PI / 180;
		let Δλ = (lon2-lon1) * Math.PI / 180;

		let a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
				Math.cos(φ1) * Math.cos(φ2) *
				Math.sin(Δλ/2) * Math.sin(Δλ/2);
		let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

		let d = R * c;

		return d
	}

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

					<div style={{position: "absolute", right: "5%", top: "15%"}}>
						<RouteData
							className="routeData"
							data={this.state.data}
						/>
					</div>

				</div>


			</div>
		);
	}
}




export default App;