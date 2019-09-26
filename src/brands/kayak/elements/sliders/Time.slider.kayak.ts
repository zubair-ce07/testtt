import { browser, by, element, ElementFinder, ExpectedConditions as EC } from "protractor";
import { DragHandle, TimeSlider } from "../../../../core/elements";
import { scrollIntoView, waitUntilInteractive } from "../../../../utils/browser.utils";

export class TimeSliderKayak implements TimeSlider {
  constructor(readonly container: ElementFinder) {
  }
  
  async drag(handle: DragHandle, x: number, y: number = 0): Promise<void> {
    const sliderHandle = this.container.element(by.css(`div[id$='-sliderWidget-handle-${handle}']`));
    waitUntilInteractive(sliderHandle);
    scrollIntoView(sliderHandle);
    await browser.driver.actions().dragAndDrop(sliderHandle, {x, y}).perform();
    await this.waitLoadingCoverToHide();
  }
  
  async getDisplayText(): Promise<string> {
    return this.container.element(by.css(`div[id*='times-takeoff-label']`)).getText();
  }
  
  async waitLoadingCoverToHide(): Promise<void> {
    await browser.wait(EC.invisibilityOf(
      element(by.className('resultsContainer')).element(by.className('loading')))
    );
  }
  
}
