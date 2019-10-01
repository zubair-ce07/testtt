import { CabinType } from "../types/cabinType";

export interface CabinSelector {
  select(option: CabinType): Promise<void>;
  
  getDisplayText(): Promise<string>;
}
