import { by, element } from "protractor";
import { CabinSelector } from "../../../../core/elements/selectors/cabinSelector";
import { CabinType } from "../../../../core/elements/types/cabinType";
import { waitUntilInteractive } from "../../../../utils/browser.utils";

export class CabinSelectorKayak implements CabinSelector {
  constructor(private readonly leg: number) {
  }
  
  async setType(option: CabinType): Promise<void> {
    const li = element(by.css(`ul[id$='-cabin_type${this.leg}-list']`)).element(by.css(`li[data-title='${option}']`));
    await this.makeOptionsInteractive();
    await waitUntilInteractive(li);
    await li.click();
  }
  
  async makeOptionsInteractive(): Promise<void> {
    const trigger = element(by.css(`div[id$='-cabin_type${this.leg}-display']`));
    await waitUntilInteractive(trigger);
    await trigger.click();
  }
  
  async getDisplayText(): Promise<string> {
    return element(by.css(`div[id$='-cabin_type${this.leg}-display-status']`)).getText();
  }
  
}
