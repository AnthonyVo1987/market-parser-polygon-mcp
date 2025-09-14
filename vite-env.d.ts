/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_TITLE: string
  readonly VITE_APP_ENV: string
  readonly VITE_DEBUG_MODE: string
  readonly VITE_PWA_ENABLED: string
  readonly VITE_HMR_ENABLED: string
  readonly VITE_SOURCE_MAP: string
  readonly VITE_BUNDLE_ANALYZER: string
  // more env variables...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}