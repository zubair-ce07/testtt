import { FlightsPage } from "../../../core/pages/flightsPage";
import { MultiCityFlightSearchForm } from "../../../core/elements/forms/multiCityFlightSearchForm";
import { FormType } from "../../../core/elements/enums";
import { MultiCityFlightSearchFormKayak } from "../elements/forms/multiCityFlightSearchForm.kayak";

export class FlightsPageKayak implements FlightsPage {
  getMultiCityForm(): MultiCityFlightSearchForm {
    return new MultiCityFlightSearchFormKayak();
  }
  
  getSearchFormType(): Promise<string> {
    return undefined;
  }
  
  getURL(): string {
    return "";
  }
  
  search(): Promise<unknown> {
    return undefined;
  }
  
  setSearchFormType(type: FormType): Promise<void> {
    return undefined;
  }
  
}
