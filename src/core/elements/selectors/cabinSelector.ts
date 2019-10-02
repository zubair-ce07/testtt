import { CabinType } from "../types/cabinType";

export interface CabinSelector {
  setType(option: CabinType): Promise<void>;
  
  getDisplayText(): Promise<string>;
}
