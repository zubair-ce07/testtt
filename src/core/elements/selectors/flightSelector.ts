export interface FlightSelector {
  set(text: string): Promise<void>;
  
  getDisplayText(): Promise<string>
}
