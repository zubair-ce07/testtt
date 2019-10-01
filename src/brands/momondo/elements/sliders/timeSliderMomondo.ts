import { browser, by, element, ExpectedConditions as EC } from "protractor";
import { DragHandle } from "../../../../core/elements/sliders/dragHandle";
import { TimeSlider } from "../../../../core/elements/sliders/timeSlider";
import { scrollIntoView, waitUntilInteractive } from "../../../../utils/browser.utils";

export class TimeSliderMomondo implements TimeSlider {
  constructor(readonly leg: number) {
  }
  
  async drag(handle: DragHandle, x: number, y?: number): Promise<void> {
    const sliderHandle = element(by.css(`div[id$='-times-takeoff-slider-${this.leg}']`))
      .element(by.css(`div[id$='-sliderWidget-handle-${handle}']`));
    waitUntilInteractive(sliderHandle);
    scrollIntoView(sliderHandle);
    await browser.driver.actions().dragAndDrop(sliderHandle, { x, y }).perform();
    await this.waitLoadingCoverToHide();
  }
  
  async getDisplayText(): Promise<string> {
    return element(by.css(`div[id$='-times-takeoff-label-${this.leg}']`)).getText();
  }
  
  async waitLoadingCoverToHide() {
    const loading = element(by.className('resultsContainer')).element(by.className('loading'));
    
    await browser.wait(EC.presenceOf(loading));
    await browser.wait(EC.invisibilityOf(loading));
  }
  
}
