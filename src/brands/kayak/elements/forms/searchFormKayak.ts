import { SearchForm } from "../../../../elements/forms/searchForm";
import { CompareTo } from "../../../../elements/compareTo";
import { DateRange } from "../../../../elements/input/dateRange";
import { Destination } from "../../../../elements/input/destination";
import { CompareToKayak } from "../compareToKayak";
import { DateRangeKayak } from "../input/dateRangeKayak";
import { DestinationKayak } from "../input/destinationKayak";

export class SearchFormKayak implements SearchForm {
  getCompareTo(): CompareTo {
    return new CompareToKayak();
  }
  
  getDateRange(): DateRange {
    return new DateRangeKayak();
  }
  
  getDestination(): Destination {
    return new DestinationKayak();
  }
  
}
