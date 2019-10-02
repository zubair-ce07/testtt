export interface FlightSelector {
  setText(text: string): Promise<void>;
  
  getDisplayText(): Promise<string>
}
