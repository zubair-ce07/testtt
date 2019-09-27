import { $$, by, element, ElementFinder } from "protractor";
import { MultiCityForm } from "../../../../core/elements/forms/multiCity";
import { CabinSelector } from "../../../../core/elements/selectors/cabin";
import { DateSelector } from "../../../../core/elements/selectors/date";
import { FlightSelector } from "../../../../core/elements/selectors/flight";
import { waitUntilInteractive } from "../../../../utils/browser.utils";
import { CabinSelectorKayak } from "../selectors/cabin";
import { DateSelectorKayak } from "../selectors/date";
import { FlightSelectorKayak } from "../selectors/flight";

export class MultiCityFormKayak implements MultiCityForm {
  async isFormVisible(): Promise<boolean> {
    return this.getMultiSearchForm().isDisplayed();
  }
  
  async makeFormVisible(): Promise<void> {
    const multiSearchForm = this.getMultiSearchForm();
    const isFormDisplayed = await multiSearchForm.isDisplayed();
    
    if (!isFormDisplayed) {
      await this.getSearchForm().click();
    }
    
    await waitUntilInteractive(multiSearchForm);
  }
  
  async clearAll(): Promise<void> {
    const clearLegs = element(by.className(`col-clear-legs`)).element(by.tagName('button'));
    await waitUntilInteractive(clearLegs);
    await clearLegs.click();
  }
  
  async clickSearch(): Promise<void> {
    const submit = element(by.css(`div[id$='-submit-multi']`));
    await waitUntilInteractive(submit);
    return submit.click();
  }
  
  getCabinSelector(leg: number): CabinSelector {
    return new CabinSelectorKayak(leg);
  }
  
  getDateSelector(leg: number): DateSelector {
    return new DateSelectorKayak(
      element(by.css(`div[id$='multiCityLeg${leg}']`))
    );
  }
  
  getFlightSelector(leg: number): FlightSelector {
    return new FlightSelectorKayak(leg);
  }
  
  async getDisplayedLegsCount(): Promise<number> {
    return $$(`.js-multiCityLeg`).filter(element => element.isDisplayed()).count();
  }
  
  getSearchForm(): ElementFinder {
    return element(by.css(`form[name='searchform']`))
  }
  
  getMultiSearchForm(): ElementFinder {
    return element(by.css(`form[name='mc-searchform']`))
  }
  
}
