import React, {Component} from "react";
import {withGoogleMap, GoogleMap, Marker, Polyline} from "react-google-maps";

class Map extends Component {
    constructor(props) {
        super(props);
        this.state = {markers: [], currentPath: []};
    }

    render() {

        let drawRoute = async () => {

            const response = await window.fetch('/test', {
                method: 'POST',
                body: JSON.stringify(this.state.markers)
            });

            let res = await response.json();
            console.log(res);
            this.setState({currentPath: res.nodes});
        };

        let addMarker = event => {
            if (this.state.markers.length < 2) {
                let markers = this.state.markers;
                let newMarker = {lat: event.latLng.lat(), lng: event.latLng.lng()};
                markers.push(newMarker);
                console.log(newMarker);
                this.setState({markers: markers});
            }
            if (this.state.markers.length === 2) {
                drawRoute();
            }
        };

        let updateMarker = (index, event) => {
            let markers = this.state.markers;
            markers[index] = {lat: event.latLng.lat(), lng: event.latLng.lng()};
            this.setState({markers: markers});
            if (markers.length === 2) {
                drawRoute();
            }
        };

        const GoogleMapExample = withGoogleMap(props => (
            <GoogleMap
                defaultCenter={{lat: 42.375801, lng: -72.519867}}
                defaultZoom={13}
                onClick={addMarker}
            >
                {this.state.markers.map((pos, index) => (
                    <Marker
                        key={index}
                        draggable={true}
                        onDragEnd={(event) => updateMarker(index, event)}
                        position={pos}
                    />
                ))}
                <Polyline
                    path={
                        this.state.currentPath
                    }
                />
            </GoogleMap>
        ));

        /*
            Add stuff here
          */

        return (
            <div>
                <GoogleMapExample
                    containerElement={<div style={{height: `100vh`, width: "100vw"}}/>}
                    mapElement={<div style={{height: `100%`}}/>}
                />
            </div>
        );
    }
}

export default Map;
