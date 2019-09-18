import { by, element } from "protractor"

export class Travellers {
  getDisplayText() {
    return element(by.css(`div[id$='-roomsGuestsAboveForm']`)).getText();
  }
}
