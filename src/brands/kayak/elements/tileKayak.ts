import { Tile } from "../../../elements/tile";

export class TileKayak implements Tile {
  constructor(readonly index: number) {
  }
  
  triggerFlights(): Promise<void> {
    return undefined;
  }
  
  triggerHotels(): Promise<void> {
    return undefined;
  }
  
}
