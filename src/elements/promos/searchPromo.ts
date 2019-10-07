import { Promo } from "./promo";

export interface SearchPromo extends Promo {
  searchNow(): Promise<void>;
}
