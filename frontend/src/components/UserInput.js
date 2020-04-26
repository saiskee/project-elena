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

	handleChange = (e) => {
		this.setState({
			[e.target.id]: e.target.value,
		});
	};

	handleSubmit = (e) => {
		e.preventDefault();
		// console.log(this.state);
		// this.setState({ loading: true });
		this.updateLoading()

		// eslint-disable-next-line
		const resp = {
			path: [
				[-71.1188219, 42.373674],
				[-71.1185058, 42.3733081],
				[-71.1193483, 42.3722633],
				[-71.1196139, 42.371766],
				[-71.1188907, 42.3714467],
				[-71.1181625, 42.3711969],
				[-71.117355, 42.3709216],
				[-71.1177529, 42.3702542],
				[-71.1181448, 42.3695963],
				[-71.1173632, 42.3692173],
				[-71.1176905, 42.3689022],
				[-71.1192636, 42.3674198],
				[-71.1190646, 42.3673015],
				[-71.1190093, 42.3673493],
				[-71.1183064, 42.3641648],
				[-71.1181752, 42.3641617],
				[-71.1178261, 42.3641803],
				[-71.1174531, 42.3610148],
				[-71.1159585, 42.3614839],
				[-71.1159469, 42.3613844],
				[-71.1158914, 42.3609058],
				[-71.1158388, 42.3605355],
				[-71.1157603, 42.3599819],
				[-71.1156712, 42.3593559],
				[-71.1156049, 42.3589434],
				[-71.1155893, 42.3588461],
				[-71.1155789, 42.3587842],
				[-71.115466, 42.358271],
				[-71.1153278, 42.357783],
				[-71.1150425, 42.3578433],
				[-71.1148799, 42.3574523],
				[-71.1150374, 42.3574058],
				[-71.1141339, 42.3563464],
				[-71.1140682, 42.3562989],
				[-71.1111139, 42.3546657],
				[-71.1108949, 42.3546324],
				[-71.1111251, 42.3540455],
				[-71.1105129, 42.3534874],
				[-71.1109194, 42.3506323],
				[-71.1096727, 42.350488],
				[-71.1066732, 42.3501335],
				[-71.1065493, 42.3501181],
				[-71.1064049, 42.3501002],
				[-71.1063793, 42.3502285],
				[-71.1062435, 42.3504679],
				[-71.1061893, 42.3508483],
				[-71.1059991, 42.3507388],
				[-71.1055298, 42.3509986],
			],
			name: "Route 1",
			color: [255, 255, 255],
		};
		// this.props.updateData(resp);

		fetch("/route", {
			method: "POST",
			body: JSON.stringify(this.state),
		})
			.then(async (res) => {
				let data = await res.json();
				this.props.updateData(data);
				this.setState({ loading: false });
			})
			.catch((err) => {
				console.log(err);
				this.props.updateErrorMsg(err.toString())
			});
	};

	updateLoading = () => {
		this.props.updateLoading()
	}

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

					<Form.Row hidden={this.state.algorithm == 'Breadth First Search'}>
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

					<Form.Row hidden={this.state.algorithm == 'Breadth First Search'}>
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
