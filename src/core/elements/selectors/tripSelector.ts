import { TripType } from "../types/tripType";

export interface TripSelector {
  select(type: TripType): Promise<void>;
  
  getCurrentTripType(): Promise<string>;
}

