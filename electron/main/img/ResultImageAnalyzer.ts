import * as Tesseract from 'tesseract.js';
import sharp, { Region } from 'sharp';

import SmashBrosResult from '../model/SmashBrosResult';

export default class ResultImageAnalyzer {
  private static readonly OWN_FIGHTER_NAME_POSITION: Region = { top: 40, height: 160, left: 491, width: 435 };

  private static readonly OPPONENT_FIGHTER_NAME_POSITION: Region = { top: 40, height: 160, left: 1314, width: 435 };

  public static analyzeResult = async (): Promise<SmashBrosResult> => {
    const smashBrosResultImageSharp = sharp('./electron/main/resources/result_win.png').threshold(220);
    const ownFighterName = await ResultImageAnalyzer.recognizeFromSharp(smashBrosResultImageSharp, ResultImageAnalyzer.OWN_FIGHTER_NAME_POSITION);
    const opponentFighterName = await ResultImageAnalyzer.recognizeFromSharp(smashBrosResultImageSharp, ResultImageAnalyzer.OPPONENT_FIGHTER_NAME_POSITION);
    return new SmashBrosResult(ownFighterName, opponentFighterName);
  };

  private static recognizeFromSharp = async (smashBrosResultImageSharp: sharp.Sharp, region: Region): Promise<string> => {
    const smashBrosResultImageBuffer = await smashBrosResultImageSharp.extract(region).toBuffer();
    const result = await Tesseract.recognize(smashBrosResultImageBuffer, 'eng');
    return result.data.text.replace(/\r?\n/g, ' ').trim();
  };
}
