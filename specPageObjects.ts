var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
import {browser} from 'protractor';
import {Factory} from './Factory'
import {Helper} from './Helper';
import {KayakFlightsPage} from './KayakFlightsPage';
import {KayakFlightsResultsPage} from './KayakFlightsResultsPage';
import {BookingProviderPage} from './BookingProviderPage';

const helper = new Helper();
const factory = new Factory();
const flightsPage: any = factory.createPageObject(`${browser.params.page}FlightsPage`);
const flightsResultPage: any =  factory.createPageObject(`${browser.params.page}FlightsResultsPage`);
const providerPage: BookingProviderPage =  new BookingProviderPage();

describe("Kayak Flights Page:", function() {

	before("Should open flights page", async function() {
		await flightsPage.get();
	});

	it("Should select multiple cities Trip option", async function() {
		await flightsPage.selectMultipleCitiesOption();
		expect(await flightsPage.multipleCitiesOptionSelected()).to.be.true;
	});

	it("Should display multiple cities form", async function() {
		expect(await flightsPage.multipleCitiesFormDisplayed()).to.be.true;
	});

	it("Should display 3 legs in a multiple cities form", async function() {
		expect(await flightsPage.threeLegsDisplayedInMultipleCitiesForm()).to.be.true;
	});

	it("Should enter FRA in leg one's origin airport", async function() {
		await flightsPage.setValueOfOriginAirportInLegOne("FRA");
		expect(await flightsPage.getValueOfOriginAirportInLegOne()).to.be.include("FRA");
	});

	it("Should enter ZRH in leg one's destination airport", async function() {
		await flightsPage.setValueOfDestinationAirportInLegOne("ZRH");
		expect(await flightsPage.getValueOfDestinationAirportInLegOne()).to.be.include("ZRH");
	});

	it("Should enter ZRH in leg two's origin airport", async function() {
		await flightsPage.setValueOfOriginAirportInLegTwo("ZRH");
		expect(await flightsPage.getValueOfOriginAirportInLegTwo()).to.be.include("ZRH");
	});

	it("Should enter LON in leg two's destination airport", async function() {
		await flightsPage.setValueOfDestinationAirportInLegTwo("LON");
		expect(await flightsPage.getValueOfDestinationAirportInLegTwo()).to.be.include("LON");
	});

	it("Should select business cabin from leg one's cabins", async function() {
		await flightsPage.clickCabinsSelectBoxOfLegOne();
		await flightsPage.selectBusinessCabinInLegOne();
		expect(await flightsPage.getSelectedCabinOfLegOne()).to.be.equal("Business");
	});

	it("Should select business cabin from leg two's cabins", async function() {
		await flightsPage.clickCabinsSelectBoxOfLegTwo();
		await flightsPage.selectBusinessCabinInLegTwo();
		expect(await flightsPage.getSelectedCabinOfLegTwo()).to.be.equal("Business");
	});

	it("Should select any date for leg one", async function() {
		await flightsPage.clickDateBoxOfLegOne();
		await flightsPage.selectDateOfLegOne();
		expect(await flightsPage.getSelectedDateOfLegOne()).to.be.true;
	});

	it("Should select any date for leg two", async function() {
		await flightsPage.clickDateBoxOfLegTwo();
		await flightsPage.selectDateOfLegTwo();
		expect(await flightsPage.getSelectedDateInLegTwo()).to.be.true;
	});

	it("Should click search button takes to Flight Results Page", async function() {
		await flightsPage.clickSearchButton();
		expect(await flightsResultPage.airportTimesFilterDisplayed()).to.be.true;
	});
});

