import { FlightLeg } from "../../../../core/elements/results/flightLeg";

export class FlightLegKayak implements FlightLeg {
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
  
  getDepartureAirportCode(): Promise<string> {
    return undefined;
  }
  
  getDepartureTime(): Promise<string> {
    return undefined;
  }
  
  getDuration(): Promise<string> {
    return undefined;
  }
}
