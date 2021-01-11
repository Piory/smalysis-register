import { ipcMain } from 'electron';
import ResultImageAnalyzer from './img/ResultImageAnalyzer';

const initIpcMain = (): void => {
  ipcMain.handle('analyze-result', async () => {
    await ResultImageAnalyzer.analyzeResult();
  });
};

export default initIpcMain;
