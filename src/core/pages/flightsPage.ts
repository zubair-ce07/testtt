import { MultiCityFlightSearchForm } from "../elements/forms/multiCityFlightSearchForm";
import { FormType } from "../elements/enums";

export interface FlightsPage {
  getURL(): string;
  
  getSearchFormType(): Promise<string>;
  
  setSearchFormType(type: FormType): Promise<void>;
  
  getMultiCityForm(): MultiCityFlightSearchForm;
  
  search(): Promise<unknown>;
}
