const ENV = process.env.NODE_ENV;

const API_URL = (ENV === 'production') ? '/api' : 'http://localhost:8000/api';

export default {
  API_URL,
};
