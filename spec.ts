import {browser} from "protractor";
import KayakHomepage from "./pages/KayakHomepage";
import chai from "chai";
import chaiAsPromised from "chai-as-promised";
import CommonHelper from "./helper/CommonHelper";
chai.use(chaiAsPromised);
chai.should();
const expect = chai.expect;

describe('Testing for Kayak.com', () => {
    const commonHelperObj = new CommonHelper();
    const kayakHomepageObj = new KayakHomepage();

    before(async () => browser.get('https://www.kayak.com/'));

    it('Should show "Flights"', () =>  kayakHomepageObj.isBtnVisible('flights').should.eventually.equal(true));

    it('Should show "Hotels"', () => kayakHomepageObj.isBtnVisible('hotels').should.eventually.equal(true));

    it('Should show "Cars"',() => kayakHomepageObj.isBtnVisible('cars').should.eventually.equal(true));

    it('Should load FFD once tapping on "Flights" ',async () => {
        await kayakHomepageObj.loadPage('flights');
        expect(await commonHelperObj.getCurrentURL()).to.contain('flights');
    });

    it('Should highlight the Flights btn',() => kayakHomepageObj.isHighlighted('flights').should.eventually.equal(true));

    it('should load /hotels once tapping on "Hotels" ',async () => {
        await kayakHomepageObj.loadPage('hotels');
        expect(await commonHelperObj.getCurrentURL()).to.contain('hotels');
    });

    it('Should highlight the Hotels btn', () => kayakHomepageObj.isHighlighted('hotels').should.eventually.equal(true));

    it('Should load /car-rental once tapping on "Cars" ',async () => {
        await kayakHomepageObj.loadPage('cars');
        expect(await commonHelperObj.getCurrentURL()).to.contain('cars');
    });

    it('Should highlight the Cars Btn',() => kayakHomepageObj.isHighlighted('cars').should.eventually.equal(true));
});
