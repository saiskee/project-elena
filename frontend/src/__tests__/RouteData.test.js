import React from "react";
import ReactDOM from "react-dom";
import RouteData from "./../components/RouteData"

/**
        Test of RouteData.js

	 	Passing Criteria
	 	----------
 		RouteData.js is able to be rendered without crashing
 **/

describe('Testing RouteData.js', () => {
	it("renders without crashing", () => {
		// DOM Target element
		const div = document.createElement("div");

		// Initial Props
		const data = [];

		// Test Rendering
		ReactDOM.render(<RouteData data={data} />, div);
	})
});
