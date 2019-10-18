export interface FlightResultsSummary {
  getTravellers(): Promise<string>;
  
  getDisplayDate(): Promise<string>;
  
  getFlightsDisplayText(): Promise<string>;
}
