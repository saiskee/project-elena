import React, { Component } from "react";

import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";

import InputSection from "./InputSection";

export default class UserInput extends Component {
	render() {
		return (
			<div style={height}>
				<Navbar bg="dark" variant="dark">
					<Container>
						<Navbar.Brand href="#home">
							EleNa: Elevation-based Navigation
						</Navbar.Brand>
					</Container>
				</Navbar>
				<Container >
					<InputSection />
				</Container>
			</div>
		);
	}
}


const height = {
	height: "25vh",
	marginBottom: "30px"
}
