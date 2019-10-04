import { Destination } from "../../../../elements/input/destination";

export class DestinationKayak implements Destination {
  type(text: string): Promise<void> {
    return undefined;
  }
  
  getDisplayText(): Promise<string> {
    return undefined;
  }
}
