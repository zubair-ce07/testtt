export interface FlightDestination {
  select(type: string): Promise<void>;
  
  isDisplayed(): Promise<boolean>;
  
  getDisplayText(): Promise<string>;
}
