export interface TripSelector {
  select(type: TripType): Promise<void>;
  
  getCurrentTripType(): Promise<string>;
}

export enum TripType {
  ONE_WAY = 'oneway',
  MULTI_CITY = 'multicity',
  ROUND_TRIP = 'roundtrip',
}