describe("Kayak Flights Result Page:", function() {
	
	before("Should click search Form", async function() {
		await flightsResultPage.clickSearchForm();
	});

	it("Should display FRA Airport be selected in leg one's origin airport", async function() {
		expect(await flightsResultPage.getOriginAirportOfLegOne()).to.be.include("FRA");
	});

	it("Should display ZRH Airport be selected in leg one's destination airport", async function() {
		expect(await flightsResultPage.getDestinationAirportOfLegOne()).to.be.include("ZRH");
	});

	it("should display ZRH Airport be selected in leg two's origin airport", async function() {
		expect(await flightsResultPage.getOriginAirportOfLegTwo()).to.be.include("ZRH");
	});

	it("should display LON Airport be selected in leg two's destination aiport", async function() {
		expect(await flightsResultPage.getDestinationAirportOfLegTwo()).to.be.include("LON");
	});

	it("Should display business cabin be selected in leg one's cabins", async function() {
		expect(await flightsResultPage.getSelectedCabinOfLegOne()).to.be.equal("Business");
	});

	it("Should display business cabin be selected in leg two's cabins", async function() {
		expect(await flightsResultPage.getSelectedCabinOfLegTwo()).to.be.equal("Business");
	});

	it("Should display selected dates in leg one", async function() {
		expect(await flightsResultPage.getSelectedDateOfLegOne()).to.be.equal(await helper.getKayakFormatedDate(6));
	});

	it("Should display selected dates in leg two", async function() {
		expect(await flightsResultPage.getSelectedDateOfLegTwo()).to.be.equal(await helper.getKayakFormatedDate(12));
	});

	it("Should display default number of travelers be selected", async function() {
		expect(await flightsResultPage.defaultTravelersSelected()).to.be.true;
	});

	it("Should display two take-off sliders in times filter", async function() {
		expect(await flightsResultPage.twoTakeOffSlidersDisplayed()).to.be.true;
	});
	
	it("Should display 'take-off from FRA slider' in times Filter", async function() {
		expect(await flightsResultPage.getFirstSliderLabel()).to.be.equal("Take-off from FRA");
	});

	it("Should display 'take-off from ZRH slider' in Times Filter", async function() {
		expect(await flightsResultPage.getSecondSliderLabel()).to.be.equal("Take-off from ZRH");
	});

	it("Should display 2 landing sliders after click on landing tab", async function() {
		await flightsResultPage.clickLandingTabInTimesFilter();
		expect(await flightsResultPage.twoLandingSlidersDisplayed()).to.be.true;
	});

	it("Should 'change take-off from ZRH' slider", async function() {
		await flightsResultPage.changeTimeSliderForZRH();
		expect(flightsResultPage.timeSliderForZRHChanged()).to.be.true;
	});

	it("Should display results with selected time for second leg times", async function() {
		expect(flightsResultPage.resultsContainNewTimeRangeForSecondLeg()).to.be.true;
	});

	it("Should click View Deal Button takes to providers page", async function() {
		await flightsResultPage.clickViewDealButton();
		await providerPage.switchTab();
		expect(await providerPage.originAirportDisplayed()).to.be.true;
	});
});

describe("Provider Page:", function() {

	it("Should display FRA Airport be selected in origin airport", async function() {
		expect(await providerPage.getoriginAirport()).to.be.include("FRA");
	});

	it("Should display ZRH Airport selected in destination airport", async function() {
		expect(await providerPage.getDestinationAirport()).to.be.include("ZRH");
	});

	it("Should display selected Dates in Date Field", async function() {
		expect(await providerPage.getDepartureDate()).to.be.equal(helper.getSwissFormatedDate(6));
	});

	it("Should go back to flights result page", async function() {
		await flightsResultPage.switchTab();
		expect(await flightsResultPage.airportTimesFilterDisplayed()).to.be.true;
	});
});

