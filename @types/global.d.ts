declare global {
  interface Window {
    api: API;
  }
}

export interface API {
  analyzeResult: () => Promise<void>;
}
