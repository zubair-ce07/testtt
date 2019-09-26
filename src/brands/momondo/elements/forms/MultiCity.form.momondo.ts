import { by, element, ElementFinder } from "protractor";
import { CabinSelector, DateSelector, FlightSelector, MultiCityForm } from "../../../../core/elements";
import { waitUntilInteractive } from "../../../../utils/browser.utils";
import { CabinSelectorMomondo, DateSelectorMomondo, FlightSelectorMomondo } from "../selectors";

export class MultiCityFormMomondo implements MultiCityForm {
  async clearAll(): Promise<void> {
    await this.makeFormVisible();
    
    const clearAll = element(by.css(`button[id$='-clearAll']`));
    const isClearAllPresent = await clearAll.isDisplayed();
    if (isClearAllPresent) {
      return clearAll.click();
    }
    
    const flightsCount = await this.getDisplayedLegsCount();
    for (let leg = 0; leg < flightsCount; leg++) {
      await this.clearOriginAndDestination(leg);
    }
  }
  
  async clickSearch(): Promise<void> {
    return element(by.css(`[id$='-submit-multi']`)).click();
  }
  
  getCabinSelector(leg: number): CabinSelector {
    return new CabinSelectorMomondo(leg);
  }
  
  getDateSelector(leg: number): DateSelector {
    return new DateSelectorMomondo(leg);
  }
  
  getFlightSelector(leg: number): FlightSelector {
    return new FlightSelectorMomondo(leg);
  }
  
  async getDisplayedLegsCount(): Promise<number> {
    return element.all(by.css(`div[id*='multiCityLeg']`)).filter(element => element.isDisplayed()).count();
  }
  
  async makeFormVisible(): Promise<void> {
    const multiFormContainer = this.getMultiFormContainer();
    const isFormDisplayed = await multiFormContainer.isDisplayed();
    
    if (!isFormDisplayed) {
      this.getFormContainer().click();
    }
    
    await waitUntilInteractive(multiFormContainer);
  }
  
  async isFormVisible(): Promise<boolean> {
    return this.getMultiFormContainer().isDisplayed();
  }
  
  getMultiFormContainer(): ElementFinder {
    return element(by.css(`form[name='mc-searchform']`))
  }
  
  getFormContainer(): ElementFinder {
    return element(by.css(`form[name='searchform']`))
  }
  
  private async clearOriginAndDestination(leg: number): Promise<void> {
    const flightSelector = this.getFlightSelector(leg);
    await flightSelector.setOrigin('');
    await flightSelector.setDestination('')
  }
}
