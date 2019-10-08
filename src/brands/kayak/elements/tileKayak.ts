import { Tile } from "../../../elements/tile";
import { $, ElementFinder } from "protractor";
import { focusCursor, waitUntilInteractive } from "../../../utils/specs.utils";

export class TileKayak implements Tile {
  constructor(readonly tile: ElementFinder) {
  }
  
  async triggerHotels(): Promise<void> {
    await focusCursor(this.tile);
    await this.tile.$(`.hotelTrigger`).click();
    await waitUntilInteractive(this.getHotelDialog());
  }
  
  async triggerFlights(): Promise<void> {
    await focusCursor(this.tile);
    await this.tile.$(`.flightTrigger`).click();
    await waitUntilInteractive(this.getFlightDialog())
  }
  
  private getFlightDialog(): ElementFinder {
    return $(`[id$='destination_tiles_flight_dialog-dialog-content']`)
  }
  
  private getHotelDialog(): ElementFinder {
    return $(`[id$='destination_tiles_hotel_dialog-dialog-content']`)
  }
}
