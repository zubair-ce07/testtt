import { FlightLegDetails } from "../../../../core/elements/results/flightLegDetails";

export class FlightLegDetailsKayak implements FlightLegDetails {
  getAirlineLogo(): Promise<string> {
    return undefined;
  }
  
  getAirlineName(): Promise<string> {
    return undefined;
  }
  
  getArrivalAirportCode(): Promise<string> {
    return undefined;
  }
  
  getArrivalTime(): Promise<string> {
    return undefined;
  }
  
  getCabinClass(): Promise<string> {
    return undefined;
  }
  
  getDepartureAirportCode(): Promise<string> {
    return undefined;
  }
  
  getDepartureTime(): Promise<string> {
    return undefined;
  }
  
  getDuration(): Promise<string> {
    return undefined;
  }
  
  getFlightNumber(): Promise<string> {
    return undefined;
  }
}
