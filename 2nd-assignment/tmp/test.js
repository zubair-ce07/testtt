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
            protractor_1.browser.waitForAngularEnabled(false);
            protractor_1.browser.get(homePageObject.url);
            homePageObject.clearCookies();
        });
        it("Should display the title of momondo", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.title.getText().should.eventually.be.equal("Buche günstige Flüge mit dem momondo-Flugvergleich");
            });
        });
        it("should display the 'Travel Inspiration' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.displayTravelInspirationSection().should.eventually.be.equal(true);
            });
        });
        it("should display the 'Trending Cities' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.displayTrendingCitiesSection().should.eventually.be.equal(true);
            });
        });
        it("should display the 'Trending Countries' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.displayTrendingCountriesSection().should.eventually.be.equal(true);
            });
        });
        it("Should display at least 2 tiles under 'Travel Inspiration' ", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.getTilesInTravelInspiration().should.eventually.be.equal(true);
            });
        });
        it("Should display at least 20 tiles under 'Trending Cities' ", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.getTrendingCityTiles().should.eventually.be.equal(true);
            });
        });
        it("Should display at least 20 tiles under 'Trending Countries' ", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.getTrendingCountriesTiles().should.eventually.be.equal(true);
            });
        });
        it("Should display image in first tile under 'Travel Inspiration'", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.getTravelInspirationFirstImage().should.eventually.be.equal(true);
            });
        });
        it("Should display image in first tile under 'Trending Cities'", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.citiesFirstImage.isDisplayed().should.eventually.be.equal(true);
            });
        });
        it("Should display image in first tile under 'Trending Countries'", function () {
            return __awaiter(this, void 0, void 0, function* () {
                yield homePageObject.countriesFirstImage.isDisplayed().should.eventually.be.equal(true);
            });
        });
        it("Should be able to click the first tile under 'Travel Inspiration' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                ((yield homePageObject.clickFirstTravelInspirationTile()).toString()).should.includes('nachhaltigere-fluege-finden');
            });
        });
        it("Should be able to click 'More Inspiration' button  under 'Travel Inspiration' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                ((yield homePageObject.clickMoreInspirationButton()).toString()).should.includes('entdecken');
            });
        });
        it("Should be able to click the 1st tile under 'Trending Cities' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                ((yield homePageObject.clickFirstCityTile()).toString()).should.includes('palma-de-mallorca');
            });
        });
        it("Should be able to click the 1st tile under 'Trending Countries' section", function () {
            return __awaiter(this, void 0, void 0, function* () {
                ((yield homePageObject.clickFirstCountryTile()).toString()).should.includes('usa');
            });
        });
    });
});
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGVzdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3Rlc3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7QUFBQSwyQ0FBMEQ7QUFDMUQscURBQWtEO0FBRWxELElBQUksSUFBSSxHQUFHLE9BQU8sQ0FBQyxNQUFNLENBQUMsQ0FBQztBQUMzQixJQUFJLGNBQWMsR0FBRyxPQUFPLENBQUMsa0JBQWtCLENBQUMsQ0FBQztBQUNqRCxJQUFJLENBQUMsR0FBRyxDQUFDLGNBQWMsQ0FBQyxDQUFDO0FBQ3pCLElBQUksTUFBTSxHQUFHLElBQUksQ0FBQyxNQUFNLENBQUM7QUFDekIsSUFBSSxNQUFNLEdBQUcsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO0FBRTNCLElBQUksY0FBYyxHQUFtQixJQUFJLCtCQUFjLEVBQUUsQ0FBQztBQUUxRCxRQUFRLENBQUMsa0JBQWtCLEVBQUU7O1FBQzNCLE1BQU0sQ0FBQztZQUNMLG9CQUFPLENBQUMscUJBQXFCLENBQUMsS0FBSyxDQUFDLENBQUM7WUFDckMsb0JBQU8sQ0FBQyxHQUFHLENBQUMsY0FBYyxDQUFDLEdBQUcsQ0FBQyxDQUFDO1lBQ2hDLGNBQWMsQ0FBQyxZQUFZLEVBQUUsQ0FBQztRQUNoQyxDQUFDLENBQUMsQ0FBQztRQUVILEVBQUUsQ0FBQyxxQ0FBcUMsRUFBRTs7Z0JBQ3hDLE1BQU0sY0FBYyxDQUFDLEtBQUssQ0FBQyxPQUFPLEVBQUUsQ0FBQyxNQUFNLENBQUMsVUFBVSxDQUFDLEVBQUUsQ0FBQyxLQUFLLENBQUMsb0RBQW9ELENBQUMsQ0FBQztZQUN4SCxDQUFDO1NBQUEsQ0FBQyxDQUFDO1FBRUgsRUFBRSxDQUFDLGlEQUFpRCxFQUFFOztnQkFDcEQsTUFBTSxjQUFjLENBQUMsK0JBQStCLEVBQUUsQ0FBQyxNQUFNLENBQUMsVUFBVSxDQUFDLEVBQUUsQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7WUFDMUYsQ0FBQztTQUFBLENBQUMsQ0FBQztRQUVILEVB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