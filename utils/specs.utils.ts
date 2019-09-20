import { HotelResult } from "../elements/HotelResult";
import { TabType } from "../elements/TabType";
import { waitForElementToBeInteractive } from "./browser.utils";

export async function switchTabAndLoadItsContainer(result: HotelResult, tab: TabType) {
  result.switchToTab(tab);
  await waitForElementToBeInteractive(result.getTabContainer(tab));
}
