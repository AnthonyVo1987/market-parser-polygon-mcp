// Configuration loader for frontend
import appConfig from '../../../config/app.config.json';

export interface AppConfig {
  backend: {
    server: { host: string; port: number };
    ai: {
      availableModels: string[];
      maxContextLength: number;
      pricing: Record<string, { inputPer1M: number; outputPer1M: number }>
    };
    agent: { sessionName: string; reportsDirectory: string };
    mcp: { version: string; timeoutSeconds: number };
    security: {
      enableRateLimiting: boolean;
      rateLimitRPM: number;
      cors: { origins: string[] }
    };
    logging: { mode: string };
  };
  frontend: {
    server: { host: string; port: number };
    api: { baseUrl: string };
    features: { appEnv: string; pwa: boolean; debugMode: boolean };
    development: { hmr: boolean; sourceMap: boolean; bundleAnalyzer: boolean };
  };
}

export const config: AppConfig = appConfig;

// Helper functions for accessing configuration
export const getBackendConfig = () => config.backend;
export const getFrontendConfig = () => config.frontend;
export const getAIConfig = () => config.backend.ai;
export const getSecurityConfig = () => config.backend.security;
export const getDevelopmentConfig = () => config.frontend.development;

// Environment-specific helpers
export const isDevelopment = () => config.frontend.features.appEnv === 'development';
export const isDebugMode = () => config.frontend.features.debugMode;
export const isPWAEnabled = () => config.frontend.features.pwa;

// API configuration helpers
export const getAPIBaseURL = () => `http://${config.backend.server.host}:${config.backend.server.port}`;
export const getBackendURL = () => `http://${config.backend.server.host}:${config.backend.server.port}`;
export const getFrontendURL = () => `http://${config.frontend.server.host}:${config.frontend.server.port}`;

// Development features
export const isHMREnabled = () => config.frontend.development.hmr;
export const isSourceMapEnabled = () => config.frontend.development.sourceMap;
export const isBundleAnalyzerEnabled = () => config.frontend.development.bundleAnalyzer;