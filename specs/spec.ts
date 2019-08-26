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
        const displayedSlidersCount = await flightSearchPage.getCountOfDisplayedTakeOffSliders();
        expect(displayedSlidersCount).to.be.at.least(2);
    });

    it(`${PageName.FlightsSearch} Should display first takeoff slider set to FRA`, async function () {
        const firstSliderTakeOffOrigin = await flightSearchPage.getSliderTakeOffOrigin(0);
        expect(firstSliderTakeOffOrigin).to.have.string('FRA');
    });

    it(`${PageName.FlightsSearch} Should display second takeoff slider set to ZRH`, async function () {
        const secondSliderTakeOffOrigin = await flightSearchPage.getSliderTakeOffOrigin(1);
        expect(secondSliderTakeOffOrigin).to.have.string('ZRH');
    });

    it(`${PageName.FlightsSearch} Should display two landing sliders in filter section`, async function () {
        const displayedSlidersCount = await flightSearchPage.getCountOfDisplayedLandingSliders();
        expect(displayedSlidersCount).to.be.at.least(2);
    });

    it(`${PageName.FlightsSearch} Should display first landing slider set to ZRH`, async function () {
        const firstSliderLandingDestination = await flightSearchPage.getSliderLandingDestination(0);
        expect(firstSliderLandingDestination).to.have.string('ZRH');
    });

    it(`${PageName.FlightsSearch} Should display second landing slider set to LON`, async function () {
        const secondSliderLandingDestination = await flightSearchPage.getSliderLandingDestination(1);
        expect(secondSliderLandingDestination).to.have.string('LON');
    });

    it(`${PageName.FlightsSearch} Select Take-off ZRH slider and slide filter - This Should reflect flight result for second leg times (ZRH-LON) `, async function () {
        const flightZRHTakeOffStartTime = await flightSearchPage.slideTakeOffSliderForZRH();
        const searchedFlightsCount = await flightSearchPage.getTotalSearchedFlightsCount();
        expect(searchedFlightsCount).to.be.above(0);

        if (searchedFlightsCount > 0) {
            const firstSearchedFlightTakeOffTime = await flightSearchPage.getTakeOffTimeForFlightZRH(0);
            expect(firstSearchedFlightTakeOffTime >= flightZRHTakeOffStartTime).to.be.true;

        }
        if (searchedFlightsCount > 1) {
            const secondSearchedFlightTakeOffTime = await flightSearchPage.getTakeOffTimeForFlightZRH(1);
            expect(secondSearchedFlightTakeOffTime >= flightZRHTakeOffStartTime).to.be.true;
        }
    });

    it(`${PageName.FlightsSearch} Should open provider page`, async function () {
        const totalOpenedTabsCount = await flightSearchPage.openDealPage();
        expect(totalOpenedTabsCount).to.equal(2);
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
        expect(cabinClass).to.have.string('Business');
    });

    it(`${PageName.FlightsSearch} Should display MC Form second cabin class set to "Business"`, async function () {
        const cabinClass = await flightSearchPage.getMultiCityFormSecondCabinClassFilter();
        expect(cabinClass).to.have.string('Business');
    });

    it(`${PageName.FlightsSearch} Should display MC Form Traveler set to "1 Adult"`, async function () {
        const travelerFilter = await flightSearchPage.getMultiCityFormTravelerFilter();
        expect(travelerFilter).to.have.string('1 Adult');
    });

    it(`${PageName.FlightsSearch} Should display MC Form first flight date filter set to applied filter`, async function () {
        const flightDateFilter = await flightPage.getFirstFlightDate();
        const dateMatched = await flightSearchPage.isMCFormFilterFirstDateMatchAppliedFilterDate(flightDateFilter);
        expect(dateMatched).to.be.true;
    });

    it(`${PageName.FlightsSearch} Should display MC Form second flight date filter set to applied filter`, async function () {
        const flightDateFilter = await flightPage.getSecondFlightDate();
        const dateMatched = await flightSearchPage.isMCFormFilterSecondDateMatchAppliedFilterDate(flightDateFilter);
        expect(dateMatched).to.be.true;
    });

    if (flightPage.isKayakSite()) {
        it(`${PageName.FlightsSearch} Clearing MC-Form filter should remove first origin and destination`, async function () {
            await flightSearchPage.clearFilter();
            const { flightOrigin, flightDestination } = await flightSearchPage.getMultiCityFormFirstAirportsFilter();
            expect(flightOrigin).to.have.string("From");
            expect(flightDestination).to.have.string("To");
        });

        it(`${PageName.FlightsSearch} Clearing MC-Form filter should remove first flight date`, async function () {
            const flightDate = await flightSearchPage.getMultiCityFormFirstFlightDateFilter();
            expect(flightDate).to.have.string("Depart");
        });

        it(`${PageName.FlightsSearch} Clearing MC-Form filter should remove second origin and destination`, async function () {
            await flightSearchPage.clearFilter();
            const { flightOrigin, flightDestination } = await flightSearchPage.getMultiCityFormSecondAirportsFilter();
            expect(flightOrigin).to.have.string("From");
            expect(flightDestination).to.have.string("To");
        });

        it(`${PageName.FlightsSearch} Clearing MC-Form filter should remove second flight date`, async function () {
            const flightDate = await flightSearchPage.getMultiCityFormSecondFlightDateFilter();
            expect(flightDate).to.have.string("Depart");
        });

        it(`${PageName.FlightsSearch} Clearing MC-Form filter should retain traveler filter`, async function () {
            const travelerFilter = await flightSearchPage.getMultiCityFormTravelerFilter();
            expect(travelerFilter).to.have.string('1 Adult');
        });

        it(`${PageName.FlightsSearch} Clearing MC-Form filter should retain first cabin class "Business"`, async function () {
            const cabinClass = await flightSearchPage.getMultiCityFormFirstCabinClassFilter();
            expect(cabinClass).to.have.string('Business');
        });

        it(`${PageName.FlightsSearch} Clearing MC-Form filter should retain second cabin class "Business"`, async function () {
            const cabinClass = await flightSearchPage.getMultiCityFormSecondCabinClassFilter();
            expect(cabinClass).to.have.string('Business');
        });
    }

    it(`${PageName.FlightsSearch} Should display error modal on clicking search button without entering origin, destination and date`, async function () {
        await flightSearchPage.clearFilter();
        await flightSearchPage.searchFlightsWithoutFillingMCForm();
        const isErrorModalDisplayed = await flightSearchPage.isErrorModalDisplayed();
        expect(isErrorModalDisplayed).to.be.true;
    });

    it(`${PageName.FlightsSearch} Error modal should display first message "Please enter a 'From' airport for flight '1'."`, async function () {
        const firstErrorMessage = await flightSearchPage.getErrorMessages(0);
        expect(firstErrorMessage).to.have.string("Please enter a 'From' airport for flight '1'.");
    });

    it(`${PageName.FlightsSearch} Error modal should display second message "Please enter a 'To' airport for flight '1'."`, async function () {
        const secondErrorMessage = await flightSearchPage.getErrorMessages(1);
        expect(secondErrorMessage).to.have.string("Please enter a 'To' airport for flight '1'.");
    });

    it(`${PageName.FlightsSearch} Error modal should display third message "Please enter a valid 'Depart' date for flight '1'."`, async function () {
        const thirdErrorMessage = await flightSearchPage.getErrorMessages(2);
        expect(thirdErrorMessage).to.have.string("Please enter a valid 'Depart' date for flight '1'.");
    });

    it(`${PageName.FlightsSearch} Clicking "OK" button on error modal should close error modal`, async function () {
        await flightSearchPage.closeErrorModal();
        const isErrorModalDisplayed = await flightSearchPage.isErrorModalDisplayed();
        expect(isErrorModalDisplayed).to.be.false;
    });
});