import {browser, element, by, protractor, promise, ElementFinder, ProtractorExpectedConditions, Key, ElementArrayFinder} from 'protractor';
import { url } from 'inspector';

export class HomePageObject {
  url: string = 'https://www.momondo.de/';
  title: ElementFinder = element(by.className("title-container"));
  travelInspirationSection: ElementFinder = element(by.className("Common-Frontdoor-Brands-Momondo-Brandonly-TravelInspirationSection"));
  trendingCitiesSection: ElementFinder = element.all(by.className("Common-Frontdoor-Brands-Momondo-Brandonly-DestinationsSection")).first();
  trendingCountriesSection: ElementFinder = element.all(by.className("Common-Frontdoor-Brands-Momondo-Brandonly-DestinationsSection")).last();
  tilesInTravelInspiration: ElementArrayFinder = element.all(by.className("Common-Frontdoor-Brands-Momondo-Brandonly-ImageCardItem"));
  tilesInTrendingCities: ElementArrayFinder = element.all(by.className("Common-Seo-Brands-Momondo-CardGrid")).first().all(by.className("Common-Seo-Brands-Momondo-LinkCardWithImage"));
  tilesInTrendingCountries: ElementArrayFinder = element.all(by.className("Common-Seo-Brands-Momondo-CardGrid")).last().all(by.className("Common-Seo-Brands-Momondo-LinkCardWithImage"));
  travelFirstImage: ElementFinder = this.tilesInTravelInspiration.first().all(by.tagName('img')).first();
  citiesFirstImage: ElementFinder = this.tilesInTrendingCities.first().element(by.tagName('a'));
  countriesFirstImage: ElementFinder = this.tilesInTrendingCountries.first().element(by.tagName('a'));
  moreInspirationButton: ElementFinder = this.travelInspirationSection.element(by.className("Common-Widgets-Button-StyleJamButton"));
  closePopupButton: ElementFinder = element.all(by.className("Button-No-Standard-Style close")).last();

  async displayTravelInspirationSection(): Promise<boolean> {
    browser.actions().mouseMove(this.travelInspirationSection).perform();
    return await this.travelInspirationSection.isDisplayed();
  }

  async displayTrendingCitiesSection(): Promise<boolean> {
    browser.actions().mouseMove(this.trendingCitiesSection).perform();
    return await this.trendingCitiesSection.isDisplayed();
  }

  async displayTrendingCountriesSection(): Promise<boolean> {
    browser.actions().mouseMove(this.trendingCountriesSection).perform();
    return await this.trendingCountriesSection.isDisplayed();
  }

  async getTilesInTravelInspiration(): Promise<number> {
    const travelInspirationTiles =  await this.tilesInTravelInspiration.count();
    let tileLength;
    travelInspirationTiles >= 2 ? tileLength=true : tileLength=false  
    return tileLength;
  }

  async getTrendingCityTiles(): Promise<number> {
    browser.actions().mouseMove(this.trendingCitiesSection).perform();
    const tilesInTrendingCities =  await this.tilesInTrendingCities.count();
    let cityTiles;
    tilesInTrendingCities >= 20 ? cityTiles=true : cityTiles=false  
    return cityTiles;
  }

  async getTrendingCountriesTiles(): Promise<number> {
    browser.actions().mouseMove(this.trendingCountriesSection).perform();
    const tilesInTrendingCountries =  await this.tilesInTrendingCities.count();
    let countryTiles;
    tilesInTrendingCountries >= 20 ? countryTiles=true : countryTiles=false  
    return countryTiles;
  }

  async getTravelInspirationFirstImage(): Promise<boolean> {
    let travelFirstImage;
    const tagName = await this.travelFirstImage.getTagName();
    tagName == "img" ? travelFirstImage=true : travelFirstImage=false;
    return travelFirstImage;
  }

  async clickFirstTravelInspirationTile(): Promise<string> {
    (this.tilesInTravelInspiration.first()).click();
    return await browser.getCurrentUrl();
  }

  async clickFirstCityTile(): Promise<string> {
    browser.get(this.url);
    browser.actions().mouseMove(this.tilesInTrendingCities.first()).perform();
    (this.tilesInTrendingCities.first()).click();
    return await browser.getCurrentUrl();
  }

  async clickFirstCountryTile(): Promise<string> {
    browser.get(this.url);
    browser.actions().mouseMove(this.tilesInTrendingCountries.first()).perform();
    (this.tilesInTrendingCountries.first()).click();
    return await browser.getCurrentUrl();
  }

  async clickMoreInspirationButton(): Promise<string> {
    browser.get(this.url);
    browser.actions().mouseMove(this.moreInspirationButton).perform();
    this.moreInspirationButton.click();
    return await browser.getCurrentUrl();
  }

  async clearCookies() {
    let until: ProtractorExpectedConditions = await protractor.ExpectedConditions; 
    await browser.wait(
    until.visibilityOf(this.closePopupButton),
    40000, `${this.closePopupButton} not appeared in expected time`)
    await this.closePopupButton.click();
  }
}
