import { FlightResultsSummary } from "../../../../core/elements/results/flightResultsSummary";

export class FlightResultsSummaryKayak implements FlightResultsSummary {
  getDisplayDate(): Promise<string> {
    return undefined;
  }
  
  getFlightsDisplayText(): Promise<string> {
    return undefined;
  }
  
  getTravellers(): Promise<string> {
    return undefined;
  }
}
