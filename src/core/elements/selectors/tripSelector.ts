import { TripType } from "./tripType";

export interface TripSelector {
  select(type: TripType): Promise<void>;
  
  getCurrentTripType(): Promise<string>;
}

