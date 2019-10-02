import { by, element, ElementFinder } from "protractor";
import { MultiCityForm } from "../../../../core/elements/forms/multiCityForm";
import { CabinSelector } from "../../../../core/elements/selectors/cabinSelector";
import { DatePicker } from "../../../../core/elements/selectors/datePicker";
import { waitUntilInteractive } from "../../../../utils/browser.utils";
import { CabinSelectorMomondo } from "../selectors/cabinSelectorMomondo";
import { DatePickerMomondo } from "../selectors/datePickerMomondo";
import { FlightSelector } from "../../../../core/elements/selectors/flightSelector";
import { FlightSelectorMomondo } from "../selectors/flightSelectorMomondo";
import { FlightType } from "../../../../core/elements/types/flightType";

export class MultiCityFormMomondo implements MultiCityForm {
  async clearAllLegs(): Promise<void> {
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
  
  getCabin(leg: number): CabinSelector {
    return new CabinSelectorMomondo(leg);
  }
  
  getDatePicker(leg: number): DatePicker {
    return new DatePickerMomondo(leg);
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
  
  getOrigin(leg: number): FlightSelector {
    return new FlightSelectorMomondo(leg, FlightType.ORIGIN);
  }
  
  getDestination(leg: number): FlightSelector {
    return new FlightSelectorMomondo(leg, FlightType.DESTINATION);
  }
  
  getMultiFormContainer(): ElementFinder {
    return element(by.css(`form[name='mc-searchform']`))
  }
  
  getFormContainer(): ElementFinder {
    return element(by.css(`form[name='searchform']`))
  }
  
  private async clearOriginAndDestination(leg: number): Promise<void> {
    const origin = this.getOrigin(leg);
    const destination = this.getDestination(0);
    await origin.setText('');
    await destination.setText('');
  }
}
