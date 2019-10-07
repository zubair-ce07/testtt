import { $ } from "protractor";
import { Subscription } from "../../../elements/subscription";

export class SubscriptionKayak implements Subscription {
  async isDisplayed(): Promise<boolean> {
    return $(`form[id$='signupForm']`).$(`input`).isPresent();
  }
}
