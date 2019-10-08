import { TilesFlightDialog } from "../../../../elements/dialogs/tilesFlightDialog";
import { $, browser, ElementFinder, ExpectedConditions as EC, Key } from "protractor";

export class TilesFlightDialogKayak implements TilesFlightDialog {
  async close(): Promise<void> {
    const closeButton = this.getDialogContainer().$(`.close`);
    await closeButton.sendKeys(Key.ESCAPE);
    await browser.wait(EC.invisibilityOf(this.getDialogContainer()));
  }
  
  async isDisplayed(): Promise<boolean> {
    return this.getDialogContainer().isPresent();
  }
  
  private getDialogContainer(): ElementFinder {
    return $(`[id$='destination_tiles_flight_dialog-dialog-content']`)
  }
}
