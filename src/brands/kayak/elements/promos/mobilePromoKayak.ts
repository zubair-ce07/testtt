import { $ } from "protractor";
import { Promo } from "../../../../elements/promos/promo";

export class MobilePromoKayak implements Promo {
  async isDisplayed(): Promise<boolean> {
    return $(`.Sem-Common-Landing-MobileAppPromo`).isPresent();
  }
}
