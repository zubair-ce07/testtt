import { $ } from "protractor";
import { MobilePromo } from "../../../../elements/promos/mobilePromo";

export class MobilePromoKayak implements MobilePromo {
  async isPresent(): Promise<boolean> {
    return $(`.Sem-Common-Landing-MobileAppPromo`).isPresent();
  }
}
