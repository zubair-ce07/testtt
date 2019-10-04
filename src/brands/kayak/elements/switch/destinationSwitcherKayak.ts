import { DestinationSwitcher } from "../../../../elements/switch/destinationSwitcher";

export class DestinationSwitcherKayak implements DestinationSwitcher {
  getOptions(): Promise<string[]> {
    return undefined;
  }
}
