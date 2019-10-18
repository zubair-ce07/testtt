import { browser } from 'protractor';
import { expect } from 'chai';
import { range, reduceHaveText, reduceIsSame, removeFlightLegsUntilResults, } from "../src/utils/spec.utils";
import { addDays, toDateString } from "../src/utils/date.util";
import { FlightsPage } from "../src/core/pages/flightsPage";
import { FormType } from "../src/core/elements/enums";
import { FlightsResultsPage } from "../src/core/pages/flightsResultsPage";
import { FlightsPageKayak } from "../src/brands/kayak/pages/flightsPage.kayak";
import { FlightsResultsPageKayak } from "../src/brands/kayak/pages/flightsResultsPage.kayak";

const flights: FlightsPage = new FlightsPageKayak();
const results: FlightsResultsPage = new FlightsResultsPageKayak();

describe('kayak.com/flights', () => {
  
  const TRAVELLERS_TEXT = '1 Traveller';
  const FLIGHT_LEGS_DATA = [
    { origin: 'BOS', destination: 'MIA', days: 7, },
    { origin: 'MIA', destination: 'LAX', days: 14, },
    { origin: 'LAX', destination: 'CHI', days: 21, },
    { origin: 'CHI', destination: 'NYC', days: 28, },
    { origin: 'NYC', destination: 'DFW', days: 35, },
    { origin: 'DFW', destination: 'WAS', days: 42, },
  ];
  
  const FIRST_LEG = FLIGHT_LEGS_DATA[0];
  const LAST_LEG = FLIGHT_LEGS_DATA[FLIGHT_LEGS_DATA.length - 1];
  
  const DEPARTURE_DATE = addDays(new Date(), FIRST_LEG.days);
  const RETURN_DATE = addDays(new Date(), LAST_LEG.days);
  
  it('should be able to load Flight Front Door', async () => {
    const url = 'https://www.kayak.com/flights';
    await browser.get(url);
    expect(await browser.getCurrentUrl()).equal(url);
  });
  
  it('should be able to tap on Multi city tab', async () => {
    await flights.setSearchFormType(FormType.MultiCity);
    expect(await flights.getSearchFormType()).equal(FormType.MultiCity);
  });
  
  it('should show 2 legs by default', async () => {
    expect(await flights.getMultiCityForm().getFlightLegs()).length.to.equal(2);
  });
  
  range(0, 2).forEach(leg => {
    const flightLeg = flights.getMultiCityForm().getFlightLeg(leg);
    
    it(`should show Origin Selector on leg ${leg + 1}`, async () => {
      expect(await flightLeg.getOrigin().isDisplayed()).is.true;
    });
    
    it(`should show Destination Selector on leg ${leg + 1}`, async () => {
      expect(await flightLeg.getDestination().isDisplayed()).is.true;
    });
    
    it(`should show Date Picker on leg ${leg + 1}`, async () => {
      expect(await flightLeg.getDatePicker().isDisplayed()).is.true;
    });
  });
  
  it('should add another leg when Add button is tapped', async () => {
    const form = flights.getMultiCityForm();
    await form.addFlightLegs(1);
    expect(await form.getFlightLegs()).length.to.equal(3);
  });
  
  it('should add 3 more legs when Add button is tapped {5} times', async () => {
    const form = flights.getMultiCityForm();
    await form.addFlightLegs(1);
    expect(await form.getFlightLegs()).length.to.equal(6);
  });
  
  it('should remove the last leg when Remove button is tapped', async () => {
    const form = flights.getMultiCityForm();
    await form.removeFlightLegs(1);
    expect(await form.getFlightLegs()).to.equal(5);
  });
  
  it('should add another leg when Add button is tapped', async () => {
    const form = flights.getMultiCityForm();
    await form.addFlightLegs(1);
    expect(await form.getFlightLegs()).length.to.equal(6);
  });
  
  FLIGHT_LEGS_DATA.forEach((leg, index) => {
    const flightLeg = flights.getMultiCityForm().getFlightLeg(index);
    
    it(`should set leg: ${index + 1} origin as ${leg.origin}`, async () => {
      const origin = flightLeg.getOrigin();
      await origin.select(leg.origin);
      expect(await origin.getDisplayText()).to.contain(leg.origin);
    });
    
    it(`should set leg: ${index + 1} destination as ${leg.destination}`, async () => {
      const destination = flightLeg.getDestination();
      await destination.select(leg.destination);
      expect(await destination.getDisplayText()).to.contain(leg.destination);
    });
    
    it(`should set leg: ${index + 1} date as {Today+${leg.days}}`, async () => {
      const datePicker = flightLeg.getDatePicker();
      const sevenDaysFromNow = addDays(new Date(), leg.days);
      await datePicker.select(sevenDaysFromNow);
      expect(await datePicker.getDisplayText()).to.equal(toDateString(sevenDaysFromNow));
    });
  });
  
  it('should be able to tap on the search CTA', async () => {
    await flights.search();
  });
  
  it(`should show ${FIRST_LEG.origin} - ${LAST_LEG.destination} in flight results summary`, async () => {
    expect(await results.getSearchSummary().getFlightsDisplayText()).is(`${FIRST_LEG.origin}-${FIRST_LEG.destination}`)
  });
  
  it(`should show {Today+${FIRST_LEG.days} - {Today+${LAST_LEG.days} in flights results summary`, async () => {
    const withDay = true;
    
    const displayDateString = [
      toDateString(DEPARTURE_DATE, withDay), toDateString(RETURN_DATE, withDay),
    ].join(' – ');
    
    expect(await results.getSearchSummary().getDisplayDate()).is.equal(displayDateString);
  });
  
  it(`should show ${TRAVELLERS_TEXT} in flights results summary`, async () => {
    expect(await results.getSearchSummary().getTravellers()).is(TRAVELLERS_TEXT)
  });
  
  it('should wait for the search to complete', async () => {
    await results.loadResults();
    expect(await results.isLoaded()).is.true;
  });
  
  it('should go back to the front door and remove the last leg if no results show up (fail the test if no results show up for a 3 leg search)', async () => {
    expect(await removeFlightLegsUntilResults(flights, results, 3)).is.true;
  });
  
  it('should show Airline logo on all legs on any flight card', async () => {
    const result = results.getFlightResult(0);
    const airlinesLogo = await Promise.all(
      range(0, 6).map(leg => result.getFlightLeg(leg).getAirlineLogo())
    );
    
    expect(reduceHaveText(airlinesLogo)).is.true;
  });
  
  it('should show departure time on all legs on any flight card', async () => {
    const result = results.getFlightResult(0);
    const departureTimes = await Promise.all(
      range(0, 6).map(leg => result.getFlightLeg(leg).getDepartureTime())
    );
    
    expect(reduceHaveText(departureTimes)).is.true;
  });
  
  it('should show arrival time on all legs on any flight card', async () => {
    const result = results.getFlightResult(0);
    const arrivalTimes = await Promise.all(
      range(0, 6).map(leg => result.getFlightLeg(leg).getArrivalTime())
    );
    
    expect(reduceHaveText(arrivalTimes)).is.true;
  });
  
  it('should show departure airport codes for all legs on any flight card', async () => {
    const result = results.getFlightResult(0);
    const departureAirportCodes = await Promise.all(
      range(0, 6).map(leg => result.getFlightLeg(leg).getDepartureAirportCode())
    );
    
    expect(reduceHaveText(departureAirportCodes)).is.true;
  });
  
  it('should show arrival airport Codes for all legs on any flight card', async () => {
    const result = results.getFlightResult(0);
    const arrivalAirportCodes = await Promise.all(
      range(0, 6).map(leg => result.getFlightLeg(leg).getArrivalAirportCode())
    );
    
    expect(reduceHaveText(arrivalAirportCodes)).is.true;
  });
  
  it('should show duration for all legs on any flight card', async () => {
    const result = results.getFlightResult(0);
    const flightNumbers = await Promise.all(
      range(0, 6).map(leg => result.getFlightLeg(leg).getDuration())
    );
    
    expect(reduceHaveText(flightNumbers)).is.true;
  });
  
  it('should show price on any flight card', async () => {
    const result = results.getFlightResult(0);
    expect(await result.getPrice()).is.not.null;
  });
  
  it('should be able to tap on any flight card', async () => {
    const result = results.getFlightResult(0);
    await result.click();
    expect(await result.getDialog().isDisplayed()).is.true;
  });
  
  it('should show matching departure airport codes in the Flight Detail Page (same as FRP)', async () => {
    const result = results.getFlightResult(0);
    const dialog = result.getDialog();
    
    const airportDepartureCodes = await Promise.all(
      range(0, 6).map((leg) =>
        Promise.all([
          result.getFlightLeg(leg).getDepartureAirportCode(),
          dialog.getFlightLeg(leg).getDepartureAirportCode(),
        ])
      )
    );
    
    expect(reduceIsSame(airportDepartureCodes)).is.true;
  });
  
  it('should show matching arrival airport codes in the Flight Detail Page (same as FRP)', async () => {
    const result = results.getFlightResult(0);
    const dialog = result.getDialog();
    
    const airportArrivalCodes = await Promise.all(
      range(0, 6).map((leg) =>
        Promise.all([
          result.getFlightLeg(leg).getArrivalAirportCode(),
          dialog.getFlightLeg(leg).getArrivalAirportCode(),
        ])
      )
    );
    
    expect(reduceIsSame(airportArrivalCodes)).is.true;
  });
  
  it(`should show {Today+${FIRST_LEG.days}} as departure date in the FDP`, async () => {
    const dialog = results.getFlightResult(0).getDialog();
    expect(await dialog.getDepartureDate()).is.equal(toDateString(DEPARTURE_DATE));
  });
  
  it(`should show {Today+${LAST_LEG.days} as return date in the FDP`, async () => {
    const dialog = results.getFlightResult(0).getDialog();
    expect(await dialog.getReturnDate()).is.equal(toDateString(RETURN_DATE));
  });
  
  it(`should show "${TRAVELLERS_TEXT}" in the FDP`, async () => {
    const dialog = results.getFlightResult(0).getDialog();
    expect(await dialog.getTravellers()).is(TRAVELLERS_TEXT);
  });
  
  it('should show same price on FDP as the price on FRP', async () => {
    const result = results.getFlightResult(0);
    const dialog = result.getDialog();
    expect(await result.getPrice()).is.same(await dialog.getPrice())
  });
  
  it('should show matching departure times for all legs on the FDP (same as FRP)', async () => {
    const result = results.getFlightResult(0);
    const dialog = result.getDialog();
    
    const departureTimes = await Promise.all(
      range(0, 6).map((leg) =>
        Promise.all([
          result.getFlightLeg(leg).getDepartureTime(),
          dialog.getFlightLeg(leg).getDepartureTime(),
        ])
      )
    );
    
    expect(reduceIsSame(departureTimes)).is.true;
  });
  
  it('should show matching arrival times for all legs on the FDP (same as FRP)', async () => {
    const result = results.getFlightResult(0);
    const dialog = result.getDialog();
    
    const arrivalTimes = await Promise.all(
      range(0, 6).map((leg) =>
        Promise.all([
          result.getFlightLeg(leg).getArrivalTime(),
          dialog.getFlightLeg(leg).getArrivalTime(),
        ])
      )
    );
    
    expect(reduceIsSame(arrivalTimes)).is.true;
  });
  
  it('should show matching duration for all legs on the FDP (same as FRP)', async () => {
    const result = results.getFlightResult(0);
    const dialog = result.getDialog();
    
    const durations = await Promise.all(
      range(0, 6).map((leg) =>
        Promise.all([
          result.getFlightLeg(leg).getDuration(),
          dialog.getFlightLeg(leg).getDuration(),
        ])
      )
    );
    
    expect(reduceIsSame(durations)).is.true;
  });
  
  it('should show flight # on each leg in the FDP', async () => {
    const dialog = results.getFlightResult(0).getDialog();
  
    const flightNumbers = await Promise.all(
      range(0, 6).map(leg => dialog.getFlightLeg(leg).getFlightNumber())
    );
  
    expect(reduceHaveText(flightNumbers)).is.true;
  });
  
  it('should show cabin class on each leg in the FDP', async () => {
    const dialog = results.getFlightResult(0).getDialog();
  
    const cabinClasses = await Promise.all(
      range(0, 6).map(leg => dialog.getFlightLeg(leg).getCabinClass())
    );
  
    expect(reduceHaveText(cabinClasses)).is.true;
  });
});
