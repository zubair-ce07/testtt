import { CompareTo } from "../../../elements/compareTo";

export class CompareToKayak implements CompareTo {
  getSelected(): Promise<string[]> {
    return undefined;
  }
  
  select(index: number): Promise<void> {
    return undefined;
  }
  
  selectAll(): Promise<void> {
    return undefined;
  }
  
  isDisplayed(): Promise<boolean> {
    return undefined;
  }
  
}
