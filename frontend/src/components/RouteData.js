import React, { Component } from "react";

import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import { Line } from "react-chartjs-2";

/*
    Options and configurations for the Chart.js graph
 */
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

let datas = [];
let finalDistance = 0;
let maxGrade = 0;
let averageGrade = 0;
let totalElevationGain = 0;
export default class RouteData extends Component {

    /**
        Calculates statistics that will be displayed

        Arguments
        ----------
        dataPoints: The json object that was passed to the frontend from the backend.

     **/
    update = (dataPoints) => {
        
        finalDistance = 0;
        averageGrade = 0;
        totalElevationGain = 0;

        if (dataPoints.length === 0) {
            return
        }
        // data[0].path is [[long, lat]]
        // data[0].path_data is [{elevation, length}]
        let path = dataPoints[0].path;
        let path_data = dataPoints[0].path_data;

        let label = [];
        let elevData = [];
        let total_Dist = 0;
        maxGrade = 0;

        for (let i = 0; i < path.length; i++) {

            let long = path[i][0];
            let lat = path[i][1];
            let dist = path_data[i].length;
            let grade = path_data[i].grade;
            let elev = path_data[i].elevation;

            total_Dist += dist;
            if (grade > maxGrade) {
                maxGrade = grade;
            }

            if (i !== path.length - 1) {
                averageGrade += grade;
                if ((path_data[i+1].elevation - elev) > 0){
                    totalElevationGain += (path_data[i+1].elevation - elev);
                }
            }
            

            label.push(lat + ", " + long);
            elevData.push(elev);
        }

        console.log(elevData, testData.datasets[0].data);

        testData.labels = label;
        testData.datasets[0].data = elevData;
        averageGrade /= path.length;
        finalDistance = total_Dist;
    };

    render() {


        let dataPoints = this.props.data;

        // Only update data if it is new
        if (dataPoints !== datas) {
            this.update(dataPoints);
            datas = dataPoints;
        }


        return (
            <Card
                body
                style={finalDistance === 0 ?
                    {
                        width: "350px",
                        background: "rgba(0, 0, 0, 0.5)",
                        color: "#ffffff",
                        marginTop: "5%",
                        marginLeft: "5%",
                        opacity: 0
                    } : {
                        width: "350px",
                        background: "rgba(0, 0, 0, 0.75)",
                        color: "#ffffff",
                        marginTop: "5%",
                        marginLeft: "5%",
                        opacity: 100
                    }}
            >
                <Form>
                    <Form.Row>
                        <Form.Group as={Col}
                                    controlId="totalDist">
                            <Form.Label>Total Distance</Form.Label>
                            <br/>
                            <Form.Label>{(finalDistance/1000).toFixed(3)} Kilometers</Form.Label>
                        </Form.Group>
                    </Form.Row>

                    <Form.Row>
                        <Form.Group as={Col} controlId="dest">
                            <Form.Label>Steepest Incline</Form.Label>
                            <br/>
                            <Form.Label>{(maxGrade * 10).toFixed(3)} Vertical Meters per 10 Meters</Form.Label>
                        </Form.Group>
                    </Form.Row>

                     <Form.Row>
                        <Form.Group as={Col} controlId="dest">
                            <Form.Label>Total Elevation Gain</Form.Label>
                            <br/>
                            <Form.Label>{totalElevationGain} Meters</Form.Label>
                        </Form.Group>
                    </Form.Row>

                    <Form.Row>
                        <Form.Group as={Col} controlId="dest">
                            <Form.Label>Average Incline</Form.Label>
                            <br/>
                            <Form.Label>{(averageGrade * 10).toFixed(3)} Vertical Meters per 10 Meters</Form.Label>
                        </Form.Group>
                    </Form.Row>

                    <Form.Row>
                        <Form.Group as={Col} controlId="graph">
                            <Form.Label>Elevation Graph</Form.Label>
                            <Line data={testData} legend={legendOpts} options={options}/>
                        </Form.Group>
                    </Form.Row>
                </Form>
            </Card>
        );
    }
}
