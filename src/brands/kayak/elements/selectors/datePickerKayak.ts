import { by, element, ElementFinder } from "protractor";
import { DatePicker } from "../../../../core/elements/selectors/datePicker";
import { waitUntilInteractive } from "../../../../utils/browser.utils";

export class DatePickerKayak implements DatePicker {
  constructor(readonly container: ElementFinder) {
  }
  
  async selectDate(date: Date): Promise<void> {
    const dateWithoutTime = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    const trigger = this.container.element(by.className(`Common-Widgets-Datepicker-DateModal`));
    await waitUntilInteractive(trigger);
    await trigger.click();
    
    const option = element(by.css(`div[data-val='${dateWithoutTime.getTime()}']`));
    await waitUntilInteractive(option);
    return option.click();
  }
  
  async getDisplayText(): Promise<string> {
    return this.container.element(by.css(`div[id$='-display-start-inner']`)).getText();
  }
}
