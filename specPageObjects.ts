var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
import {flightResultsPage} from './flightResultsPage'

describe('Flight Prediction Graph: ', function() {

	let flightResults = new flightResultsPage();
	
	before("Should open kayak site and maximize browser", async function() {
		await flightResults.isNonAngularApplication();
		await flightResults.get();
		await flightResults.maximizeBrowser(); 
		
	});

	it("Should show xxx of XXXX flights on top", async function() {
		
		await flightResults.closePopup();
		expect(await flightResults.getFlightsCount()).to.match(/^[0-9]+ of [0-9]+ flights$/gm);
	});

	it("Should all stop filters be checked and prices listed next to them", async function() {

		expect(await flightResults.isStopFiltersChecked()).to.be.true;
		expect(await flightResults.isStopFiltersContainPrices()).to.be.true;
	});

	it("Should be able to highlighted and show only link on hover", async function() {

		expect(await flightResults.isStopFiltersHighlightedAndShowOnlyOnHover()).to.be.true;
	});

	it("Should be able to select non stop only and verify if results contain non stop flights only", async function() {

		await flightResults.hoverAndClickNonStopOnlyLink();
		expect(await flightResults.isResultsContainNonStopOnly()).to.be.true;
	});

	it("Should show reset link at top of stop filters", async function() {

		expect(await flightResults.isResetLinkAppeared()).to.be.true;
	});

	it("Should be able to check one stop and verify if results contain one stop as well", async function() {

		await flightResults.clickOneStopCheckbox();
		expect(await flightResults.isResultsContainNonStopAndOneStopOnly()).to.be.true;
	});

	it("Should be able check Depart/Return Same and verify if results contain Depart and Return Same", async function() {

		await flightResults.clickSameDepartAndReturn();
		expect(await flightResults.isResultsContainDepartAndReturnSame()).to.be.true;
	});

	it("Should be able to uncheck Depart/Return Same and verify if results contain either Depart and Return same or not", async function() {

		await flightResults.clickSameDepartAndReturn();
		expect(await flightResults.isResultsContainDepartAndReturnSame()).to.be.true;
	});

	it("Should be able to uncheck EWR Airport and verify if results don't contain EWR airport", async function() {

		await flightResults.clickEWRCheckbox();
		expect(await flightResults.isResultsContainEWRAirport()).to.be.true;
	});

	it("Should be able to click Price for JetBlue Airways and verify if results contain jetblue Airways only", async function() {

		await flightResults.clickJetBluePrice();
		expect(await flightResults.isResultsContainJetBlueAirwaysOnly()).to.be.true;
	});

	it("Should be able to uncheck economy cabin and verify if results don't contain economy cabins", async function() {

		await flightResults.clickCabinTitle();
		await flightResults.uncheckEconomyFilter();
		expect(await flightResults.isResultsNotContainEconomyCabins()).to.be.true;
	});

	it("Should be able click reset link on cabins and verify if result contain economy cabins", async function() {

		await flightResults.clickResetCabinLink();
		expect(await flightResults.isResultsNotContainEconomyCabins()).to.be.false;
	});

	it("Should be able to check long flights and verify if count of total flights increases", async function() {

		const flightCountBefore = await flightResults.getTotalFlights();
		await flightResults.clickFlightQualityTitle();
		await flightResults.clickLongFlightsFilter();
		const flightCountAfter = await flightResults.getTotalFlights();
		
		expect(flightCountBefore).to.be.below(flightCountAfter);
	});

	it("Should be able to select Alaska Airlines provider and verify if results contain that provider only", async function() {

		await flightResults.clickBookingSitesTitle();
		await flightResults.selectAlaskaAirlines();
		expect(await flightResults.isResultsContainsAlaskaAirlinesOnly()).to.be.true;
	});

	it("Should be able to click at top of booking providers filter and verify if results contain all providers", async function() {

		await flightResults.clickBookingProviderResetLink();
		expect(await flightResults.isResultsContainsAlaskaAirlinesOnly()).to.be.false;
	});

	it("Should be able to select any provider price and verify if it is equal to cheapest price", async function() {

		await flightResults.selectAlaskaAirlines();
		expect(await flightResults.getCheapestPrice()).to.be.equal(await flightResults.getBookingProviderFilterPrice());
	});

	it("Should be able to click reset link at top of booking providers filter and verify if results contain providers again", async function() {

		await flightResults.clickBookingProviderResetLink();
		expect(await flightResults.isResultsContainsAlaskaAirlinesOnly()).to.be.false;
	});

	it("should be able to click xxx of XXX on top and verify if all filters are reset again", async function() {

		await flightResults.clickTopFlightsLink();
		expect(await flightResults.isResultsContainsAlaskaAirlinesOnly()).to.be.false;
		expect(await flightResults.isResultsContainJetBlueAirwaysOnly()).to.be.false;
		expect(await flightResults.isResultsNotContainEconomyCabins()).to.be.false;
	});
});
