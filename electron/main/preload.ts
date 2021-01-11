import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('api', {
  analyzeResult: () => ipcRenderer.invoke('analyze-result'),
});
