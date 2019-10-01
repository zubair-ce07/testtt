import { DragHandle } from "./dragHandle";

export interface TimeSlider {
  drag(handle: DragHandle, x: number, y?: number): Promise<void>;
  
  getDisplayText(): Promise<string>;
}
