import FlightPageObject from './../pageobjects/flightPageObject';
import FlightSearchResultPageObject from './../pageobjects/flightSearchResultPageObject';
import { expect } from "chai";

describe('Hotels Sanity -', () => {
    const flightPage: FlightPageObject = new FlightPageObject();
    const flightSearchPage: FlightSearchResultPageObject = new FlightSearchResultPageObject();

    enum PageName {
        Flights = "Flights Page -",
        FlightsSearch = "Flights Search Result Page -"
    }

    it(`${PageName.Flights} Should open flights front page`, async function () {
        flightPage.openHomePage();
        await flightPage.openFlightsPage();
        const isFlightsPageDisplayed = await flightPage.isFlightsPageDisplayed();
        expect(isFlightsPageDisplayed).to.be.true;
    });

    it(`${PageName.Flights} Should display atleast 2 nulticity flight legs`, async function () {
        await flightPage.setFlightsToMultiCity();
        const flightsCount = await flightPage.getDisplayedFlightsCount();
        expect(flightsCount).to.be.at.least(2);
    });

    it(`${PageName.Flights} Should set multi city flights filter"`, async function () {
        await flightPage.setFirstFlightDetail("FRA", "ZRH");
        await flightPage.setSecondFlightDetail("ZRH", "LON");
        await flightPage.searchFlights();
        // todo: check current page url, it should be search page
    });

    it(`${PageName.FlightsSearch} Should display city filter set to FRA-ZRH & ZRH-LON'`, async function () {
        const airportFilter = await flightSearchPage.getAppliedAirportFilter();
        expect(airportFilter).to.include("FRA-ZRH");
        expect(airportFilter).to.include("ZRH-LON");
    });

    it(`${PageName.FlightsSearch} Should display flight departure dates as per applied filter dates`, async function () {
        const departureDate = `${flightPage.getFirstFlightDate()}, ${flightPage.getSecondFlightDate()}`;
        const isAppliedDateMatchedDepartureDate = await flightSearchPage.doesFirstAppliedDateFilterMatchFlightDate(departureDate);
        expect(isAppliedDateMatchedDepartureDate).to.be.true;
    });

    it(`${PageName.FlightsSearch} Should display traveler set to "1 Adult"`, async function () {
        const travelerFilter = await flightSearchPage.getAppliedTravelerFilter();
        expect(travelerFilter).to.have.string('1 Adult');
    });

    it(`${PageName.FlightsSearch} Should cabin class set to "Business"`, async function () {
        const cabinClass = await flightSearchPage.getAppliedCabinClass();
        expect(cabinClass).to.have.string('Business');
    });

    it(`${PageName.FlightsSearch} Should display two takeoff sliders in filter section`, async function () {
        // todo: wait for search result list to load for site "Momondo" (this should be done in searchFlights() method
        const displayedSlidersCount = await flightSearchPage.getCountOfDisplayedTakeOffSliders();
        expect(displayedSlidersCount).to.be.at.least(2);
    });

    it(`${PageName.FlightsSearch} Should display first takeoff slider set to FRA`, async function () {
        const firstSliderTakeOffOrigin = await flightSearchPage.getSliderTakeOffOrigin(0);
        console.log('origin', firstSliderTakeOffOrigin);
        expect(firstSliderTakeOffOrigin).to.have.string('FRA');
    });

    it(`${PageName.FlightsSearch} Should display second takeoff slider set to ZRH`, async function () {
        const secondSliderTakeOffOrigin = await flightSearchPage.getSliderTakeOffOrigin(1);
        console.log('origin', secondSliderTakeOffOrigin);
        expect(secondSliderTakeOffOrigin).to.have.string('ZRH');
    });

    it(`${PageName.FlightsSearch} Should display two landing sliders in filter section`, async function () {
        // todo: wait for search result list to load for site "Momondo" (this should be done in searchFlights() method
        const displayedSlidersCount = await flightSearchPage.getCountOfDisplayedLandingSliders();
        expect(displayedSlidersCount).to.be.at.least(2);
    });

    it(`${PageName.FlightsSearch} Should display first landing slider set to ZRH`, async function () {
        const firstSliderLandingDestination = await flightSearchPage.getSliderLandingDestination(0);
        console.log('origin', firstSliderLandingDestination);
        expect(firstSliderLandingDestination).to.have.string('ZRH');
    });

    it(`${PageName.FlightsSearch} Should display second landing slider set to LON`, async function () {
        const secondSliderLandingDestination = await flightSearchPage.getSliderLandingDestination(1);
        console.log('origin', secondSliderLandingDestination);
        expect(secondSliderLandingDestination).to.have.string('LON');
    });

    it(`Select Take-off ZRH slider and slide filter`, function () {
        // TO BE DONE: Task 6
    });

    it(`Click the "View Deal" button for the first result`, function () {
        // TO BE DONE: Task 7
    });

    it(`Go back to the flight result page`, function () {
        // TO BE DONE: Task 8
    });

    it(`${PageName.FlightsSearch} Should display Multi-City Form`, async function () {
        await flightSearchPage.searchFlightAgain();
        const isMultiCityFormDisplayed = await flightSearchPage.isMultiFormDisplayed();
        expect(isMultiCityFormDisplayed).to.be.true;

    });

    it(`${PageName.FlightsSearch} Should display MC Form first airport filter set to FRA-ZRH`, async function () {
        const { flightOrigin, flightDestination } = await flightSearchPage.getMultiCityFormFirstAirportsFilter();
        expect(flightOrigin).to.have.string('FRA');
        expect(flightDestination).to.have.string('ZRH');
    });

    it(`${PageName.FlightsSearch} Should display MC Form second airport filter set to ZRH-LON`, async function () {
        const { flightOrigin, flightDestination } = await flightSearchPage.getMultiCityFormSecondAirportsFilter();
        expect(flightOrigin).to.have.string('ZRH');
        expect(flightDestination).to.have.string('LON');
    });

    it(`${PageName.FlightsSearch} Should display MC Form first cabin class set to "Business"`, async function () {
        const cabinClass = await flightSearchPage.getMultiCityFormFirstCabinClassFilter();
        console.log('cabin class', cabinClass);
        expect(cabinClass).to.have.string('Business');
    });

    it(`${PageName.FlightsSearch} Should display MC Form second cabin class set to "Business"`, async function () {
        const cabinClass = await flightSearchPage.getMultiCityFormSecondCabinClassFilter();
        console.log('cabin class', cabinClass);
        expect(cabinClass).to.have.string('Business');
    });

    it(`${PageName.FlightsSearch} Should display MC Form Traveler set to "1 Adult"`, async function () {
        const travelerFilter = await flightSearchPage.getMultiCityFormTravelerFilter();
        console.log('traveler filter', travelerFilter);
        expect(travelerFilter).to.have.string('1 Adult');
    });
});