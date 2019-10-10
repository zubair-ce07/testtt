"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const protractor_1 = require("protractor");
const homePageObject_1 = require("./homePageObject");
var chai = require('chai');
var chaiAsPromised = require('chai-as-promised');
chai.use(chaiAsPromised);
var expect = chai.expect;
var should = chai.should();
let homePageObject = new homePageObject_1.HomePageObject();
describe("kayak Automation", function () {
    return __awaiter(this, void 0, void 0, function* () {
        before(function () {
            return __awaiter(this, void 0, void 0, function* () {
                protractor_1.browser.waitForAngularEnabled(false);
                yield protractor_1.browser.get(homePageObject.url);
                yield homePageObject.clearCookies();
            });
        });
        it("should display the 'Travel Inspiration' section", function () {
            homePageObject.travelSection().isDisplayed().should.eventually.be.true;
        });
        it("should display the 'Trending Cities' section", function () {
            homePageObject.citiesSection().isDisplayed().should.eventually.be.true;
        });
        it("should display the 'Trending Countries' section", function () {
            homePageObject.countriesSection().isDisplayed().should.eventually.be.true;
        });
        it("Should display at least 2 tiles under 'Travel Inspiration' ", function () {
            homePageObject.getTilesInTravelInspiration().should.eventually.be.true;
        });
        it("Should display at least 20 tiles under 'Trending Cities' ", function () {
            homePageObject.getTrendingCityTiles().should.eventually.be.true;
        });
        it("Should display at least 20 tiles under 'Trending Countries' ", function () {
            homePageObject.getTrendingCountriesTiles().should.eventually.be.true;
        });
        it("Should display image in first tile under 'Travel Inspiration'", function () {
            homePageObject.getTravelInspirationFirstImage().should.eventually.be.true;
        });
        it("Should display image in first tile under 'Trending Cities'", function () {
            homePageObject.citiesFirstImage.isDisplayed().should.eventually.be.true;
        });
        it("Should display image in first tile under 'Trending Countries'", function () {
            homePageObject.countriesFirstImage.isDisplayed().should.eventually.be.true;
        });
        it("Should be able to click the first tile under 'Travel Inspiration' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.clickFirstTravelInspirationTile().should.eventually.true;
            });
        });
        it("Should be able to click 'More Inspiration' button  under 'Travel Inspiration' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                homePageObject.navigateToHomePage();
                yield homePageObject.clickMoreInspirationButton().should.eventually.be.true;
            });
        });
        it("Should be able to click the 1st tile under 'Trending Cities' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                homePageObject.navigateToHomePage();
                yield homePageObject.clickFirstCityTile().should.eventually.be.true;
            });
        });
        it("Should be able to click the 1st tile under 'Trending Countries' section", function () {
            homePageObject.navigateToHomePage();
            homePageObject.clickFirstCountryTile().should.eventually.be.true;
        });
    });
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGVzdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3Rlc3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7QUFBQSwyQ0FBMEQ7QUFDMUQscURBQWtEO0FBR2xELElBQUksSUFBSSxHQUFHLE9BQU8sQ0FBQyxNQUFNLENBQUMsQ0FBQztBQUMzQixJQUFJLGNBQWMsR0FBRyxPQUFPLENBQUMsa0JBQWtCLENBQUMsQ0FBQztBQUNqRCxJQUFJLENBQUMsR0FBRyxDQUFDLGNBQWMsQ0FBQyxDQUFDO0FBQ3pCLElBQUksTUFBTSxHQUFHLElBQUksQ0FBQyxNQUFNLENBQUM7QUFDekIsSUFBSSxNQUFNLEdBQUcsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO0FBRTNCLElBQUksY0FBYyxHQUFtQixJQUFJLCtCQUFjLEVBQUUsQ0FBQztBQUUxRCxRQUFRLENBQUMsa0JBQWtCLEVBQUU7O1FBQzNCLE1BQU0sQ0FBQzs7Z0JBQ0wsb0JBQU8sQ0FBQyxxQkFBcUIsQ0FBQyxLQUFLLENBQUMsQ0FBQztnQkFDckMsTUFBTSxvQkFBTyxDQUFDLEdBQUcsQ0FBQyxjQUFjLENBQUMsR0FBRyxDQUFDLENBQUM7Z0JBQ3RDLE1BQU0sY0FBYyxDQUFDLFlBQVksRUFBRSxDQUFDO1lBQ3RDLENBQUM7U0FBQSxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsaURBQWlELEVBQUU7WUFDcEQsY0FBYyxDQUFDLGFBQWEsRUFBRSxDQUFDLFdBQVcsRUFBRSxDQUFDLE1BQU0sQ0FBQyxVQUFVLENBQUMsRUFBRSxDQUFDLElBQUksQ0FBQztRQUN6RSxDQUFDLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyw4Q0FBOEMsRUFBRTtZQUNqRCxjQUFjLENBQUMsYUFBYSxFQUFFLENBQUMsV0FBVyxFQUFFLENBQUMsTUFBTSxDQUFDLFVBQVUsQ0FBQyxFQUFFLENBQUMsSUFBSSxDQUFDO1FBQ3pFLENBQUMsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLGlEQUFpRCxFQUFFO1lBQ3BELGNBQWMsQ0FBQyxnQkFBZ0IsRUFBRSxDQUFDLFdBQVcsRUFBRSxDQUFDLE1BQU0sQ0FBQyxVQUFVLENBQUMsRUFBRSxDQUFDLElBQUksQ0FBQztRQUM1RSxDQUFDLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyw2REFBNkQsRUFBRTtZQUNoRSxjQUFjLENBQUMsMkJBQTJCLEVBQUUsQ0FBQyxNQUFNLENBQUMsVUFBVSxDQUFDLEVBQUUsQ0FBQyxJQUFJLENBQUM7UUFDekUsQ0FBQyxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsMkRBQTJELEVBQUU7WUFDOUQsY0FBYyxDQUFDLG9CQUFvQixFQUFFLENBQUMsTUFBTSxDQUFDLFVBQVUsQ0FBQyxFQUFFLENBQUMsSUFBSSxDQUFDO1FBQ2xFLENBQUMsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLDhEQUE4RCxFQUFFO1lBQ2pFLGNBQWMsQ0FBQyx5QkFBeUIsRUFBRSxDQUFDLE1BQU0sQ0FBQyxVQUFVLENBQUMsRUFBRSxDQUFDLElBQUksQ0FBQztRQUN2RSxDQUFDLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQywrREFBK0QsRUFBRTtZQUNsRSxjQUFjLENBQUMsOEJBQThCLEVBQUUsQ0FBQyxNQUFNLENBQUMsVUFBVSxDQUFDLEVBQUUsQ0FBQyxJQUFJLENBQUM7UUFDNUUsQ0FBQyxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsNERBQTRELEVBQUU7WUFDL0QsY0FBYyxDQUFDLGdCQUFnQixDQUFDLFdBQVcsRUFBRSxDQUFDLE1BQU0sQ0FBQyxVQUFVLENBQUMsRUFBRSxDQUFDLElBQUksQ0FBQztRQUMxRSxDQUFDLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQywrREFBK0QsRUFBRTtZQUNsRSxjQUFjLENBQUMsbUJBQW1CLENBQUMsV0FBVyxFQUFFLENBQUMsTUFBTSxDQUFDLFVBQVUsQ0FBQyxFQUFFLENBQUMsSUFBSSxDQUFDO1FBQzdFLENBQUMsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLDJFQUEyRSxFQUFFOztnQkFDOUUsTUFBTSxjQUFjLENBQUMsK0JBQStCLEVBQUUsQ0FBQyxNQUFNLENBQUMsVUFBVSxDQUFDLElBQUksQ0FBQztZQUNoRixDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLHVGQUF1RixFQUFFOztnQkFDMUYsY0FBYyxDQUFDLGtCQUFrQixFQUFFLENBQUM7Z0JBQ3BDLE1BQU0sY0FBYyxDQUFDLDBCQUEwQixFQUFFLENBQUMsTUFBTSxDQUFDLFVBQVUsQ0FBQyxFQUFFLENBQUMsSUFBSSxDQUFDO1lBQzlFLENBQUM7U0FBQSxDQUFDLENBQUM7UUFFSCxFQUFFLENBQUMsc0VBQXNFLEVBQUU7O2dCQUN6RSxjQUFjLENBQUMsa0JBQWtCLEVBQUUsQ0FBQztnQkFDcEMsTUFBTSxjQUFjLENBQUMsa0JBQWtCLEVBQUUsQ0FBQyxNQUFNLENBQUMsVUFBVSxDQUFDLEVBQUUsQ0FBQyxJQUFJLENBQUM7WUFDdEUsQ0FBQztTQUFBLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyx5RUFBeUUsRUFBRTtZQUM1RSxjQUFjLENBQUMsa0JBQWtCLEVBQUUsQ0FBQztZQUNwQyxjQUFjLENBQUMscUJBQXFCLEVBQUUsQ0FBQyxNQUFNLENBQUMsVUFBVSxDQUFDLEVBQUUsQ0FBQyxJQUFJLENBQUM7UUFDbkUsQ0FBQyxDQUFDLENBQUM7SUFDTCxDQUFDO0NBQUEsQ0FBQyxDQUFDIn0=