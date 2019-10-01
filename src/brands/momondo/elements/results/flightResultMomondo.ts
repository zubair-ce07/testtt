import { by, ElementFinder } from "protractor";
import { FlightResult } from "../../../../core/elements/results/flightResult";
import { waitUntilInteractive } from "../../../../utils/browser.utils";

export class FlightResultMomondo implements FlightResult {
  constructor(readonly container: ElementFinder) {
  }
  
  async openProviderPage(): Promise<void> {
    const viewDealButton = this.container.element(by.css(`a[id$='-booking-link']`));
    await waitUntilInteractive(viewDealButton);
    return viewDealButton.click();
    
  }
}
