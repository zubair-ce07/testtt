export interface FlightSelector {
  setOrigin(text: string): Promise<void>;
  
  setDestination(text: string): Promise<void>;
  
  getDisplayText(type: 'origin' | 'destination'): Promise<string>;
}
