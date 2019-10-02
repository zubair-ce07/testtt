import { browser, element, by, promise} from 'protractor';
import { HomePageObject } from './homePageObject';
import { FlightsPageObject } from './flightsPageObject';

var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
let homePageObject: HomePageObject = new HomePageObject();
let flightsPageObject: FlightsPageObject = new FlightsPageObject();

describe("kayak Automation", function() {
  before(function() {
    browser.waitForAngularEnabled(false);
    browser.get('https://www.kayak.com');
  });

  it("Select flights from top", function() {
    expect(homePageObject.clickFlights()); 
  });

  it("Should display the origin field", function() {
    expect(homePageObject.getOrigin()).to.eventually.be.true; 
  });

  it("Should display the destination field", function() {
    expect(homePageObject.getDestination()).to.eventually.be.true; 
  });

  it("Should display the departure date field", function() {
    expect(homePageObject.departureField()).to.eventually.be.true; 
  });

  it("Should display the return date field", function() {
    expect(homePageObject.returnField()).to.eventually.be.true; 
  });

  it("Should display ‘Round-trip’ in trip type field", function() {
    expect(homePageObject.roundTripTypeField()).to.eventually.be.equal('true');
  });

  it("Switch to ‘One-way’ trip type mode", function() {
    homePageObject.clickSwitch();
    homePageObject.clickOneWay();
    expect(homePageObject.departureField()).to.eventually.be.true;
  });
  
  it("Switch to ‘Multi-city’ trip type mode", function() {
    homePageObject.clickSwitch();
    homePageObject.clickMultiCity();
    expect(homePageObject.multiCities()).to.eventually.be.true;
  });

  it("Switch to ‘Round-trip’ trip type mode", function() {
    homePageObject.clickSwitch();
    homePageObject.clickRoundTrip();
    expect(homePageObject.returnField()).to.eventually.be.true;
  });

  it("Change number of ‘adults’ from travelers field to 9", function() {
    homePageObject.clickTravelersGrid();
    homePageObject.addAdultPassengers(10);
    expect(homePageObject.getAdultsLimitMessage()).to.eventually.be.equal("Searches cannot have more than 9 adults");
  });

  it("Should display ‘Paris (PAR)’ in origin field", function() {
    homePageObject.clickSwitch();
    homePageObject.clickRoundTrip();
    homePageObject.clickOriginField();
    homePageObject.fillOrigin("PAR");
    homePageObject.selectOrigin();
    expect(homePageObject.getOriginValue()).to.eventually.be.include("Paris (PAR)");
  });

  it("Should display ‘New York (NYC)’ in the destination field", function() {
    homePageObject.clickDestinationField();
    homePageObject.fillDestination("NYC");
    homePageObject.selectDestination();
    expect(homePageObject.getDestinationValue()).to.eventually.be.include("New York (NYC)");
  });

  it("Should display ‘4 Travelers’ in the travelers field", function() {
    homePageObject.clickPassengersDropdown();
    homePageObject.decreaseAdultPassengers(6);
    expect(homePageObject.getAdultPassenger()).to.eventually.be.equal('4');
  });

  it("Should display ‘6 Travelers’ in the travelers field", function() {
    homePageObject.addChildPassengers(2);
    expect(homePageObject.getChildPassenger()).to.eventually.be.equal('2');
  });

  it("Should display accurate date in departure field", function() {
    homePageObject.clickDepartureField();
    homePageObject.fillDatesDeparture();
    expect(homePageObject.getDepartureDate()).to.eventually.equal(homePageObject.getTripDates(3));
  });

  it("Should display accurate date in return date field", function() {
    homePageObject.fillDatesReturn();
    expect(homePageObject.getReturnDate()).to.eventually.equal(homePageObject.getTripDates(6));
  });

  it("Should display all unchecked checkboxes in compare-to block", function() {
    homePageObject.clickSwitch();
    homePageObject.clickRoundTrip();
    expect(homePageObject.uncheckAllCheckBox());
  });

  it("Should display correct filled-in search form on results page", function() {
    homePageObject.clickSearch();
    homePageObject.switchTabs();
    browser.sleep(5000);

    expect(flightsPageObject.getDeparture()).to.eventually.equal("Paris (PAR)");
    expect(flightsPageObject.getDestination()).to.eventually.equal("New York (NYC)");
    expect(flightsPageObject.getDepartureDate()).to.eventually.equal(flightsPageObject.getTripDates(3));
    expect(flightsPageObject.getReturnDate()).to.eventually.equal(flightsPageObject.getTripDates(6));
  });

  it("Should display least price in ‘Cheapest’ sort option compared to ‘Best’ and ‘Quickest’ sort options", async function() {
    const cheapPrice = await flightsPageObject.getCheapestPrice();
    const bestPrice =  await flightsPageObject.getBestPrice();
    const quickPrice = await flightsPageObject.getQuickestPrice();

    expect(cheapPrice).to.be.at.most(bestPrice);
    expect(cheapPrice).to.be.at.most(quickPrice);
  });

  it("Should display least time in ‘Quickest’ sort option compared to ‘Cheapest’ and ‘Best’ sort options", async function() { 
    const cheapTime = await flightsPageObject.getCheapestTime();
    const bestTime = await flightsPageObject.getBestTime();
    const quickTime = await flightsPageObject.getQuickestTime();
    
    expect(quickTime).to.be.at.most(cheapTime);
    expect(quickTime).to.be.at.most(bestTime);
  });
});
