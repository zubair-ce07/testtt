import { $ } from "protractor";
import { SearchPromo } from "../../../../elements/promos/searchPromo";
import { click } from "../../../../utils/specs.utils";

export class SearchPromoKayak implements SearchPromo {
  async isDisplayed(): Promise<boolean> {
    return $(`.Sem-Common-Landing-SearchPromo`).isPresent();
  }
  
  async searchNow(): Promise<void> {
    await click($(`button[id$='search-promo-search']`));
  }
  
}
