import React, { useState, useEffect } from 'react';
import Map from './Map'; // The Map component
import { fetchElectricityPrices } from '../services/api'; // Function to fetch data

const NORWAY_REGIONS = {
  NO1: { region: "Oslo", coordinates: [59.9139, 10.7522] },
  NO2: { region: "Kristiansand", coordinates: [58.1467, 7.9956] },
  NO3: { region: "Trondheim", coordinates: [63.4305, 10.3951] },
  NO4: { region: "Tromsø", coordinates: [69.6492, 18.9553] },
  NO5: { region: "Bergen", coordinates: [60.3928, 5.3221] }
};

const MapDashboard = () => {
  const [locations, setLocations] = useState([]); // To store fetched locations
  const [selectedDate, setSelectedDate] = useState('2023-09-09'); // Default date
  const [zoomLevel, setZoomLevel] = useState(5); // Default zoom level

  // Fetch electricity prices when the component mounts or when the date changes
  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const locationData = [];
        for (const regionCode in NORWAY_REGIONS) {
          const region = NORWAY_REGIONS[regionCode];
          const electricityPrices = await fetchElectricityPrices(regionCode, selectedDate); // Fetching from API
          locationData.push({
            region: region.region,
            coordinates: region.coordinates,
            prices: electricityPrices, // Storing the fetched prices
          });
        }
        setLocations(locationData); // Updating locations state with the fetched data
      } catch (error) {
        console.error('Error fetching electricity prices:', error);
      }
    };

    fetchPrices(); // Trigger the fetch function
  }, [selectedDate]); // Fetch whenever the selected date changes

  return (
    <div>
      <Map
        locations={locations} // Pass locations with prices to the map
        zoomLevel={zoomLevel}
        setZoomLevel={setZoomLevel}
      />

      {/* Date Picker */}
      <input
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)} // Update date when the user selects a new one
      />
    </div>
  );
};

export default MapDashboard;

