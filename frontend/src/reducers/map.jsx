// components/Map.jsx
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import L from 'leaflet';

const Map = ({ geocodeResults, mapState }) => {
  useEffect(() => {
    const map = L.map('map').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);

    // Add geocoding results to the map
    if (geocodeResults.length) {
      geocodeResults.forEach((result) => {
        L.marker([result.lat, result.lng]).addTo(map);
      });
    }
  }, [geocodeResults]);

  return <div id="map" style={{ height: '500px' }} />;
};

const mapStateToProps = (state) => ({
  geocodeResults: state.geocode.results,
  mapState: state.map,
});

export default connect(mapStateToProps)(Map);
