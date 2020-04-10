import React, { Component } from "react";

import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

export default class InputSection extends Component {
	render() {
		return (
			<div style={padding}>
				<Row>
					<Col>
						<Form>
							<Form.Row>
								<Form.Group as={Col} controlId="start_loc">
									<Form.Label>Start Location</Form.Label>
									<Form.Control
										type="text"
										placeholder="Enter start location"
									/>
								</Form.Group>

								<Form.Group as={Col} controlId="end_loc">
									<Form.Label>End Location</Form.Label>
									<Form.Control
										type="text"
										placeholder="Enter end location"
									/>
								</Form.Group>

								<Form.Group
									as={Col}
									controlId="exampleForm.ControlSelect1"
								>
									<Form.Label>Optimization</Form.Label>
									<Form.Control as="select">
										<option>Minimize Elevation Gain</option>
										<option>Maximize Elevation Gain</option>
									</Form.Control>
								</Form.Group>

								<Form.Group as={Col} controlId="end_loc">
									<Form.Label>
										Deviation Limit (x%)
									</Form.Label>
									<Form.Control
										type="number"
										placeholder="x%"
									/>
								</Form.Group>
							</Form.Row>

							<Form.Row className="justify-content-md-center">
								<Button variant="primary" type="submit">
									Submit
								</Button>
							</Form.Row>
						</Form>
					</Col>
				</Row>
			</div>
		);
	}
}

const padding = {
	marginTop: "15px",
};
