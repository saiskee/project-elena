import React, { Component } from "react";

import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import { Line } from "react-chartjs-2";

const options = {
	scales: {
		xAxes: [
			{
				ticks: {
					display: false, //this will remove only the label
				},
			},
		],
	},
};

const legendOpts = {
	display: false,
};

const testData = {
	labels: [],
	datasets: [
		{
			label: "",
			fill: false,
			lineTension: 0.1,
			backgroundColor: "rgba(75,192,192,0.4)",
			borderColor: "rgba(75,192,192,1)",
			borderCapStyle: "butt",
			borderDash: [],
			borderDashOffset: 0.0,
			borderJoinStyle: "miter",
			pointBorderColor: "rgba(75,192,192,1)",
			pointBackgroundColor: "#fff",
			pointBorderWidth: 1,
			pointHoverRadius: 5,
			pointHoverBackgroundColor: "rgba(75,192,192,1)",
			pointHoverBorderColor: "rgba(220,220,220,1)",
			pointHoverBorderWidth: 2,
			pointRadius: 1,
			pointHitRadius: 10,
			data: [10, 11],
		},
	],
};

let finalDistance = 0;
let maxElevation = 0;
let maxEleClimb = 0;
let datas = [];

export default class RouteData extends Component {
	update = (dataPoints) => {
		if (dataPoints.length === 0) {
			return;
		}
		let path = dataPoints[0].path;
		let path_data = dataPoints[0].path_data;

		let label = [];
		let elevData = [];
		let total_Dist = 0;
		let maxElev = 0;

		for (let i = 0; i < path.length; i++) {
			let long = path[i][0];
			let lat = path[i][1];
			let dist = path_data[i].length;
			let elev = path_data[i].elevation;

			total_Dist += dist;
			if (elev > maxElev) {
				maxElev = elev;
			}

			if (i !== path.length - 1) {
				let nextEle = path_data[i + 1].elevation;

				if (nextEle - elev > maxEleClimb) {
					maxEleClimb = nextEle - elev;
				}
			}

			label.push(lat + ", " + long);
			elevData.push(elev);
		}

		console.log(elevData, testData.datasets[0].data);

		testData.labels = label;
		testData.datasets[0].data = elevData;

		finalDistance = total_Dist;
		maxElevation = maxElev;
	};

	render() {
		// data[0].path is {long, lat, dist, elevation}
		let dataPoints = this.props.data;

		if (dataPoints !== datas) {
			this.update(dataPoints);
			datas = dataPoints;
		}

		return (
			<Card
				body
				style={
					finalDistance === 0
						? {
								width: "350px",
								background: "rgba(0, 0, 0, 0.5)",
								color: "#ffffff",
								marginTop: "5%",
								marginLeft: "5%",
								opacity: 0,
						  }
						: {
								width: "350px",
								background: "rgba(0, 0, 0, 0.75)",
								color: "#ffffff",
								marginTop: "5%",
								marginLeft: "5%",
								opacity: 100,
						  }
				}
			>
				<Form>
					<Form.Row>
						<Form.Group as={Col} controlId="totalDist">
							<Form.Label>Total Distance</Form.Label>
							<br />
							<Form.Label>
								{finalDistance.toFixed(3)} Meters
							</Form.Label>
						</Form.Group>
					</Form.Row>

					<Form.Row>
						<Form.Group as={Col} controlId="dest">
							<Form.Label>Maximum Elevation</Form.Label>
							<br />
							<Form.Label>{maxElevation}</Form.Label>
						</Form.Group>
					</Form.Row>

					<Form.Row>
						<Form.Group as={Col} controlId="dest">
							<Form.Label>
								Greatest Elevation Climbed At Once
							</Form.Label>
							<br />
							<Form.Label>{maxEleClimb}</Form.Label>
						</Form.Group>
					</Form.Row>

					<Form.Row>
						<Form.Group as={Col} controlId="graph">
							<Form.Label>Elevation Graph</Form.Label>
							<Line
								data={testData}
								legend={legendOpts}
								options={options}
							/>
						</Form.Group>
					</Form.Row>
				</Form>
			</Card>
		);
	}
}
