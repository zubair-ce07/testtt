import { by, element } from "protractor"

export class Travellers {
  async getDisplayText(): Promise<string> {
    return element(by.css(`div[id$='-roomsGuestsAboveForm']`)).getText();
  }
}
