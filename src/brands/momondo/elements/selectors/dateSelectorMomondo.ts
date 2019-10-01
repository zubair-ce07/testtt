import { by, element } from "protractor";
import { DateSelector } from "../../../../core/elements/selectors/dateSelector";
import { waitUntilInteractive } from "../../../../utils/browser.utils";

export class DateSelectorMomondo implements DateSelector {
  constructor(readonly leg: number) {
  }
  
  async selectDate(date: Date): Promise<void> {
    const trigger = element(by.css(`div[id$='-departDate${this.leg}-input']`));
    await trigger.click();
    
    const dateWithoutTime = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const dateElement = element(by.css(`div[data-val='${dateWithoutTime.getTime()}']`));
    await waitUntilInteractive(dateElement);
    return dateElement.click();
  }
  
  async getDisplayText(): Promise<string> {
    return element(by.css(`div[id$='-departDate${this.leg}-input']`)).getText();
  }
}
