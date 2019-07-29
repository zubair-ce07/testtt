var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
import {FlightResultsPage} from './FlightResultsPage'

describe('Flight Prediction Graph: ', function() {

	const flightResults = new FlightResultsPage();
	const flightCountBefore = flightResults.getTotalFlights();

	before("Should open kayak site and close popup dialog", async function() {
		
		await flightResults.get();
		await flightResults.closePopupDialog();
	});

	it("Should FPP(Flight Prediction Price) graph Appears in Left Rail", async function() {
		
		expect(await flightResults.farePredictionPriceDisplayed()).to.be.true;
	});

	it("Should show xxx of XXXX flights on top", async function() {
		
		expect(await flightResults.getFlightsCount()).to.match(/^[0-9]+ of [0-9]+ flights$/gm);
	});

	it("Should check all airport stops", async function() {

		expect(await flightResults.airportStopFiltersChecked()).to.be.true;
	});

	it("Should display prices next to all stops", async function() {

		expect(await flightResults.airportStopFiltersContainPrices()).to.be.true;
	});

	it("Should hover cursor over each stop option and verify if line is highlighted in blue and a 'only' link appears", async function() {

		expect(await flightResults.airportStopFiltersHighlightedAndAppearOnlyOnHover()).to.be.true;
	});

	it("Should click nonstop only link and verify if nonstop results are listed only", async function() {

		await flightResults.hoverAndClickNonStopOnlyLink();
		expect(await flightResults.resultsContainNonStopOnly()).to.be.true;
	});

	it("Should appear reset link on the top of stop filters", async function() {

		expect(await flightResults.stopResetLinkDisplayed()).to.be.true;
	});

	it("Should click onestop checkbox and verify if results include 1 stop flights along with nonstop", async function() {

		await flightResults.clickOneStopCheckbox();
		expect(await flightResults.oneStopChecked()).to.be.true;
	});

	it("Should results include 1 stop flights along with nonstop", async function() {

		expect(await flightResults.resultsContainNonStopAndOneStopOnly()).to.be.true;
	});

	it("Should check 'Depart/Return Same' under Airports", async function() {

		await flightResults.checkSameDepartureAndReturnAirport();
		expect(await flightResults.sameDepartureAndReturnAirportChecked()).to.be.true;
	});

	it("Should results have the same departure and return airport", async function() {

		expect(await flightResults.resultsContainDepartAndReturnSame()).to.be.true;
	});

	it("should display fewer number of flight results", async function() {

		const flightCountAfter = await flightResults.getTotalFlights();
		expect(flightCountBefore).to.eventually.be.most(flightCountAfter);
	});

	it("Should uncheck 'Depart/Return Same' under airports", async function() {

		await flightResults.uncheckSameDepartureAndReturnAirport();
		expect(await flightResults.sameDepartureAndReturnAirportChecked()).to.be.false;
	});

	it("Should results with different departure and arrival airports listed again", async function() {

		expect(await flightResults.resultsContainDepartAndReturnSameAndDifferent()).to.be.true;
	});

	it("Should check EWR under Airports", async function() {

		await flightResults.checkEwrAirport();
		expect(await flightResults.ewrAirportChecked()).to.be.true;
	});

	it("Should results do not include results with EWR", async function() {

		expect(await flightResults.resultsNotContainEWRAirport()).to.be.true;
	});

	it("Should click Price for JetBlue Airways under airlines and verify if jetblue Airways results listed only", async function() {

		await flightResults.clickJetBluePrice();
		expect(await flightResults.resultsContainJetBlueAirwaysOnly()).to.be.true;
	});

	it("Should uncheck economy cabin under cabins", async function() {

		await flightResults.uncheckEconomyCabin();
		expect(await flightResults.economyCabinChecked()).to.be.false;
	});

	it("Should results do not include Economy cabin results", async function() {

		expect(await flightResults.resultsNotContainEconomyCabins()).to.be.true;
	});

	it("Should click reset link above cabins and verify if results include all cabin classes", async function() {

		await flightResults.clickResetCabinLink();
		expect(await flightResults.resultsContainAllCabins()).to.be.false;
	});

	it("Should check 'Show xx longer flights' filter option", async function() {

		await flightResults.checkLongFlightsFilter();
		expect(flightResults.longFlightsFilterChecked()).to.be.true;
	});

	it("Should number of results is now more than what it was", async function() {

		const flightCountAfter = await flightResults.getTotalFlights();
		expect(flightCountBefore).to.eventually.be.below(flightCountAfter);
	});


	it("Should click Alaska Airlines only link under booking providers and verify if results contain Alaska Airlines results only", async function() {

		await flightResults.selectAlaskaAirlines();
		expect(await flightResults.resultsContainsAlaskaAirlinesOnly()).to.be.true;
	});

	it("Should click reset link and verify if all booking provider results are displayed", async function() {

		await flightResults.clickBookingProviderResetLink();
		expect(await flightResults.resultsContainsAlaskaAirlinesOnly()).to.be.false;
	});

	it("Should click any provider price and verify if click price should match cheapest result", async function() {

		await flightResults.selectAlaskaAirlines();
		expect(await flightResults.getCheapestPrice()).to.be.equal(await flightResults.getBookingProviderFilterPrice());
	});

	it("Should click reset link in the booking providers and verify if all providers results are displayed", async function() {

		await flightResults.clickBookingProviderResetLink();
		expect(await flightResults.resultsContainsAllProviders()).to.be.false;
	});

	it("should click xxx of XXXX on top of the page and verify if all filters are unset again", async function() {

		await flightResults.clickTopFlightsLink();
		expect(await flightResults.resetAllFilters()).to.be.false;
	});
});
