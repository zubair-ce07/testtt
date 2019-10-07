import { $, ElementFinder } from "protractor";
import { CompareTo } from "../../../elements/compareTo";

export class CompareToKayak implements CompareTo {
  async getSelected(): Promise<string[]> {
    return this.getContainer().$$(`span[aria-checked='true']`).map(finder => finder.getText());
  }
  
  async select(index: number): Promise<void> {
    return this.getContainer().$$('span').get(index).click();
  }
  
  selectAll(): Promise<void> {
    return undefined;
  }
  
  async isDisplayed(): Promise<boolean> {
    return $(`.Common-Compareto-V3-SEMCmp2`).isDisplayed();
  }
  
  private getContainer(): ElementFinder {
    return $(`div[id$='compareTo-checkbox-row']`)
  }
}
