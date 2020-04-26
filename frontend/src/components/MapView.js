import React from "react";
import DeckGL from "@deck.gl/react";
import { PathLayer } from "@deck.gl/layers";
import { StaticMap } from "react-map-gl";

// Set your mapbox access token here
const MAPBOX_TOKEN =
	"pk.eyJ1IjoibmlsYXkxODA4IiwiYSI6ImNrOG1iaXp0cjBkeTEzZm12N3l3ODJweWEifQ.TDhSzGcCsjt5CsVRljpcrw";

export default class MapView extends React.Component {
	render() {
		const data = this.props.data;

		function perc2color(perc) {
			let r, g, b = 0;
			if (perc < 50) {
				g = 255;
				r = Math.round(5.1 * perc);
			} else {
				r = 255;
				g = Math.round(510 - 5.1 * perc);
			}
			return [r, g, b];
		}

		const renderColor = (item, min, max) => {
			// get max and min grades
			let grade = item.path_data[0].elevation; // between max and min
			let grade_percent = ((grade - min) * 100) / (max - min);
			return perc2color(grade_percent);
		};

		const pathLayers = [];
		if (data[0] && data[0].path) {
			let d = data[0];
			let min_grade = Number.POSITIVE_INFINITY;
			let max_grade = Number.NEGATIVE_INFINITY;
			for (let path of d.path_data) {
				if (path.elevation < min_grade) {
					min_grade = path.elevation;
				}
				if (path.elevation > max_grade) {
					max_grade = path.elevation;
				}
			}
			for (let i = 0; i < d.path.length - 1; i++) {
				let newData = [
					{
						color: d.color,
						name: d.name,
						path: d.path.slice(i, i + 2),
						path_data: d.path_data.slice(i, i + 2),
					},
				];
				const newLayer = new PathLayer({
					id: "path-layer" + String(i),
					data: newData,
					pickable: true,
					widthScale: 5,
					widthMinPixels: 2,
					getColor: (item) => renderColor(item, min_grade, max_grade),
				});
				pathLayers.push(newLayer);
			}
		}

		let style = {
			top: "auto",
			left: "auto",
			zIndex: "0",
			marginTop: this.props.marginTop,
		};

		return (
			<DeckGL
				// initialViewState={this.props.viewport}
				viewState={this.props.viewport}
				onViewStateChange={(v) => {
					this.props._onViewStateChange(v);
				}}
				controller={true}
				layers={pathLayers}
				width={this.props.width}
				height={this.props.height}
				style={style}
			>
				<StaticMap
					mapStyle="mapbox://styles/mapbox/dark-v10"
					onViewportChange={(viewport) => this.setState({ viewport })}
					mapboxApiAccessToken={MAPBOX_TOKEN}
				/>
			</DeckGL>
		);
	}
}
