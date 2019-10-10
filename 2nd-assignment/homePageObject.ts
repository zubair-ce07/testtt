import {browser, element, by, protractor, promise, ElementFinder, ProtractorExpectedConditions, Key, ElementArrayFinder} from 'protractor';
import { url } from 'inspector';
import { async } from 'q';

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
  travelFirstImageUrl: ElementFinder = this.tilesInTravelInspiration.first();
  citiesFirstImage: ElementFinder = this.tilesInTrendingCities.first().element(by.tagName('a'));
  countriesFirstImage: ElementFinder = this.tilesInTrendingCountries.first().element(by.tagName('a'));
  moreInspirationButton: ElementFinder = this.travelInspirationSection.element(by.className("Common-Widgets-Button-StyleJamButton"));
  closePopupButton: ElementFinder = element.all(by.className("Button-No-Standard-Style close")).last();

  travelSection(): ElementFinder {
    browser.actions().mouseMove(this.travelInspirationSection).perform();
    return this.travelInspirationSection;
  }

  citiesSection(): ElementFinder {
    browser.actions().mouseMove(this.trendingCitiesSection).perform();
    return this.trendingCitiesSection;
  }

  countriesSection(): ElementFinder {
    browser.actions().mouseMove(this.trendingCountriesSection).perform();
    return this.trendingCountriesSection;
  }

  async getTilesInTravelInspiration(): Promise<boolean> {
    const travelInspirationTiles = await this.tilesInTravelInspiration.count();
    let tileLength;
    travelInspirationTiles >=2 ? tileLength=true : tileLength=false  
    return tileLength;
  }

  async getTrendingCityTiles(): Promise<boolean> {
    browser.actions().mouseMove(this.trendingCitiesSection).perform();
    const tilesInTrendingCities = await this.tilesInTrendingCities.count();
    let cityTiles;
    tilesInTrendingCities >= 20 ? cityTiles=true : cityTiles=false  
    return cityTiles;
  }

  async getTrendingCountriesTiles(): Promise<boolean> {
    browser.actions().mouseMove(this.trendingCountriesSection).perform();
    const tilesInTrendingCountries = await this.tilesInTrendingCities.count();
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

  async clickFirstTravelInspirationTile(): Promise<boolean> {
    let firstTravelInspiration;
    let firstTravelImageUrl = await this.travelFirstImageUrl.getAttribute('href');
    (this.tilesInTravelInspiration.first()).click();
    return (await browser.getCurrentUrl()).includes(firstTravelImageUrl) ? firstTravelInspiration=true : firstTravelInspiration=false;
  }

  async clickFirstCityTile(): Promise<boolean> {
    let firstCity;
    browser.actions().mouseMove(this.tilesInTrendingCities.first()).perform();
    let firstImageUrl =  await this.citiesFirstImage.getAttribute('href');
    (this.tilesInTrendingCities.first()).click();
    return (await browser.getCurrentUrl()).includes(firstImageUrl) ? firstCity=true : firstCity=false;
  }

  async clickFirstCountryTile(): Promise<boolean> {
    let firstCountry: boolean;
    browser.actions().mouseMove(this.tilesInTrendingCountries.first()).perform();
    let firstCountryUrl = await this.countriesFirstImage.getAttribute('href');
    (this.tilesInTrendingCountries.first()).click();
    return (await browser.getCurrentUrl()).includes(firstCountryUrl) ? firstCountry=true : firstCountry=false;
  }

  async clickMoreInspirationButton(): Promise<boolean> {
    let moreInspirationButton;
    browser.actions().mouseMove(this.moreInspirationButton).perform();
    let moreInspirationUrl = await this.moreInspirationButton.getAttribute('href');
    this.moreInspirationButton.click();
    return (await browser.getCurrentUrl()).includes(moreInspirationUrl) ? moreInspirationButton=true : moreInspirationButton=false;
  }

  async clearCookies() {
    let until: ProtractorExpectedConditions = await protractor.ExpectedConditions;
    await browser.wait(
    until.visibilityOf(this.closePopupButton),
    4000, `${this.closePopupButton} not appeared in expected time`);
    await this.closePopupButton.click();
  }

  async navigateToHomePage() {
    await browser.get(this.url);
  }
}
