import { browser, element, by, promise} from 'protractor';
import { HomePageObject } from './homePageObject';
import { FlightsPageObject } from './flightsPageObject';
import { SearchFormObject } from './searchFormObject';
import { userInputJSON } from './userInputJSON';
import { async } from 'q';

var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
var should = chai.should();
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
    await homePageObject.getDepartureValue().should.eventually.be.equal("Paris (PAR)");
  });

  it("Change number of ‘adults’ from travelers field to 9",async function() {
    homePageObject.addAdultPassengers(10);
    await homePageObject.getAdultsLimitMessage().should.eventually.be.equal("Searches cannot have more than 9 adults");
  });
});

for (let senario in userInputJSON){
  describe("Verify complete flow to search flights", async function() {
    before(async function() {
      browser.waitForAngularEnabled(false);
      await browser.get('https://www.kayak.com');
      await browser.manage().deleteAllCookies();
      await browser.refresh();
    });
  
    it("Should display origin input which is entered", async function() {
      homePageObject.setDeparture(userInputJSON[senario]["Origin Input"]);
      await homePageObject.getDepartureValue().should.eventually.be.equal(userInputJSON[senario]["Origin Selection"]);
    });
  
    it("Should display destination which is entered", async function() {
      homePageObject.setDestination(userInputJSON[senario]["Destination Input"]);
      await homePageObject.getDestinationValue().should.eventually.be.equal(userInputJSON[senario]["Destination Selection"]);
    });
  
    it("Change number of ‘adults’ from travelers field to user entered",async function() {
      homePageObject.addAdultPassengers(userInputJSON[senario]["Passengers"]["Adults"]);
      await homePageObject.getAdultPassengers().should.eventually.be.equal((userInputJSON[senario]["Passengers"]["Adults"]).toString());
    });

    it("Change number of ‘children’ from travelers field to user entered",async function() {
      homePageObject.addChildPassengers(userInputJSON[senario]["Passengers"]["Child"]);
      await homePageObject.getChildPassenger().should.eventually.be.equal((userInputJSON[senario]["Passengers"]["Child"]).toString());
    });
  
    it("Should display accurate date in departure field",async function() {
      homePageObject.fillDatesDeparture();
      await homePageObject.getDepartureDate().getText().should.eventually.be.equal(homePageObject.getTripDates(3));
    });
  
    it("Should display accurate date in return date field",async function() {
      homePageObject.fillDatesReturn();
      await homePageObject.getReturnDate().should.eventually.be.equal(homePageObject.getTripDates(6));
    });
  
    it("Should display all unchecked checkboxes in compare-to block",async function() {
      await homePageObject.uncheckAllCheckBox();
    });
  
    it("Should display same inputs in search form which user entered", function() {
      homePageObject.searchButton.click();
      homePageObject.getDepartureValue().should.eventually.be.equal(userInputJSON[senario]["Origin Selection"]);
      homePageObject.getDestinationValue().should.eventually.be.equal(userInputJSON[senario]["Destination Selection"]);
      homePageObject.getAdultPassengers().should.eventually.be.equal((userInputJSON[senario]["Passengers"]["Adults"]).toString());
      homePageObject.getDepartureDate().getText().should.eventually.be.equal(homePageObject.getTripDates(3));
      homePageObject.getReturnDate().should.eventually.be.equal(homePageObject.getTripDates(6));
    });
  
    it("Should display least price in ‘Cheapest’ sort option compared to ‘Best’ and ‘Quickest’ sort options", function() {
      const cheapPrice =  flightsPageObject.getCheapestPrice();
      const bestPrice =  flightsPageObject.getBestPrice();
      const quickPrice =  flightsPageObject.getQuickestPrice();
      expect(cheapPrice).to.be.at.most(bestPrice, "Cheapest Price is less than best price");
      expect(cheapPrice).to.be.at.most(quickPrice, "Cheapest Price is less than Quickest price");
    });
  
    it("Should display least time in ‘Quickest’ sort option compared to ‘Cheapest’ and ‘Best’ sort options", function() { 
      const cheapTime = flightsPageObject.getCheapestTime();
      const bestTime = flightsPageObject.getBestTime();
      const quickTime = flightsPageObject.getQuickestTime();
      expect(quickTime).to.be.at.most(bestTime, "Quickest Time is less than best Time");
      expect(quickTime).to.be.at.most(cheapTime, "Quickest Time is less than Quickest Time");
    });
  });
}
