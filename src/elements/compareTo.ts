export interface CompareTo {
  select(index: number): Promise<void>;
  
  selectAll(): Promise<void>;
  
  getSelected(): Promise<string[]>;
  
  isDisplayed(): Promise<boolean>;
}
