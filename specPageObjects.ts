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

	it("Should display xxx of XXXX flights on top", async function() {
		
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

	it("Should click nonstop 'only' link", async function() {

		await flightResults.hoverAndClickNonStopOnlyLink();
		expect(await flightResults.nonStopChecked()).to.be.true;
	});

	it("Should display results with nonstop only", async function() {

		expect(await flightResults.resultsContainNonStopOnly()).to.be.true;
	});

	it("Should display reset link on the top of stop filters", async function() {

		expect(await flightResults.stopResetLinkDisplayed()).to.be.true;
	});

	it("Should click onestop checkbox", async function() {

		await flightResults.clickOneStopCheckbox();
		expect(await flightResults.oneStopChecked()).to.be.true;
	});

	it("Should display results with 1-stop and non-stop", async function() {

		expect(await flightResults.resultsContainNonStopAndOneStopOnly()).to.be.true;
	});

	it("Should check 'Depart/Return Same' under Airports", async function() {

		await flightResults.checkSameDepartureAndReturnAirport();
		expect(await flightResults.sameDepartureAndReturnAirportChecked()).to.be.true;
	});

	it("Should display results with same departure and return airport", async function() {

		expect(await flightResults.resultsContainDepartureAndReturnSame()).to.be.true;
	});

	it("should display fewer number of flight results", async function() {

		const flightCountAfter = await flightResults.getTotalFlights();
		expect(flightCountBefore).to.eventually.be.most(flightCountAfter);
	});

	it("Should uncheck 'Depart/Return Same' under airports", async function() {

		await flightResults.uncheckSameDepartureAndReturnAirport();
		expect(await flightResults.sameDepartureAndReturnAirportChecked()).to.be.false;
	});

	it("Should display results with different departure and arrival airports", async function() {

		expect(await flightResults.resultsContainDepartureAndReturnSameAndDifferent()).to.be.true;
	});

	it("Should check EWR under Airports", async function() {

		await flightResults.checkEwrAirport();
		expect(await flightResults.ewrAirportChecked()).to.be.true;
	});

	it("Should display results without EWR airport", async function() {

		expect(await flightResults.resultsNotContainEWRAirport()).to.be.true;
	});

	it("Should click Price for JetBlue Airways", async function() {

		await flightResults.clickJetBluePrice();
		expect(await flightResults.jetBlueAirlineChecked()).to.be.true;
	});

	it("Should display results with jetblue Airways only", async function() {

		expect(await flightResults.resultsContainJetBlueAirwaysOnly()).to.be.true;
	});

	it("Should uncheck economy cabin under cabins", async function() {

		await flightResults.uncheckEconomyCabin();
		expect(await flightResults.economyCabinChecked()).to.be.false;
	});

	it("Should results do not include Economy cabin results", async function() {

		expect(await flightResults.resultsNotContainEconomyCabins()).to.be.true;
	});

	it("Should click reset link above cabins", async function() {

		await flightResults.clickResetCabinLink();
		expect(await flightResults.resetCabinLinkDisplayed()).to.be.false;
	});

	it("Should display results with all cabin classes", async function() {

		expect(await flightResults.resultsContainAllCabins()).to.be.true;
	});

	it("Should check 'Show xx longer flights' filter option", async function() {

		await flightResults.checkLongFlightsFilter();
		expect(flightResults.longFlightsFilterChecked()).to.be.true;
	});

	it("Should display more number of results", async function() {

		const flightCountAfter = await flightResults.getTotalFlights();
		expect(flightCountBefore).to.eventually.be.below(flightCountAfter);
	});


	it("Should click Alaska Airlines 'only' link", async function() {

		await flightResults.selectAlaskaAirlines();
		expect(await flightResults.alaskaAirlinesFilterChecked()).to.be.true;
	});

	it("Should display results with Alaska Airlines only", async function() {

		expect(await flightResults.resultsContainsAlaskaAirlinesOnly()).to.be.true;
	});

	it("Should click reset link", async function() {

		await flightResults.clickBookingProviderResetLink();
		expect(await flightResults.bookingProviderResetLinkDisplayed()).to.be.false;
	});

	it("Should display results with all booking providers", async function() {

		expect(await flightResults.resultsContainsAlaskaAirlinesOnly()).to.be.false;
	});

	it("Should click CheapoAir provider price", async function() {

		await flightResults.clickCheapoAirBookingProviderPrice();
		expect(await flightResults.cheapoairBookingProviderCheckbox).to.be.true;
	});

	it("Should CheapoAir price matches cheapest result", async function() {

		await flightResults.selectAlaskaAirlines();
		expect(await flightResults.getCheapestPrice()).to.be.equal(await flightResults.getCheapoAirBookingProviderPrice());
	});

	it("Should click xxx of XXXX on top and verify if all filters reset again", async function() {

		await flightResults.clickTopFlightsLink();
		expect(await flightResults.resetAllFilters()).to.be.false;
	});

});
