import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// Override the default marker icon with correct paths
let DefaultIcon = L.icon({
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
  iconSize: [25, 41], // Size of the icon
  iconAnchor: [12, 41], // Anchor the icon to the map position
  popupAnchor: [1, -34], // Popup position relative to the icon
  shadowSize: [41, 41], // Size of the shadow
});

// Set the default marker icon to the one we defined
L.Marker.prototype.options.icon = DefaultIcon;

const Map = ({ locations, zoomLevel, setZoomLevel }) => {
  const [geojsonData, setGeojsonData] = useState(null);

  // Fetch the GeoJSON data when the component mounts
  useEffect(() => {
    const fetchGeoJSON = async () => {
      try {
        const response = await fetch('/aligned_non_overlapping_map.geojson');  // Adjust the path if needed
        if (response.ok) {
          const data = await response.json();
          setGeojsonData(data);
        } else {
          console.error('Failed to fetch GeoJSON data');
        }
      } catch (error) {
        console.error('Error loading GeoJSON:', error);
      }
    };

    fetchGeoJSON();
  }, []);

  // Assign different colors based on the properties of each feature
  const getRegionColor = (regionName) => {
    switch (regionName) {
      case 'Northern Norway':
        return '#FF5733'; // Red
      case 'Middle Norway':
        return '#33FF57'; // Green
      case 'Western Norway':
        return '#3357FF'; // Blue
      case 'Eastern Norway':
        return '#FF33FF'; // Pink
      case 'Southern Norway':
        return '#FFFF33'; // Yellow
      default:
        return '#333333'; // Default color (Gray)
    }
  };

  // Dynamically style GeoJSON features
  const geojsonStyle = (feature) => {
    const regionName = feature.properties.name;  // Assuming the region name is stored in the 'name' property
    return {
      color: getRegionColor(regionName), // Border color
      weight: 2,
      fillColor: getRegionColor(regionName), // Fill color
      fillOpacity: 0.4,
    };
  };

  // Optional popup or interaction for GeoJSON features
  const onEachFeature = (feature, layer) => {
    if (feature.properties && feature.properties.name) {
      layer.bindPopup(`<p>${feature.properties.name}</p>`);
    }
  };

  return (
    <div className="map-container">
      <MapContainer
        center={[63.4305, 10.3951]} // Center on Trondheim (midpoint)
        zoom={zoomLevel}
        style={{ height: '100%', width: '100%' }}
        whenCreated={(map) => {
          map.on('zoomend', () => {
            setZoomLevel(map.getZoom());
          });
        }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {/* Render a marker for each location */}
        {locations.map((location, index) => (
          <Marker 
            key={index} 
            position={location.coordinates}
            eventHandlers={{
              click: () => console.log('Marker clicked:', location),  // Simple logging for now
            }}
          >
            <Popup>
              <div>
                <p>Region: {location.region}</p>  {/* Region name */}
                <p>Price (NOK/kWh): {location.prices?.[0]?.NOK_per_kWh || 'N/A'}</p>
                <p>Price (EUR/kWh): {location.prices?.[0]?.EUR_per_kWh || 'N/A'}</p>
                <p>Exchange Rate: {location.prices?.[0]?.EXR || 'N/A'}</p>
                <p>Time Start: {location.prices?.[0]?.time_start || 'N/A'}</p>
                <p>Time End: {location.prices?.[0]?.time_end || 'N/A'}</p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Render the GeoJSON data if it's loaded */}
        {geojsonData && (
          <GeoJSON
            data={geojsonData}
            style={geojsonStyle}  // Apply the dynamic styles
            onEachFeature={onEachFeature}  // Attach popups
          />
        )}
        
      </MapContainer>
    </div>
  );
};

export default Map;
