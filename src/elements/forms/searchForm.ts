import { CompareTo } from "../compareTo";
import { DateRange } from "../input/dateRange";
import { Destination } from "../input/destination";

export interface SearchForm {
  
  getDateRange(): DateRange;
  
  getCompareTo(): CompareTo;
  
  getDestination(): Destination;
}
