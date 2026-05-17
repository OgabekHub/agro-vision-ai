// ===========================
// AgroVision AI — API Client
// ===========================

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `API Error: ${response.status}`);
    }

    return response.json();
  }

  // Plant Detection
  async detectPlant(imageFile: File, language: string = "uz") {
    const formData = new FormData();
    formData.append("file", imageFile);
    formData.append("language", language);
    return this.request<any>("/api/v1/plant/detect", {
      method: "POST",
      body: formData,
    });
  }

  // Disease Analysis
  async analyzeDiseases(imageFile: File, language: string = "uz") {
    const formData = new FormData();
    formData.append("file", imageFile);
    formData.append("language", language);
    return this.request<any>("/api/v1/disease/analyze", {
      method: "POST",
      body: formData,
    });
  }

  // Land/Crop Recommendation
  async analyzeLand(imageFile: File, language: string = "uz", region?: string) {
    const formData = new FormData();
    formData.append("file", imageFile);
    formData.append("language", language);
    if (region) formData.append("region", region);
    return this.request<any>("/api/v1/recommend/crops", {
      method: "POST",
      body: formData,
    });
  }

  // Weather
  async getWeather(region: string) {
    return this.request(`/api/v1/weather/${encodeURIComponent(region)}`);
  }

  // Regions
  async getRegions() {
    return this.request("/api/v1/regions");
  }

  async getRegion(id: string) {
    return this.request(`/api/v1/regions/${id}`);
  }

  // Admin
  async getAdminLogs(page = 1, limit = 20) {
    return this.request(`/api/v1/admin/logs?page=${page}&limit=${limit}`);
  }

  async getAdminStats() {
    return this.request("/api/v1/admin/stats");
  }

  async getAdminUsers(page = 1, limit = 20) {
    return this.request(`/api/v1/admin/users?page=${page}&limit=${limit}`);
  }

  // Upload Image (to Cloudinary via backend)
  async uploadImage(imageFile: File) {
    const formData = new FormData();
    formData.append("file", imageFile);
    return this.request("/api/v1/upload/image", {
      method: "POST",
      body: formData,
    });
  }
}

export const api = new ApiClient(API_BASE);
