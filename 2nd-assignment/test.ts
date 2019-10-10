import { browser, element, by, promise} from 'protractor';
import { HomePageObject } from './homePageObject';
import { async } from 'q';

var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
var should = chai.should();

let homePageObject: HomePageObject = new HomePageObject();

describe("kayak Automation", async function() {
  before(async function() {
    browser.waitForAngularEnabled(false);
    await browser.get(homePageObject.url);
    await homePageObject.clearCookies();
  });

  it("should display the 'Travel Inspiration' section", function() {
    homePageObject.travelSection().isDisplayed().should.eventually.be.equal(true);
  });

  it("should display the 'Trending Cities' section", function() {
    homePageObject.citiesSection().isDisplayed().should.eventually.be.equal(true);
  });

  it("should display the 'Trending Countries' section", function() {
    homePageObject.countriesSection().isDisplayed().should.eventually.equal(true);
  });

  it("Should display at least 2 tiles under 'Travel Inspiration' ", function() {
    homePageObject.getTilesInTravelInspiration().should.eventually.be.equal(true);
  });

  it("Should display at least 20 tiles under 'Trending Cities' ", function() {
    homePageObject.getTrendingCityTiles().should.eventually.be.equal(true);
  });

  it("Should display at least 20 tiles under 'Trending Countries' ", function() {
    homePageObject.getTrendingCountriesTiles().should.eventually.be.equal(true);
  });

  it("Should display image in first tile under 'Travel Inspiration'", function() {
    homePageObject.getTravelInspirationFirstImage().should.eventually.be.equal(true);
  });

  it("Should display image in first tile under 'Trending Cities'", function() {
    homePageObject.citiesFirstImage.isDisplayed().should.eventually.be.equal(true);
  });

  it("Should display image in first tile under 'Trending Countries'", function() {
    homePageObject.countriesFirstImage.isDisplayed().should.eventually.be.equal(true);
  });

  it("Should be able to click the first tile under 'Travel Inspiration' section", async function() {
    await homePageObject.clickFirstTravelInspirationTile().should.eventually.equal(true);
  });

  it("Should be able to click 'More Inspiration' button  under 'Travel Inspiration' section", async function() {
    homePageObject.navigateToHomePage();
    await homePageObject.clickMoreInspirationButton().should.eventually.equal(true);
  });

  it("Should be able to click the 1st tile under 'Trending Cities' section", async function() {
    homePageObject.navigateToHomePage();
    await homePageObject.clickFirstCityTile().should.eventually.equal(true);
  });

  it("Should be able to click the 1st tile under 'Trending Countries' section", function() {
    homePageObject.navigateToHomePage();
    homePageObject.clickFirstCountryTile().should.eventually.equal(true);
  });
});
