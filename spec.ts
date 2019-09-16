import {browser} from "protractor";
import KayakHomepage from "./pages/KayakHomepage";
import chai from "chai";
import CommonHelper from "./helper/CommonHelper";
const expect = chai.expect;

const commonHelperObj = new CommonHelper();
const kayakHomepageObj = new KayakHomepage();
describe('Testing for Kayak.com', () => {
    before(async () => {
        browser.get('https://www.kayak.com/');
    });
    it('Should show "Flights"', async () => {
        expect(await kayakHomepageObj.isFlightsBtnVisible()).to.equal(true);
    });
    it('Should show "Hotels"', async () => {
        expect(await kayakHomepageObj.isHotelsBtnVisible()).to.equal(true);
    });
    it('Should show "Cars"', async () => {
        expect(await kayakHomepageObj.isCarsBtnVisible()).to.equal(true);
    });
    it('Should load FFD once tapping on "Flights" ',async () => {
        await kayakHomepageObj.clickFlightsBtn();
        await commonHelperObj.waitForURLToBeLoaded('flights');
        expect(await commonHelperObj.getCurrentURL()).to.contain('flights');
        expect(await kayakHomepageObj.isFlightsBtnHighlighted()).to.equal(true);
    });
    it('should load /hotels once tapping on "Hotels" ',async () => {
        await kayakHomepageObj.clickHotelsBtn();
        await commonHelperObj.waitForURLToBeLoaded('hotels');
        expect(await commonHelperObj.getCurrentURL()).to.contain('hotels');
    });
    it('Should highlight the Hotels btn', async () => {
        expect(await kayakHomepageObj.isHotelsBtnHighlighted()).to.equal(true);
    });
    it('Should load /car-rental once tapping on "Cars" ',async () => {
        await kayakHomepageObj.clickCarsBtn();
        await commonHelperObj.waitForURLToBeLoaded('cars');
        expect(await commonHelperObj.getCurrentURL()).to.contain('cars');
    });
    it('Should highlight the Cars Btn', async () => {
        expect(await kayakHomepageObj.isCarsBtnHighlighted()).to.equal(true);
    });
});
