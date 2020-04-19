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
		

		function perc2color(perc) {
			var r, g, b = 0;
			if(perc < 50) {
				g = 255;
				r = Math.round(5.1 * perc);
			}
			else {
				r = 255;
				g = Math.round(510 - 5.10 * perc);
			}
			
			return [r, g, b];
		}

		const renderColor = (item, min, max) => {
			// get max and min grades
			let grade = item.path[0][2] // between max and min
			let grade_percent = (grade - min) * 100 / (max - min)
			return perc2color(grade_percent)
		}
		
		const pathLayers = []
		if (data[0] && data[0].path){
			let d = data[0]
			let min_grade = Number.POSITIVE_INFINITY;
			let max_grade = Number.NEGATIVE_INFINITY;
			for (let path of d.path){
				if (path[2] < min_grade){
					min_grade = path[2]
				}
				if (path[2] > max_grade){
					max_grade = path[2]
				}
			}
			for (let i = 0; i < d.path.length-1; i++){
				let newData = [{color: d.color, name: d.name, path: d.path.slice(i, i+2)}]
				const newLayer = new PathLayer({
					id: "path-layer" + String(i),
					data: newData,
					pickable: true,
					widthScale: 5,
					widthMinPixels: 2,
					getColor: (item) => renderColor(item, min_grade, max_grade),

				})
				pathLayers.push(newLayer)
			}
		}

		const path = new PathLayer({
			id: "path-layer",
			data,
			pickable: true,
			widthScale: 5,
			widthMinPixels: 2,
			getColor: renderColor,
		});

		const startPinData = [
			{
				name: "Colma (COLM)",
				address: "365 D Street, Colma CA 94014",
				exits: 4214,
				coordinates: [42.20515744581611, -72.19204888633023],
			},
		];

		const ICON_MAPPING = {
			marker: {x: 0, y: 0, width: 32, height: 32, mask: true}
		  };

		const startPin = new IconLayer({
			id: "icon-layer",
			startPinData,
			pickable: true,
			// iconAtlas and iconMapping are required
			// getIcon: return a string
			getIcon: d => ({
				url: "https://img.icons8.com/color/50/000000/map-pin.png",
				width: 128,
				height: 128,
				anchorY: 128
			  }),
		
			getIcon: d => 'marker',

			sizeScale: 15,
			getPosition: d => d.coordinates,
			getSize: d => 5,
			getColor: d => [Math.sqrt(d.exits), 140, 0],
		});

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
				layers={ pathLayers }
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
