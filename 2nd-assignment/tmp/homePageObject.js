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
class HomePageObject {
    constructor() {
        this.url = 'https://www.momondo.de/';
        this.title = protractor_1.element(protractor_1.by.className("title-container"));
        this.travelInspirationSection = protractor_1.element(protractor_1.by.className("Common-Frontdoor-Brands-Momondo-Brandonly-TravelInspirationSection"));
        this.trendingCitiesSection = protractor_1.element.all(protractor_1.by.className("Common-Frontdoor-Brands-Momondo-Brandonly-DestinationsSection")).first();
        this.trendingCountriesSection = protractor_1.element.all(protractor_1.by.className("Common-Frontdoor-Brands-Momondo-Brandonly-DestinationsSection")).last();
        this.tilesInTravelInspiration = protractor_1.element.all(protractor_1.by.className("Common-Frontdoor-Brands-Momondo-Brandonly-ImageCardItem"));
        this.tilesInTrendingCities = protractor_1.element.all(protractor_1.by.className("Common-Seo-Brands-Momondo-CardGrid")).first().all(protractor_1.by.className("Common-Seo-Brands-Momondo-LinkCardWithImage"));
        this.tilesInTrendingCountries = protractor_1.element.all(protractor_1.by.className("Common-Seo-Brands-Momondo-CardGrid")).last().all(protractor_1.by.className("Common-Seo-Brands-Momondo-LinkCardWithImage"));
        this.travelFirstImage = this.tilesInTravelInspiration.first().all(protractor_1.by.tagName('img')).first();
        this.travelFirstImageUrl = this.tilesInTravelInspiration.first();
        this.citiesFirstImage = this.tilesInTrendingCities.first().element(protractor_1.by.tagName('a'));
        this.countriesFirstImage = this.tilesInTrendingCountries.first().element(protractor_1.by.tagName('a'));
        this.moreInspirationButton = this.travelInspirationSection.element(protractor_1.by.className("Common-Widgets-Button-StyleJamButton"));
        this.closePopupButton = protractor_1.element.all(protractor_1.by.className("Button-No-Standard-Style close")).last();
    }
    travelSection() {
        protractor_1.browser.actions().mouseMove(this.travelInspirationSection).perform();
        return this.travelInspirationSection.isDisplayed();
    }
    citiesSection() {
        protractor_1.browser.actions().mouseMove(this.trendingCitiesSection).perform();
        return this.trendingCitiesSection.isDisplayed();
    }
    countriesSection() {
        protractor_1.browser.actions().mouseMove(this.trendingCountriesSection).perform();
        return this.trendingCountriesSection.isDisplayed();
    }
    getTilesInTravelInspiration() {
        return __awaiter(this, void 0, void 0, function* () {
            const travelInspirationTiles = yield this.tilesInTravelInspiration.count();
            let tileLength;
            travelInspirationTiles >= 2 ? tileLength = true : tileLength = false;
            return tileLength;
        });
    }
    getTrendingCityTiles() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.actions().mouseMove(this.trendingCitiesSection).perform();
            const tilesInTrendingCities = yield this.tilesInTrendingCities.count();
            let cityTiles;
            tilesInTrendingCities >= 20 ? cityTiles = true : cityTiles = false;
            return cityTiles;
        });
    }
    getTrendingCountriesTiles() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.actions().mouseMove(this.trendingCountriesSection).perform();
            const tilesInTrendingCountries = yield this.tilesInTrendingCities.count();
            let countryTiles;
            tilesInTrendingCountries >= 20 ? countryTiles = true : countryTiles = false;
            return countryTiles;
        });
    }
    getTravelInspirationFirstImage() {
        return __awaiter(this, void 0, void 0, function* () {
            let travelFirstImage;
            const tagName = yield this.travelFirstImage.getTagName();
            tagName == "img" ? travelFirstImage = true : travelFirstImage = false;
            return travelFirstImage;
        });
    }
    clickFirstTravelInspirationTile() {
        return __awaiter(this, void 0, void 0, function* () {
            let firstTravelInspiration;
            let firstTravelImageUrl = yield this.travelFirstImageUrl.getAttribute('href');
            (this.tilesInTravelInspiration.first()).click();
            return (yield protractor_1.browser.getCurrentUrl()).includes(firstTravelImageUrl) ? firstTravelInspiration = true : firstTravelInspiration = false;
        });
    }
    clickFirstCityTile() {
        return __awaiter(this, void 0, void 0, function* () {
            let firstCity;
            protractor_1.browser.actions().mouseMove(this.tilesInTrendingCities.first()).perform();
            let firstImageUrl = yield this.citiesFirstImage.getAttribute('href');
            (this.tilesInTrendingCities.first()).click();
            return (yield protractor_1.browser.getCurrentUrl()).includes(firstImageUrl) ? firstCity = true : firstCity = false;
        });
    }
    clickFirstCountryTile() {
        return __awaiter(this, void 0, void 0, function* () {
            let firstCountry;
            protractor_1.browser.actions().mouseMove(this.tilesInTrendingCountries.first()).perform();
            let firstCountryUrl = yield this.countriesFirstImage.getAttribute('href');
            (this.tilesInTrendingCountries.first()).click();
            return (yield protractor_1.browser.getCurrentUrl()).includes(firstCountryUrl) ? firstCountry = true : firstCountry = false;
        });
    }
    clickMoreInspirationButton() {
        return __awaiter(this, void 0, void 0, function* () {
            let moreInspirationButton;
            protractor_1.browser.actions().mouseMove(this.moreInspirationButton).perform();
            let moreInspirationUrl = yield this.moreInspirationButton.getAttribute('href');
            this.moreInspirationButton.click();
            return (yield protractor_1.browser.getCurrentUrl()).includes(moreInspirationUrl) ? moreInspirationButton = true : moreInspirationButton = false;
        });
    }
    clearCookies() {
        return __awaiter(this, void 0, void 0, function* () {
            let until = yield protractor_1.protractor.ExpectedConditions;
            protractor_1.browser.wait(until.visibilityOf(this.closePopupButton), 4000, `${this.closePopupButton} not appeared in expected time`);
            this.closePopupButton.click();
        });
    }
    navigateToHomePage() {
        protractor_1.browser.get(this.url);
    }
}
exports.HomePageObject = HomePageObject;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaG9tZVBhZ2VPYmplY3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9ob21lUGFnZU9iamVjdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBLDJDQUEySTtBQUkzSSxNQUFhLGNBQWM7SUFBM0I7UUFDRSxRQUFHLEdBQVcseUJBQXlCLENBQUM7UUFDeEMsVUFBSyxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxTQUFTLENBQUMsaUJBQWlCLENBQUMsQ0FBQyxDQUFDO1FBQ2hFLDZCQUF3QixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxTQUFTLENBQUMsb0VBQW9FLENBQUMsQ0FBQyxDQUFDO1FBQ3RJLDBCQUFxQixHQUFrQixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsU0FBUyxDQUFDLCtEQUErRCxDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUMxSSw2QkFBd0IsR0FBa0Isb0JBQU8sQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLFNBQVMsQ0FBQywrREFBK0QsQ0FBQyxDQUFDLENBQUMsSUFBSSxFQUFFLENBQUM7UUFDNUksNkJBQXdCLEdBQXVCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxTQUFTLENBQUMseURBQXlELENBQUMsQ0FBQyxDQUFDO1FBQ3BJLDBCQUFxQixHQUF1QixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsU0FBUyxDQUFDLG9DQUFvQyxDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLFNBQVMsQ0FBQyw2Q0FBNkMsQ0FBQyxDQUFDLENBQUM7UUFDckwsNkJBQXdCLEdBQXVCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxTQUFTLENBQUMsb0NBQW9DLENBQUMsQ0FBQyxDQUFDLElBQUksRUFBRSxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsU0FBUyxDQUFDLDZDQUE2QyxDQUFDLENBQUMsQ0FB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