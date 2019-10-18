import { FlightResult } from "../elements/results/flightResult";
import { FlightResultsSummary } from "../elements/results/flightResultsSummary";

export interface FlightsResultsPage {
  getFlightResult(index: number): FlightResult;
  
  getFlightResults(): Promise<FlightResult[]>;
  
  getSearchSummary(): FlightResultsSummary;
  
  loadResults(): Promise<void>;
  
  isLoaded(): Promise<boolean>
}
