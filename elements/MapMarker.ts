import { browser, by, element, ElementFinder, ExpectedConditions as EC } from "protractor";
import { scrollElementIntoView } from "../utils/browser.utils";

export class MapMarker {
  constructor(readonly elm: ElementFinder) {
  }
  
  async click() {
    browser.wait(EC.presenceOf(this.elm));
    browser.wait(EC.visibilityOf(this.elm));
    await scrollElementIntoView(this.elm);
    browser.wait(EC.elementToBeClickable(this.elm));
    return this.elm.click();
  }
  
  async hoverMouse() {
    await scrollElementIntoView(this.elm);
    browser.wait(EC.presenceOf(this.elm));
    browser.wait(EC.visibilityOf(this.elm));
    browser.wait(EC.elementToBeClickable(this.elm));
    await browser.actions().mouseMove(this.elm).perform();
  }
  
  async isSummaryCardDisplayed() {
    const summary = await this.getSummaryCardContainer();
    await browser.wait(EC.presenceOf(summary));
    return summary.isDisplayed();
  }
  
  async getSummaryCardContainer() {
    const markerId: string = await this.elm.getAttribute('id');
    const [ignored, id] = markerId.split('-');
    return element(by.id(`summaryCard-${id}`))
  }
  
}
