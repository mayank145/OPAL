import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 second timeout for slow connections
});

// Add request interceptor for timeout handling
api.interceptors.request.use(
  (config) => {
    // Add timestamp to track request duration
    config.metadata = { startTime: new Date() };
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      console.error('Request timeout - backend may be slow or unresponsive');
    }
    return Promise.reject(error);
  }
);

// FATS API
export const fatsAPI = {
  // Get all FATS entries
  getAll: async (params = {}) => {
    const { skip = 0, limit = 20, search, section, section2, status } = params; // Reduced default limit to 20
    const queryParams = new URLSearchParams();
    if (skip) queryParams.append('skip', skip);
    if (limit) queryParams.append('limit', limit);
    // Only add search if it's a non-empty string
    if (search && search.trim()) queryParams.append('search', search.trim());
    if (section && section.trim()) queryParams.append('section', section);
    if (section2 && section2.trim()) queryParams.append('section2', section2);
    if (status && status.trim()) queryParams.append('status', status);
    
    // Use longer timeout for list endpoint - database query can be slow
    const listApi = axios.create({
      baseURL: API_BASE_URL,
      timeout: 60000, // Increased to 60 seconds for large datasets
    });
    const response = await listApi.get(`/api/v1/fats/?${queryParams.toString()}`);
    return response.data;
  },

  // Get FATS by ID
  getById: async (idno) => {
    // Use shorter timeout for individual FATS (10 seconds) to prevent hanging
    const fatsApi = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000, // 10 second timeout for individual FATS
    });
    const response = await fatsApi.get(`/api/v1/fats/${idno}`);
    return response.data;
  },

  // Search FATS by IDNo
  searchByIdno: async (idno) => {
    const response = await api.get(`/api/v1/fats/search/${idno}`);
    return response.data;
  },

  // Create FATS entry
  create: async (fatsData, confirmed = false) => {
    const response = await api.post(`/api/v1/fats/?confirmed=${confirmed}`, fatsData);
    return response.data;
  },

  // Update FATS entry
  update: async (idno, updateData) => {
    const response = await api.put(`/api/v1/fats/${idno}`, updateData);
    return response.data;
  },

  // Delete FATS entry
  delete: async (idno) => {
    await api.delete(`/api/v1/fats/${idno}`);
  },

  // Delete blank FATS entries
  deleteBlank: async () => {
    const response = await api.delete('/api/v1/fats/cleanup/blank');
    return response.data;
  },

  // Get FATS statistics
  getStatistics: async () => {
    const response = await api.get('/api/v1/fats/stats/summary');
    return response.data;
  },

  // Add comment to FATS
  addComment: async (fatsId, commentData) => {
    const response = await api.post(`/api/v1/fats/${fatsId}/comments`, commentData);
    return response.data;
  },

  // Get comments for FATS
  getComments: async (fatsId) => {
    const response = await api.get(`/api/v1/fats/${fatsId}/comments`);
    return response.data;
  },

  // Update comment
  updateComment: async (commentId, commentData) => {
    const response = await api.patch(`/api/v1/fats/comments/${commentId}`, commentData);
    return response.data;
  },

  // Delete comment
  deleteComment: async (commentId) => {
    await api.delete(`/api/v1/fats/comments/${commentId}`);
  },

  // Upload image for FATS
  uploadImage: async (fatsId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post(`/api/v1/fats/${fatsId}/images`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 30000, // 30 second timeout for image uploads
    });
    return response.data;
  },

  // Upload multiple images for FATS (bulk upload - more efficient)
  uploadImages: async (fatsId, files) => {
    const formData = new FormData();
    // Append all files with 'files' key (matches backend expectation)
    Array.from(files).forEach((file) => {
      formData.append('files', file);
    });
    const response = await api.post(`/api/v1/fats/${fatsId}/images/bulk`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // 60 second timeout for bulk uploads
    });
    return response.data;
  },

  // Get images for FATS
  getImages: async (fatsId) => {
    // Use shorter timeout for images (5 seconds) to prevent blocking
    const imageApi = axios.create({
      baseURL: API_BASE_URL,
      timeout: 5000, // 5 second timeout for images
    });
    const response = await imageApi.get(`/api/v1/fats/${fatsId}/images`);
    return response.data;
  },

  // Delete image by filename
  deleteImage: async (filename) => {
    await api.delete(`/api/v1/fats/images/${filename}`);
  },

  // Get image URL (for display) - now uses filename
  getImageUrl: (filename) => {
    return `${API_BASE_URL}/api/v1/fats/images/${filename}/file`;
  },
};

// Reference Data API
export const referenceAPI = {
  // Get all sections (for section dropdown)
  getSections: async () => {
    const response = await api.get('/api/v1/reference/sections');
    return response.data;
  },
  
  // Get all sections2 (for section2 dropdown)
  getSections2: async () => {
    const response = await api.get('/api/v1/reference/sections2');
    return response.data;
  },
  
  // Get all staff (for operator dropdown)
  getStaff: async () => {
    const response = await api.get('/api/v1/reference/staff');
    return response.data;
  },
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;

