export interface FlightsResultsSummary {
  getTravellers(): Promise<string>;
  
  getDisplayDate(): Promise<string>;
  
  getFlightsDisplayText(): Promise<string>;
}
