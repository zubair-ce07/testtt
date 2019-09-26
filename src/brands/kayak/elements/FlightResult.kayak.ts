import { by, ElementFinder } from "protractor";
import { FlightResult } from "../../../core/elements";
import { waitUntilInteractive } from "../../../utils/browser.utils";

export class FlightResultKayak implements FlightResult {
  constructor(readonly container: ElementFinder) {
  }
  
  async clickViewDeal(): Promise<void> {
    const button = this.container.element(by.cssContainingText(`.Common-Booking-MultiBookProvider`, 'View Deal'));
    await waitUntilInteractive(button);
    return button.click();
  }
  
}
