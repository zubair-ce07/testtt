import { browser, by, element, ElementFinder, ExpectedConditions as EC } from "protractor";

export class MapMarker {
  constructor(readonly marker: ElementFinder) {
  }
  
  async click(): Promise<void> {
    return this.marker.click();
  }
  
  async hoverMouse(): Promise<void> {
    return browser.actions().mouseMove(this.marker).perform();
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
