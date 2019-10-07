import { Subscription } from "../../../elements/subscription";
import { $ } from "protractor";

export class SubscriptionKayak implements Subscription {
  async isPresent(): Promise<boolean> {
    return $(`form[id$='signupForm']`).$(`input`).isPresent();
  }
}
