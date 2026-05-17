// ===========================
// AgroVision AI — TypeScript Types
// ===========================

// Plant Detection
export interface PlantDetectionResult {
  plant_name: string;
  scientific_name: string;
  confidence: number;
  description: string;
  family: string;
  suitable_regions: string[];
  growing_season: string;
  water_needs: string;
  image_url: string;
}

// Disease Detection
export type SeverityLevel = "low" | "medium" | "high" | "critical";

export interface DiseaseDetectionResult {
  disease_name: string;
  plant_affected: string;
  confidence: number;
  severity: SeverityLevel;
  description: string;
  causes: string[];
  symptoms: string[];
  treatments: string[];
  prevention_tips: string[];
  image_url: string;
}

// Land / Crop Recommendation
export interface SoilCondition {
  type: string;
  ph_level: number;
  moisture: string;
  organic_matter: string;
  nutrients: {
    nitrogen: string;
    phosphorus: string;
    potassium: string;
  };
}

export interface CropRecommendation {
  crop_name: string;
  suitability_score: number;
  expected_yield: string;
  growing_period: string;
  irrigation_type: string;
  tips: string[];
}

export interface LandAnalysisResult {
  soil_condition: SoilCondition;
  region: string;
  recommended_crops: CropRecommendation[];
  farming_suggestions: string[];
  irrigation_advice: string;
  image_url: string;
}

// Region Data
export interface RegionData {
  id: string;
  name: string;
  name_uz: string;
  capital: string;
  coordinates: [number, number];
  area_km2: number;
  climate: string;
  avg_temperature: { summer: number; winter: number };
  annual_rainfall_mm: number;
  main_crops: string[];
  soil_types: string[];
  agricultural_area_hectares: number;
}

// Weather
export interface WeatherData {
  region: string;
  temperature: number;
  feels_like: number;
  humidity: number;
  wind_speed: number;
  description: string;
  icon: string;
  forecast: WeatherForecast[];
}

export interface WeatherForecast {
  date: string;
  temp_min: number;
  temp_max: number;
  description: string;
  icon: string;
}

// Analysis Log (Admin)
export interface AnalysisLog {
  id: string;
  analysis_type: "plant" | "disease" | "land";
  input_image_url: string;
  result: Record<string, unknown>;
  processing_time_ms: number;
  model_version: string;
  created_at: string;
}

// User (Admin)
export interface User {
  id: string;
  email: string;
  full_name: string;
  role: "user" | "admin";
  created_at: string;
}

// API Response wrapper
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  processing_time_ms?: number;
}

// Upload state
export interface UploadState {
  file: File | null;
  preview: string | null;
  uploading: boolean;
  progress: number;
  error: string | null;
}

// Analysis state
export type AnalysisStatus = "idle" | "uploading" | "processing" | "complete" | "error";

export interface AnalysisState<T> {
  status: AnalysisStatus;
  result: T | null;
  error: string | null;
  processingTime: number | null;
}
