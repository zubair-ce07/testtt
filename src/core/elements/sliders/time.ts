export interface TimeSlider {
  drag(handle: DragHandle, x: number, y?: number): Promise<void>;
  
  getDisplayText(): Promise<string>;
}

export enum DragHandle {
  LEFT,
  RIGHT,
}
