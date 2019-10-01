import { by, element, ElementFinder } from "protractor";
import { CabinSelector } from "../../../../core/elements/selectors/cabin";
import { CabinType } from "../../../../core/elements/selectors/cabinType";

export class CabinSelectorMomondo implements CabinSelector {
  constructor(readonly leg: number) {
  }
  
  async select(option: CabinType): Promise<void> {
    return this.getSelectElement().element(by.css(`option[title=${option}]`)).click();
  }
  
  async getDisplayText(): Promise<string> {
    return this.getSelectElement().getAttribute('title');
  }
  
  getSelectElement(): ElementFinder {
    return element(by.css(`select[id$='cabin_type${this.leg}-select']`))
  }
}
