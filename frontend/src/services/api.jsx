import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create an axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      console.log('Token attached:', token); // Log the token being attached
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Error in request interceptor:', error);
    return Promise.reject(error);
  }
);



export const fetchElectricityPrices = async (regionCode, date) => {
  try {
    // Log the payload being sent
    console.log('Sending request with payload:', { region: regionCode, date });

    const response = await apiClient.post('/electricity-prices/', {
      region: regionCode,
      date: date,
    });

    console.log('API response for region', regionCode, ':', response.data);  // Log the API response
    return response.data;
  } catch (error) {
    console.error('Error fetching electricity prices:', error);
    throw error;
  }
};
