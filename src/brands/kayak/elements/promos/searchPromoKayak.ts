import { $, ElementFinder } from "protractor";
import { SearchPromo } from "../../../../elements/promos/searchPromo";
import { click, focusCursor } from "../../../../utils/specs.utils";

export class SearchPromoKayak implements SearchPromo {
  async isDisplayed(): Promise<boolean> {
    return this.getContainer().isDisplayed();
  }
  
  async searchNow(): Promise<void> {
    await click($(`[id$='search-promo-search']`));
  }
  
  async focus(): Promise<void> {
    await focusCursor(this.getContainer());
  }
  
  private getContainer(): ElementFinder {
    return $(`.Sem-Common-Landing-SearchPromo`)
  }
}
