import React from "react";
import ReactDOM from "react-dom";
import App from "./../App"

/**
        Test to make sure the React app compiles

	 	Passing Criteria
	 	----------
	 	The app is able to be rendered without crashing
 **/
it("renders without crashing", () => {
	const div = document.createElement("div");
	ReactDOM.render(<App />, div);
});