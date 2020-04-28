import React, { Component } from "react";
import "./styles/App.css";

import UserInput from "./components/UserInput";
import RouteData from "./components/RouteData";
import MapView from "./components/MapView";
import ErrorModal from "./components/ErrorModal";

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
			marginTop: "1vh",
			errorMsg: "No errors",
			showError: false,
			loading: false
		};
		this._onViewStateChange = this._onViewStateChange.bind(this);
	}

	/**
        Updates the viewport, loading screen, and the height of the map

        Arguments
        ----------
        d: HTTP Response
	 		The HTTP Response from the backend

     **/
	updateData = (d) => {
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

		this.updateLoading();

		// Required to update viewport
		this.updateHeight();
	};

	/**
        Listens for a state change from the viewport and sets it's state

        Arguments
        ----------
        viewState: Viewport
	 		The updated viewport

     **/
	_onViewStateChange({ viewState }) {
		this.setState({ viewport: viewState });
	}

	/**
        Updates the height. This is required to update the viewport correctly.
     **/
	updateHeight = () => {
		if (this.state.height === "100vh") {
			this.setState({ height: "99vh", marginTop: "1vh" });
		} else {
			this.setState({ height: "100vh", marginTop: "0vh" });
		}
	};

	/**
        Update the error message and shows the error dialog.

        Arguments
        ----------
        msg: String
	 		The error message.

     **/
	updateErrorMsg = (msg) => {
		this.setState({ errorMsg: msg, showError: true });
	};

	/**
        Toggles the loading screen.
     **/
	updateLoading = () => {
		let bool = this.state.loading;
		this.setState({ loading: !bool });
	};

	/**
        Removes the error and hides the error dialog.
     **/
	clearError = () => {
		this.setState({ errorMsg: "No errors", showError: false });
		this.updateLoading()
	};

	/**
        Calculates the proper map zoom level based on the haversine formula for the path length

        Arguments
        ----------
        path: [[long, lat]]
	 		The path to be displayed

	 	Returns
	 	----------
	 	The calculated zoom level.

     **/
	calculateZoom = (path) => {
		let start = path[0];
		let end = path[path.length - 1];

		let dist = this.haversine(start[1], start[0], end[1], end[0]);

		console.log("dist: " + dist);

		if (dist <= 1500) {
			return 14;
		}
		if (dist <= 5000) {
			return 12;
		}
		if (dist <= 15000) {
			return 11.5;
		}
		if (dist <= 35000) {
			return 11;
		}
		if (dist <= 65000) {
			return 10;
		}
		return 8;
	};

	/**
        Calculates haversine formula for the great-circle distance between two points on the earth

        Arguments
        ----------
        lat1: Float
	 		Latitude of the first node.
	 	lon1: Float
	 		Longitude of the first node.
	 	lat2: Float
	 		Latitude of the second node.
	 	long2: Float
	 		Longitude of the second node.

	 	Returns
	 	----------
	 	d: The haversine distance between the two points.

     **/
	haversine = (lat1, lon1, lat2, lon2) => {
		let R = 6371e3; // metres
		let φ1 = (lat1 * Math.PI) / 180;
		let φ2 = (lat2 * Math.PI) / 180;
		let Δφ = ((lat2 - lat1) * Math.PI) / 180;
		let Δλ = ((lon2 - lon1) * Math.PI) / 180;

		let a =
			Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
			Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
		let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

		let d = R * c;

		return d;
	};

	/**
        Renders the react components to the screen.

	 	Returns
	 	----------
	 	The HTML formatted React components to be rendered

     **/
	render() {
		return (
			<div
				className="App"
				style={{
					background: "rgb(23, 24, 24)",
					position: "relative",
					alignItems: "bottom",
				}}
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
						style={{
							height: "8vh",
							background: "rgba(0, 0, 0, 0.5)",
						}}
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

					<ErrorModal
						showError={this.state.showError}
						errorMsg={this.state.errorMsg}
						clearError={this.clearError}
					/>

					<div>
						<UserInput
							className="userInput"
							updateData={this.updateData}
							payload={this.state}
							updateErrorMsg={this.updateErrorMsg}
							loading={this.state.loading}
							updateLoading = {this.updateLoading}
						/>
					</div>

					<div
						style={{
							position: "absolute",
							right: "5%",
							top: "12.5%",
						}}
					>
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
