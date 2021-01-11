import { ipcMain } from 'electron';
import ResultImageAnalyzer from '../src/main/img/ResultImageAnalyzer';

export const initIpcMain = (): void => {
  ipcMain.handle('analyze-result', async () => {
    const result = await ResultImageAnalyzer.analyzeResult();
    console.log(`result -> ${JSON.stringify(result)}`);
  });
};
