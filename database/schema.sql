-- ===========================
-- AgroVision AI — Database Schema
-- Supabase PostgreSQL
-- ===========================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Plant analyses
CREATE TABLE plant_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    image_url TEXT NOT NULL,
    plant_name TEXT,
    scientific_name TEXT,
    family TEXT,
    confidence FLOAT,
    description TEXT,
    suitable_regions TEXT[],
    growing_season TEXT,
    water_needs TEXT,
    model_version TEXT DEFAULT 'YOLOv8n-plant-v1',
    processing_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Disease analyses
CREATE TABLE disease_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    image_url TEXT NOT NULL,
    disease_name TEXT,
    plant_affected TEXT,
    confidence FLOAT,
    severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    description TEXT,
    causes TEXT[],
    symptoms TEXT[],
    treatments TEXT[],
    prevention_tips TEXT[],
    model_version TEXT DEFAULT 'EfficientNet-B0-disease-v1',
    processing_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Land/crop recommendations
CREATE TABLE land_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    image_url TEXT NOT NULL,
    soil_condition JSONB,
    region TEXT,
    recommended_crops JSONB,
    farming_suggestions TEXT[],
    irrigation_advice TEXT,
    model_version TEXT DEFAULT 'OpenCV-Soil-v1',
    processing_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI logs (admin)
CREATE TABLE ai_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_type TEXT NOT NULL CHECK (analysis_type IN ('plant', 'disease', 'land')),
    analysis_id UUID,
    input_image_url TEXT,
    result JSONB,
    confidence FLOAT,
    processing_time_ms INTEGER,
    model_version TEXT,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_plant_analyses_user ON plant_analyses(user_id);
CREATE INDEX idx_plant_analyses_created ON plant_analyses(created_at DESC);
CREATE INDEX idx_disease_analyses_user ON disease_analyses(user_id);
CREATE INDEX idx_disease_analyses_severity ON disease_analyses(severity);
CREATE INDEX idx_disease_analyses_created ON disease_analyses(created_at DESC);
CREATE INDEX idx_land_analyses_user ON land_analyses(user_id);
CREATE INDEX idx_land_analyses_region ON land_analyses(region);
CREATE INDEX idx_ai_logs_type ON ai_logs(analysis_type);
CREATE INDEX idx_ai_logs_created ON ai_logs(created_at DESC);

-- Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE plant_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE disease_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE land_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_logs ENABLE ROW LEVEL SECURITY;

-- Policies: Users can read their own data, admins can read all
CREATE POLICY "Users can view own data" ON plant_analyses FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own data" ON plant_analyses FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can view own diseases" ON disease_analyses FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own diseases" ON disease_analyses FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can view own land" ON land_analyses FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own land" ON land_analyses FOR INSERT WITH CHECK (auth.uid() = user_id);
