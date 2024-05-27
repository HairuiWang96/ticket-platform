// src/services/apiService.ts
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Assuming your backend runs on port 8000

const apiService = axios.create({
    baseURL: API_BASE_URL,
});

export default apiService;
