import chai from 'chai';
import chaiAsPromised from 'chai-as-promised'
import {browser} from "protractor";
import KayakHomepage from "./pages/KayakHomepage";
import KayakTripsHomepage from "./pages/KayakTripsHomepage";
import AddTripPopup from "./popups/AddTripPopup";
import EditTripPopup from "./popups/EditTripPopup";
import DeleteTripPopup from "./popups/DeleteTripPopup";
chai.use(chaiAsPromised);

const expect = chai.expect;
const assert = chai.assert;

describe('Kayak Trips',() => {
    const kayakHomepageObj = new KayakHomepage();
    const kayakTripsHomepageObj = new KayakTripsHomepage();
    const addTripPopupObj = new AddTripPopup();
    const editTripPopupObj = new EditTripPopup();
    const deleteTripPopupObj = new DeleteTripPopup();
    let tripEditedData: object = {};
    before(async () => {
        await browser.get('https://www.kayak.com/');
    });
    it('Should load trips page',async () => {
        await kayakHomepageObj.goToTripsPage();
        expect(kayakTripsHomepageObj.isTripsPageLoaded()).to.eventually.equal(true);
    });
    it('Should login successfully', async () => {
        await kayakHomepageObj.getSignInDropdown();
        await kayakHomepageObj.signInUsingCred();
        expect(await kayakHomepageObj.isUserSignedIn()).to.equal(true);
    });
    it('Should Create new trip', async () => {
        await kayakTripsHomepageObj.clickCreateTripBtn();
        await addTripPopupObj.setTripDestination();
        await addTripPopupObj.setTripName();
        await addTripPopupObj.setTripDuration();
        await addTripPopupObj.saveTrip();
        expect(await kayakTripsHomepageObj.isTripSaved()).to.equal(true);
    });
    it('Should edit trip', async () => {
        await kayakTripsHomepageObj.clickEditTripBtn();
        await editTripPopupObj.editTripDestination();
        await editTripPopupObj.editTripName();
        await editTripPopupObj.editTripDuration();
        tripEditedData = await editTripPopupObj.getTripDetails();
        await editTripPopupObj.saveTrip();
        expect(await kayakTripsHomepageObj.isTripSaved()).to.equal(true);
    });
    it('Should save trip details correctly', async () => {
        expect(await kayakTripsHomepageObj.isTripDetailsSavedCorrectly()).equal(JSON.stringify(tripEditedData));
    });
    it('Should delete trip', async () => {
        await kayakTripsHomepageObj.clickMoreOptionsBtn();
        await kayakTripsHomepageObj.clickDeleteTrip();
        await deleteTripPopupObj.deleteTrip();
    })
});