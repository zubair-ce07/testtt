import { Trip } from "./Trip";
import { AirportSelector } from "./Airport";
import { Passengers } from "./Passenger";
import { DateRange } from "./DateRange";
import { FlightCompare } from "./Flights";
import { FlightsResultsPage } from "../pages/FlightsResults";
import { browser, by, element, ExpectedConditions as EC } from "protractor";

export class SearchForm {
  public trip: Trip;
  public origin: AirportSelector;
  public destination: AirportSelector;
  public passengers: Passengers;
  public dateRange: DateRange;
  public compare: FlightCompare;
  
  constructor(readonly id: string) {
    this.origin = new AirportSelector(id, 'origin');
    this.compare = new FlightCompare(id);
    this.dateRange = new DateRange(id);
    this.passengers = new Passengers(`${this.id}-travelersAboveForm`);
    this.destination = new AirportSelector(id, 'destination');
  }
  
  async load() {
    const id = await this.findSelectTripTypeId();
    this.trip = new Trip(id);
  }
  
  async submit(): Promise<FlightsResultsPage> {
    const elm = element(by.id(`${this.id}-submit`));
    browser.wait(EC.visibilityOf(elm));
    browser.wait(EC.elementToBeClickable(elm));
    
    await elm.click();
    return new FlightsResultsPage(await browser.getCurrentUrl());
  }
  
  private async findSelectTripTypeId() {
    const elm = element(by.id(this.id)).all(by.css(`div[id$='-switch']`)).first();
    
    const id = await elm.getAttribute('id');
    return id.split('-')[0];
  }
  
}