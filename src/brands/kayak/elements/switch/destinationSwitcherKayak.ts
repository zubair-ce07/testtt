import { $ } from "protractor";
import { DestinationSwitcher } from "../../../../elements/switch/destinationSwitcher";

export class DestinationSwitcherKayak implements DestinationSwitcher {
  async getOptions(): Promise<string[]> {
    return $(`.destinationSwitcher`).$$(`.destinationTitle`).map(finder => finder.getText());
  }
}