describe("Flight Results Page:", function() {

	it("Should open multiple cities form when click on search form", async function() {
		await flightsResultPage.clickSearchForm();
		expect(await flightsResultPage.multipleCitiesFormDisplayed()).to.be.true;
	});

	it("Should retained FRA Airport be selected in leg one's origin airport", async function() {
		expect(await flightsResultPage.getOriginAirportOfLegOne()).to.be.include("FRA");
	});

	it("Should retained ZRH Airport be selected in leg one's destination airport", async function() {
		expect(await flightsResultPage.getDestinationAirportOfLegOne()).to.be.include("ZRH");
	});

	it("Should retained ZRH Airport be selected in leg two's origin airport", async function() {
		expect(await flightsResultPage.getDestinationAirportOfLegOne()).to.be.include("ZRH");
	});

	it("Should retained LON Airport be selected in leg two's destination airport", async function() {
		expect(await flightsResultPage.getDestinationAirportOfLegTwo()).to.be.include("LON");
	});

	it("Should retained business cabin be selected for leg's one", async function() {
		expect(await flightsResultPage.getSelectedCabinOfLegOne()).to.be.equal("Business");
	});

	it("Should retained business cabin be selected for leg two", async function() {
		expect(await flightsResultPage.getSelectedCabinOfLegTwo()).to.be.equal("Business");
	});

	it("Should retained selected dates for leg one", async function() {
		expect(await flightsResultPage.getSelectedDateOfLegOne()).to.be.equal(await helper.getKayakFormatedDate(6));
	});

	it("Should retained selected dates for leg two", async function() {
		expect(await flightsResultPage.getSelectedCabinOfLegTwo()).to.be.equal(await helper.getKayakFormatedDate(12));
	});

	it("Should retained default number of travelers", async function() {
		expect(await flightsResultPage.defaultTravelersSelected()).to.be.true;
	});

	it("should be able to click on clear all button", async function() {
		await flightsResultPage.clickClearAllButton();
		expect(await flightsResultPage.clearLegOneOriginAirport()).to.be.true;
	});

	it("should clear origin Airport for leg one", async function() {
		expect(await flightsResultPage.clearLegOneOriginAirport()).to.be.true;
	});

	it("should clear origin Airport for leg two", async function() {
		expect(await flightsResultPage.clearLegTwoOriginAirport()).to.be.true;
	});

	it("should clear destination Airport for leg one", async function() {
		expect(await flightsResultPage.clearLegOneDestinationAirport()).to.be.true;
	});

	it("should clear destination Airport for leg two", async function() {
		expect(await flightsResultPage.clearLegTwoDestinationAirport()).to.be.true;
	});

	it("should clear departure date for leg one", async function() {
		expect(await flightsResultPage.clearLegOneDepartureDate()).to.be.true;
	});

	it("should clear departure date for leg one", async function() {
		expect(await flightsResultPage.clearLegTwoDepartureDate()).to.be.true;
	});

	it("should not clear cabin class for leg one", async function() {
		expect(await flightsResultPage.notClearLegOneCabinClass()).to.be.false;
	});

	it("should not clear cabin class for leg two", async function() {
		expect(await flightsResultPage.notClearLegTwoCabinClass()).to.be.false;
	});

	it("should not clear number of travelers", async function() {
		expect(await flightsResultPage.notClearSelectedTravelers()).to.be.true;
	});

	it("should click search button", async function() {
		await flightsResultPage.clickSearchButton();
		expect(await flightsResultPage.errorDialogBoxDisplayed()).to.be.true;
	});

	it("should display error message with 'Please enter a 'From' airport for flight '1'.'", async function() {
		expect(await flightsResultPage.getFirstErrorMessage()).to.be.equal("Please enter a 'From' airport for flight '1'.");
	});

	it("should display error message with 'Please enter a 'Please enter a 'To' airport for flight '1'.'", async function() {
		expect(await flightsResultPage.getSecondErrorMessage()).to.be.equal("Please enter a 'To' airport for flight '1'.");
	});

	it("should display error message with 'Please enter a valid 'Depart' date for flight '1'.'", async function() {
		expect(await flightsResultPage.getThirdErrorMessage()).to.be.equal("Please enter a valid 'Depart' date for flight '1'.");
	});

	it("should close messages when click 'ok'", async function() {
		await flightsResultPage.clickErrorDialogOkButton();
		expect(await flightsResultPage.closeErrorDialogBox()).to.be.true;
	});
});