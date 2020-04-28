import React, { Component } from "react";

import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

export default class ErrorModal extends Component {
	/**
        Renders the react components to the screen. In particular, the error modal.

	 	Returns
	 	----------
	 	The HTML formatted React components to be rendered

     **/
	render() {
		return (
			<Modal show={this.props.showError}>
				<Modal.Header>
					<Modal.Title>Error</Modal.Title>
				</Modal.Header>

				<Modal.Body>
					<p>{this.props.errorMsg}</p>
				</Modal.Body>

				<Modal.Footer>
					<Button variant="danger" onClick={() => {
						this.props.clearError()
					}}>Close</Button>
				</Modal.Footer>
			</Modal>
		);
	}
}
