import { browser, by, element, ElementFinder, ExpectedConditions as EC } from "protractor";
import { scrollElementIntoView } from "../utils/browser.utils";

export class MapMarker {
  constructor(readonly marker: ElementFinder) {
  }
  
  async click(): Promise<void> {
    browser.wait(EC.presenceOf(this.marker));
    browser.wait(EC.visibilityOf(this.marker));
    await scrollElementIntoView(this.marker);
    browser.wait(EC.elementToBeClickable(this.marker));
    return this.marker.click();
  }
  
  async hoverMouse(): Promise<void> {
    await scrollElementIntoView(this.marker);
    browser.wait(EC.presenceOf(this.marker));
    browser.wait(EC.visibilityOf(this.marker));
    browser.wait(EC.elementToBeClickable(this.marker));
    await browser.actions().mouseMove(this.marker).perform();
  }
  
  async isSummaryCardDisplayed(): Promise<boolean> {
    const summary = await this.getSummaryCardContainer();
    await browser.wait(EC.presenceOf(summary));
    return summary.isDisplayed();
  }
  
  async getSummaryCardContainer(): Promise<ElementFinder> {
    const markerId: string = await this.marker.getAttribute('id');
    const [ignored, id] = markerId.split('-');
    return element(by.id(`summaryCard-${id}`))
  }
  
}
