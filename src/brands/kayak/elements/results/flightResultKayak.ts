import { by, ElementFinder } from "protractor";
import { FlightResult } from "../../../../core/elements/results/flightResult";
import { waitUntilInteractive } from "../../../../utils/browser.utils";

export class FlightResultKayak implements FlightResult {
  constructor(readonly container: ElementFinder) {
  }
  
  async openProviderPage(): Promise<void> {
    const button = this.container.element(by.cssContainingText(`.Common-Booking-MultiBookProvider`, 'View Deal'));
    await waitUntilInteractive(button);
    return button.click();
  }
  
}
