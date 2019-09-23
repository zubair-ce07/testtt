import { browser, by, element, ExpectedConditions as EC } from "protractor";
import { Travellers } from "../elements/Travellers";
import { DateRange } from "../elements/DateRange";
import { Destination } from "../elements/Destination";
import { HotelsResults } from "./HotelsResults";

export class Hotels {
  readonly dateRange: DateRange = new DateRange();
  readonly travellers: Travellers = new Travellers();
  readonly destination: Destination = new Destination();
  
  async clickSearch(): Promise<void> {
    const submit = element(by.css(`div[id$='-formGridSearchBtn']`)).element(by.css(`button[id$='-submit']`));
    browser.wait(EC.visibilityOf(submit));
    browser.wait(EC.elementToBeClickable(submit));
    submit.click();
    return HotelsResults.loadResults();
  }
}
