import { $, ElementFinder } from "protractor";
import { CompareTo } from "../../../elements/compareTo";

export class CompareToKayak implements CompareTo {
  async selectAtLeast(count: number): Promise<void> {
    const selected = await this.getSelected();
  
    if (selected.length < count) {
      for (let index = selected.length; index < count; index++) {
        await this.select(index);
      }
    }
    
  }
  
  async getSelected(): Promise<string[]> {
    return this.getContainer().$$(`.item[aria-checked='true']`).map(finder => finder.getText());
  }
  
  async select(index: number): Promise<void> {
    return this.getContainer().$$('.item').get(index).click();
  }
  
  selectAll(): Promise<void> {
    return undefined;
  }
  
  async isDisplayed(): Promise<boolean> {
    return $(`.Common-Compareto-V3-SEMCmp2`).isDisplayed();
  }
  
  private getContainer(): ElementFinder {
    return $(`[id$='compareTo-checkbox-row']`)
  }
}
