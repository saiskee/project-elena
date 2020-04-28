import React from "react";
import ReactDOM from "react-dom";
import MapView from "./../components/MapView";

/**
        Test of MapView.js

	 	Passing Criteria
	 	----------
 		MapView.js is able to be rendered without crashing
 **/

describe("Testing MapView.js", () => {
	it("renders without crashing", () => {
		// DOM Target element
		const div = document.createElement("div");

		// Initial Props
		const data = [];
		const viewport = {
			latitude: 42.20515744581611,
			longitude: -72.19204888633023,
			zoom: 7.5,
			bearing: 0,
			pitch: 0,
		};
		const height = "99vh";
		const width = "100vw";
		const marginTop = "1vh";
		const _onViewStateChange = () => {};

		ReactDOM.render(
			<MapView
				data={data}
				viewport={viewport}
				_onViewStateChange={_onViewStateChange}
				height={height}
				width={width}
				marginTop={marginTop}
			/>,
			div
		);
	});
});
