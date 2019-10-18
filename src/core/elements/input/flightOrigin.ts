export interface FlightOrigin {
  select(type: string): Promise<void>;
  
  isDisplayed(): Promise<boolean>;
  
  getDisplayText(): Promise<string>;
}
