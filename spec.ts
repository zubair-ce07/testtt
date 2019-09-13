import {browser} from "protractor";
import * as chai from "chai";
import * as chaiAsPromised from "chai-as-promised";
import CarResultPage from "./pages/CarResultPage";
import KayakHomepage from "./pages/KayakHomepage";
import KayakCarsHomepage from "./pages/KayakCarsHomepage";
import * as moment from "moment";

chai.use(chaiAsPromised);

const expect = chai.expect;

describe('Kayak cars',() => {
    const kayakHomepageObj = new KayakHomepage();
    const kayakCarsHomepage = new KayakCarsHomepage();
    const carResultPageObj = new CarResultPage();

    before(async () => {
        await browser.get('https://www.kayak.com/');
    });
    it('Should load cars page',async () => {
        await kayakHomepageObj.clickCarsBtn();
    });
    it('Should have "Same drop-off" search option selected by default',  () => {
        expect(kayakCarsHomepage.getDropOffStatus()).to.eventually.equal('Same drop-off');
    });
    it('Should be able to select "Different drop-off" search option',async () => {
        await kayakCarsHomepage.clickDropOffLabel();
        await kayakCarsHomepage.clickDifferentDropOffOption();
        expect(kayakCarsHomepage.getDropOffStatus()).to.eventually.equal('Different drop-off');
    });
    it('Should display destination input field after selecting "different drop-off" search option', async () => {
        expect(kayakCarsHomepage.isDestinationFieldVisible()).to.eventually.equal(true);
    });
    it('Should have departure date selected to current date + 1', async () => {
        await kayakCarsHomepage.clickDepartureInput();
        const dayAfterCurrentDate = moment().add(1,'days').format('L');
        const selectedDepartureDate = await kayakCarsHomepage.getSelectedDepartureDate();
        expect(selectedDepartureDate).to.equal(dayAfterCurrentDate);
    });
    it('Should have arrival date selected to current date + 3', async () => {
        const threeDaysAfterCurrentDate = moment().add(3,'days').format('L');
        const selectedArrivalDate =await kayakCarsHomepage.getSelectedArrivalDate();
        expect(selectedArrivalDate).to.equal(threeDaysAfterCurrentDate);
    });
    it('Should be able to add origin in Smarty',async () => {
        await kayakCarsHomepage.setOrigin();
        expect(await kayakCarsHomepage.isOriginAdded()).to.equal('true');
    });
    it('Should be able to add destination in Smarty',async () => {
        await kayakCarsHomepage.setDestination();
        expect(await kayakCarsHomepage.isDestinationAdded()).to.equal('true');
    });
    it('Should be able to click search button and redirect to result page', async () => {
        await kayakCarsHomepage.clickSearchBtn();
        expect(await carResultPageObj.isCarResultsLoaded());
    });
    it('should not have map view on CRP', async () => {
        expect(await carResultPageObj.isMapVisible()).to.equal(false);
    });
    it('Should have 15 inline results on result page', async () => {
        expect(await carResultPageObj.getCarResultCount()).to.equal(15);
    });
});
