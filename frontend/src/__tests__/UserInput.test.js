import React from "react";
import ReactDOM from "react-dom";
import UserInput from "./../components/UserInput"

/**
        Test of UserInput.js

	 	Passing Criteria
	 	----------
 		UserInput.js is able to be rendered without crashing
 **/

it("renders without crashing", () => {
	const div = document.createElement("div");
	ReactDOM.render(<UserInput />, div);
});