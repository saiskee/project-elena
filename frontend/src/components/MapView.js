import React from "react";
import DeckGL from "@deck.gl/react";
import { PathLayer, IconLayer } from "@deck.gl/layers";
import { StaticMap } from "react-map-gl";

// Set your mapbox access token here
const MAPBOX_TOKEN =
	"pk.eyJ1IjoibmlsYXkxODA4IiwiYSI6ImNrOG1iaXp0cjBkeTEzZm12N3l3ODJweWEifQ.TDhSzGcCsjt5CsVRljpcrw";

// Data to be used by the LineLayer
// const data =

export default class MapView extends React.Component {

	render() {
		const data = this.props.data;

		const path = new PathLayer({
			id: "path-layer",
			data,
			pickable: true,
			widthScale: 5,
			widthMinPixels: 2,
			getColor: [255, 255, 255]
		});

		const iconTest =  [
				{name: 'Colma (COLM)', address: '365 D Street, Colma CA 94014', exits: 4214, coordinates: [-122.466233, 37.684638]},
			]

		const iconLayer = new IconLayer({
			id: 'icon-layer',
			data,
			pickable: true,
		})

		return (
			<DeckGL
				// initialViewState={this.props.viewport}
				viewState={this.props.viewport}
				onViewStateChange={v => {
					this.props._onViewStateChange(v)
				}}
				controller={true}
				layers={path}
				width={this.props.width}
				height={this.props.height}
				style={{ top: "auto", left: "auto", zIndex: "0" }}
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
