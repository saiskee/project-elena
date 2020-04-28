import React, { Component } from "react";

import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Spinner from "react-bootstrap/Spinner";

export default class UserInput extends Component {
	state = {
		start: "",
		dest: "",
		goal: "Minimize Elevation Gain",
		limit: "0",
		algorithm: "AStar",
		method: "drive",
	};

	/**
        Sets the state to the value based on the given parameter.

	 	Arguments
	 	----------
	 	e: Event Object
	 		An event object that contains the name of a state and the value it is being set to.

     **/
	handleChange = (e) => {
		this.setState({
			[e.target.id]: e.target.value,
		});
	};

	/**
        Listens for submit button to be pushed fetches the data from the backend. Calls the updateData method from app.js
     **/
	handleSubmit = (e) => {
		e.preventDefault();
		// console.log(this.state);
		// this.setState({ loading: true });
		this.updateLoading();

		fetch("/route", {
			method: "POST",
			body: JSON.stringify(this.state),
		})
			.then(async (res) => {
				if (res.status !== 200){
					let json = await res.json()
					throw new Error(json.error)
				}
				else{
				let data = await res.json();
				this.props.updateData(data);
				this.setState({ loading: false });
				}
			})
			.catch((err) => {
				// console.log(err);
				this.props.updateErrorMsg(err.toString())
			});
	};

	/**
        Calls the updateLoading method in app.js
     **/
	updateLoading = () => {
		this.props.updateLoading()
	};

	/**
        Renders the react components to the screen. In particular, the User Input component.

	 	Returns
	 	----------
	 	The HTML formatted React components to be rendered

     **/
	render() {
		return (
			<Card
				body
				style={{
					width: "400px",
					background: "rgba(0, 0, 0, 0.5)",
					color: "#ffffff",
					marginTop: "2.5%",
					marginLeft: "5%",
				}}
			>
				<Form
					onSubmit={(e) => {
						this.handleSubmit(e);
					}}
				>
					<Form.Row>
						<Form.Group as={Col} controlId="start">
							<Form.Label>Start Location</Form.Label>
							<Form.Control
								type="text"
								placeholder="Enter start location"
								value={this.state.start}
								onChange={(e) => {
									this.handleChange(e);
								}}
							/>
						</Form.Group>
					</Form.Row>

					<Form.Row>
						<Form.Group as={Col} controlId="dest">
							<Form.Label>End Location</Form.Label>
							<Form.Control
								type="text"
								placeholder="Enter end location"
								value={this.state.dest}
								onChange={(e) => {
									this.handleChange(e);
								}}
							/>
						</Form.Group>
					</Form.Row>

					<Form.Row>
						<Form.Group as={Col} controlId="algorithm">
							<Form.Label>Algorithm</Form.Label>
							<Form.Control
								as="select"
								value={this.state.algorithm}
								onChange={(e) => {
									this.handleChange(e);
								}}
							>
								{/* <option>Uniform Cost Search</option> */}
								<option>AStar</option>
								{/* <option>AStar (Old)</option> */}
								<option>Breadth First Search</option>
								<option>Dijkstra</option>
								
							</Form.Control>
						</Form.Group>
					</Form.Row>

					<Form.Row hidden={this.state.algorithm === 'Breadth First Search'}>
						<Form.Group as={Col} controlId="goal">
							<Form.Label>Optimization</Form.Label>
							<Form.Control
								as="select"
								value={this.state.goal}
								onChange={(e) => {
									this.handleChange(e);
								}}
							>
								<option>Minimize Elevation Gain</option>
								<option>Maximize Elevation Gain</option>
								<option>Maximize Steepness</option>
								<option>Minimize Steepness</option>
							</Form.Control>
						</Form.Group>
					</Form.Row>

					<Form.Row hidden={this.state.algorithm === 'Breadth First Search'}>
						<Form.Group as={Col} controlId="limit">
							<Form.Label>Deviation Limit (x%)</Form.Label>
							<Form.Control
								type="number"
								placeholder="x%"
								value={this.state.limit}
								onChange={(e) => {
									this.handleChange(e);
								}}
							/>
						</Form.Group>
					</Form.Row>

					<Form.Row>
						<Form.Group as={Col} controlId="method">
							<Form.Label>Transportation Method</Form.Label>
							<Form.Control
								as="select"
								// disabled
								value={this.state.method}
								onChange={(e) => {
									this.handleChange(e);
								}}
							>
								<option>drive</option>
								<option>bike</option>
								<option>walk</option>
							</Form.Control>
						</Form.Group>
					</Form.Row>
					<Form.Row className="justify-content-md-center">
						<Button variant="light" type="submit">
							{this.props.loading ? (
								<Spinner animation="border" />
							) : (
								"Submit"
							)}
						</Button>
					</Form.Row>
				</Form>
			</Card>
		);
	}
}
