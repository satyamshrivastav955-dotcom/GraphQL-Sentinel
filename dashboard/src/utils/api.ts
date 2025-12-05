import axios, { AxiosError } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add retry interceptor
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const config = error.config as any;
    
    // Retry logic (max 3 attempts)
    if (!config || !config.retry) {
      config.retry = 0;
    }
    
    config.retry += 1;
    
    if (config.retry <= 3) {
      // Exponential backoff
      const delay = Math.pow(2, config.retry) * 100;
      await new Promise(resolve => setTimeout(resolve, delay));
      return api(config);
    }
    
    return Promise.reject(error);
  }
);

export const getStream = async () => {
  const response = await api.get('/api/stream');
  return response.data;
};

export const getMetrics = async () => {
  const response = await api.get('/api/metrics');
  return response.data;
};

export const getQueryDetails = async (id: string) => {
  const response = await api.get(`/api/query/${id}`);
  return response.data;
};

export const getExplanation = async (id: string) => {
  const response = await api.get(`/api/explain/${id}`);
  return response.data;
};

export const submitQuery = async (query: string, clientId?: string) => {
  const response = await api.post('/graphql-proxy',
    { query },
    { headers: clientId ? { 'X-Client-ID': clientId } : {} }
  );
  return response.data;
};

// Export base URL for other components
export { API_BASE_URL };
