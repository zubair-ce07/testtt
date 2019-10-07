export interface Tile {
  triggerFlights(): Promise<void>;
  
  triggerHotels(): Promise<void>;
}
