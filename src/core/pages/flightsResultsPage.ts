import { FlightResult } from "../elements/results/flightResult";
import { FlightsResultsSummary } from "../elements/results/flightResultsSummary";

export interface FlightsResultsPage {
  getFlightResult(index: number): FlightResult;
  
  getFlightResults(): Promise<FlightResult[]>;
  
  getSearchSummary(): FlightsResultsSummary;
  
  loadResults(): Promise<void>;
  
  isLoaded(): Promise<boolean>
}
