import { browser, element, by, promise} from 'protractor';
import { HomePageObject } from './homePageObject';
import { FlightsPageObject } from './flightsPageObject';
import { SearchFormObject } from './searchFormObject';
import { userInputJSON } from './userInputJSON';
import { async } from 'q';
import http = require('http');
var Intercept = require('protractor-intercept');

var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
var should = chai.should();
var intercept = new Intercept(browser);
let homePageObject: HomePageObject = new HomePageObject();
let flightsPageObject: FlightsPageObject = new FlightsPageObject();
let searchFormObject: SearchFormObject = new SearchFormObject();

describe("Search form and travelers Verification", async function() {
  before(async function() {
    browser.waitForAngularEnabled(false);
    await browser.get('https://www.kayak.com');
  });

  it('Changing trip types should change search inputs accordingly',async function() {
    homePageObject.changeToOneWayTrip();
    await homePageObject.returnDateText.isDisplayed().should.eventually.be.false;

    homePageObject.changeToMulticityTrip();
    await homePageObject.multiCitiesOptions.isDisplayed().should.eventually.be.true;

    homePageObject.changeToRoundTrip();
    await homePageObject.returnDateText.isDisplayed().should.eventually.be.true;
  });
  
  it("Should display correct city in origin field",async function() {
    homePageObject.setDeparture("Paris (PAR)");
    await searchFormObject.getDepartureValue().should.eventually.be.equal("Paris (PAR)");
  });

  it("Should display adult passengers limit after selecting more then 9 adults",async function() {
    homePageObject.addAdultPassengers(10);
    await homePageObject.getAdultsLimitMessage().should.eventually.be.equal("Searches cannot have more than 9 adults");
  });
});

Object.keys(userInputJSON).map( senario => {
  describe("Verify flights search process:", async function() {
    before(async function() {
      browser.waitForAngularEnabled(false);
      await browser.get('https://www.kayak.com');
      await browser.manage().deleteAllCookies();
      await browser.refresh();
    });

    it(`Should display ${userInputJSON[senario]["Origin Input"]} in departure field`, async function() {
      await homePageObject.setDeparture(userInputJSON[senario]["Origin Input"]);
      await searchFormObject.getDepartureValue().should.eventually.be.equal(userInputJSON[senario]["Origin Selection"]);
    });
  
    it(`Should display ${userInputJSON[senario]["Destination Input"]} in destination field`,async function() {
      homePageObject.setDestination(userInputJSON[senario]["Destination Input"]);
      await searchFormObject.getDestinationValue().should.eventually.be.equal(userInputJSON[senario]["Destination Selection"]);
    });
  
    it(`Change number of ‘adults’ from travelers field to ${userInputJSON[senario]["Passengers"]["Adults"]}`,async function() {
      homePageObject.addAdultPassengers(userInputJSON[senario]["Passengers"]["Adults"]);
      await searchFormObject.getAdultPassengers().should.eventually.be.equal((userInputJSON[senario]["Passengers"]["Adults"]).toString());
    });

    it(`Change number of ‘children’ from travelers field to ${userInputJSON[senario]["Passengers"]["Child"]}`,async function() {
       homePageObject.addChildPassengers(userInputJSON[senario]["Passengers"]["Child"]);
      await homePageObject.getChildPassenger().should.eventually.be.equal((userInputJSON[senario]["Passengers"]["Child"]).toString());
    });
  
    it("Should display 3rd Day after today as trip start date",async function() {
      homePageObject.fillDatesDeparture();
      await searchFormObject.getDepartureDate().getText().should.eventually.be.equal(await homePageObject.getTripDates(3));
    });
  
    it("Should display 6th Day after today as trip start date",async function() {
      homePageObject.fillDatesReturn();
      await searchFormObject.getReturnDate().getText().should.eventually.be.equal(await homePageObject.getTripDates(6));
    });
  
    it("Should uncheck all checkboxes in compare-to block",async function() {
      await homePageObject.uncheckAllCheckBox();
    });
  
    it("Should display same inputs in search form after trip search",async function() {
      homePageObject.searchButton.click();
    });
  
    it("Should display ‘Cheapest’ sort option in least price as compared to ‘Best’ and ‘Quickest’ sort options", function() {
      const cheapPrice =  flightsPageObject.getCheapestPrice();
      const bestPrice =  flightsPageObject.getBestPrice();
      const quickPrice =  flightsPageObject.getQuickestPrice();
      expect(cheapPrice).to.be.at.most(bestPrice, "Cheapest Price is less than best price");
      expect(cheapPrice).to.be.at.most(quickPrice, "Cheapest Price is less than Quickest price");
    });
  
    it("Should display ‘Quickest’ sort option in least time as compared to ‘Cheapest’ and ‘Best’ sort options", function() { 
      const cheapTime = flightsPageObject.getCheapestTime();
      const bestTime = flightsPageObject.getBestTime();
      const quickTime = flightsPageObject.getQuickestTime();
      expect(quickTime).to.be.at.most(bestTime, "Quickest Time is less than best Time");
      expect(quickTime).to.be.at.most(cheapTime, "Quickest Time is less than Quickest Time");
    });
  });
})