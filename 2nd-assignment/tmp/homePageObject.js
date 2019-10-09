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
        this.citiesFirstImage = this.tilesInTrendingCities.first().element(protractor_1.by.tagName('a'));
        this.countriesFirstImage = this.tilesInTrendingCountries.first().element(protractor_1.by.tagName('a'));
        this.moreInspirationButton = this.travelInspirationSection.element(protractor_1.by.className("Common-Widgets-Button-StyleJamButton"));
        this.closePopupButton = protractor_1.element.all(protractor_1.by.className("Button-No-Standard-Style close")).last();
    }
    displayTravelInspirationSection() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.actions().mouseMove(this.travelInspirationSection).perform();
            return yield this.travelInspirationSection.isDisplayed();
        });
    }
    displayTrendingCitiesSection() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.actions().mouseMove(this.trendingCitiesSection).perform();
            return yield this.trendingCitiesSection.isDisplayed();
        });
    }
    displayTrendingCountriesSection() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.actions().mouseMove(this.trendingCountriesSection).perform();
            return yield this.trendingCountriesSection.isDisplayed();
        });
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
            (this.tilesInTravelInspiration.first()).click();
            return yield protractor_1.browser.getCurrentUrl();
        });
    }
    clickFirstCityTile() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.get(this.url);
            protractor_1.browser.actions().mouseMove(this.tilesInTrendingCities.first()).perform();
            (this.tilesInTrendingCities.first()).click();
            return yield protractor_1.browser.getCurrentUrl();
        });
    }
    clickFirstCountryTile() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.get(this.url);
            protractor_1.browser.actions().mouseMove(this.tilesInTrendingCountries.first()).perform();
            (this.tilesInTrendingCountries.first()).click();
            return yield protractor_1.browser.getCurrentUrl();
        });
    }
    clickMoreInspirationButton() {
        return __awaiter(this, void 0, void 0, function* () {
            protractor_1.browser.get(this.url);
            protractor_1.browser.actions().mouseMove(this.moreInspirationButton).perform();
            this.moreInspirationButton.click();
            return yield protractor_1.browser.getCurrentUrl();
        });
    }
    clearCookies() {
        return __awaiter(this, void 0, void 0, function* () {
            let until = yield protractor_1.protractor.ExpectedConditions;
            yield protractor_1.browser.wait(until.visibilityOf(this.closePopupButton), 40000, `${this.closePopupButton} not appeared in expected time`);
            yield this.closePopupButton.click();
        });
    }
}
exports.HomePageObject = HomePageObject;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaG9tZVBhZ2VPYmplY3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9ob21lUGFnZU9iamVjdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBLDJDQUEySTtBQUczSSxNQUFhLGNBQWM7SUFBM0I7UUFDRSxRQUFHLEdBQVcseUJBQXlCLENBQUM7UUFDeEMsVUFBSyxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxTQUFTLENBQUMsaUJBQWlCLENBQUMsQ0FBQyxDQUFDO1FBQ2hFLDZCQUF3QixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxTQUFTLENBQUMsb0VBQW9FLENBQUMsQ0FBQyxDQUFDO1FBQ3RJLDBCQUFxQixHQUFrQixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsU0FBUyxDQUFDLCtEQUErRCxDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUMxSSw2QkFBd0IsR0FBa0Isb0JBQU8sQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLFNBQVMsQ0FBQywrREFBK0QsQ0FBQyxDQUFDLENBQUMsSUFBSSxFQUFFLENBQUM7UUFDNUksNkJBQXdCLEdBQXVCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxTQUFTLENBQUMseURBQXlELENBQUMsQ0FBQyxDQUFDO1FBQ3BJLDBCQUFxQixHQUF1QixvQkFBTyxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsU0FBUyxDQUFDLG9DQUFvQyxDQUFDLENBQUMsQ0FBQyxLQUFLLEVBQUUsQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLFNBQVMsQ0FBQyw2Q0FBNkMsQ0FBQyxDQUFDLENBQUM7UUFDckwsNkJBQXdCLEdBQXVCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxTQUFTLENBQUMsb0NBQW9DLENBQUMsQ0FBQyxDQUFDLElBQUksRUFBRSxDQUFDLEdBQUcsQ0FBQyxlQUFFLENBQUMsU0FBUyxDQUFDLDZDQUE2QyxDQUFDLENBQUMsQ0FB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