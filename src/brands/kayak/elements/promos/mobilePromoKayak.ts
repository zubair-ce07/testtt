import { $, ElementFinder } from "protractor";
import { Promo } from "../../../../elements/promos/promo";
import { focusCursor } from "../../../../utils/specs.utils";

export class MobilePromoKayak implements Promo {
  async isDisplayed(): Promise<boolean> {
    return this.getContainer().isDisplayed();
  }
  
  async focus(): Promise<void> {
    await focusCursor(this.getContainer());
  }
  
  private getContainer(): ElementFinder {
    return $(`.Sem-Common-Landing-MobileAppPromo`)
  }
}
