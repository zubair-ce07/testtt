import { TilesHotelDialog } from "../../../../elements/dialogs/tilesHotelDialog";
import { $, browser, ElementFinder, ExpectedConditions as EC, Key } from "protractor";

export class TilesHotelDialogKayak implements TilesHotelDialog {
  async close(): Promise<void> {
    const closeButton = this.getDialogContainer().$(`.close`);
    await closeButton.sendKeys(Key.ESCAPE);
    await browser.wait(EC.invisibilityOf(this.getDialogContainer()))
  }
  
  async isDisplayed(): Promise<boolean> {
    return this.getDialogContainer().isPresent();
  }
  
  private getDialogContainer(): ElementFinder {
    return $(`[id$='destination_tiles_hotel_dialog-dialog-content']`)
  }
}
