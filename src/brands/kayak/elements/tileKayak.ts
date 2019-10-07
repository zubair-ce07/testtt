import { Tile } from "../../../elements/tile";
import { ElementFinder } from "protractor";
import { focusCursor } from "../../../utils/specs.utils";

export class TileKayak implements Tile {
  constructor(readonly tile: ElementFinder) {
  }
  
  async triggerHotels(): Promise<void> {
    await focusCursor(this.tile);
    this.tile.$(`.hotelTrigger`).click();
  }
  
  async triggerFlights(): Promise<void> {
    await focusCursor(this.tile);
    this.tile.$(`.flightTrigger`).click();
  }
  
}
