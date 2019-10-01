import { CabinType } from "./cabinType";

export interface CabinSelector {
  select(option: CabinType): Promise<void>;
  
  getDisplayText(): Promise<string>;
}
