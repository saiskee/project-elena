import React from "react";
import DeckGL from "@deck.gl/react";
import { PathLayer } from "@deck.gl/layers";
import { StaticMap } from "react-map-gl";

// Set your mapbox access token here
const MAPBOX_TOKEN =
	"pk.eyJ1IjoibmlsYXkxODA4IiwiYSI6ImNrOG1iaXp0cjBkeTEzZm12N3l3ODJweWEifQ.TDhSzGcCsjt5CsVRljpcrw";

// Data to be used by the LineLayer
// const data =

export default class MapView extends React.Component {

	render() {
		const data = this.props.data;

		const layer = new PathLayer({
			id: "path-layer",
			data,
			pickable: true,
			widthScale: 5,
			widthMinPixels: 2,
		});

		return (
			<DeckGL
				// initialViewState={this.props.viewport}
				viewState={this.props.viewport}
				onViewStateChange={v => {
					this.props._onViewStateChange(v)
				}}
				controller={true}
				layers={layer}
				width="60vw"
				height={this.props.height}
				style={{ top: "auto", left: "auto", zIndex: "0", marginBottom: "3em" }}
			>
				<StaticMap
					mapStyle="mapbox://styles/mapbox/outdoors-v11"
					onViewportChange={(viewport) => this.setState({ viewport })}
					mapboxApiAccessToken={MAPBOX_TOKEN}
					
				/>
			</DeckGL>
		);
	}
}
