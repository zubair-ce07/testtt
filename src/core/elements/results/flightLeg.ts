export interface FlightLeg {
  getAirlineName(): Promise<string>;
  
  getAirlineLogo(): Promise<string>;
  
  getDepartureTime(): Promise<string>;
  
  getArrivalTime(): Promise<string>;
  
  getDepartureAirportCode(): Promise<string>;
  
  getArrivalAirportCode(): Promise<string>;
  
  getDuration(): Promise<string>;
}
