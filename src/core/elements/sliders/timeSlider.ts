import { HandleType } from "../types/handleType";

export interface TimeSlider {
  drag(handle: HandleType, x: number, y?: number): Promise<void>;
  
  getDisplayText(): Promise<string>;
}
