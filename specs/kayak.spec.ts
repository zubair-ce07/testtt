import { browser }                                                from "protractor";
import { expect, use }                                            from "chai";
import chaiAsPromised                                             from "chai-as-promised";
import { FlightFilterType, LandingPage, PassengerType, TripType } from "../pages/Flights";
import { formatDate, removeNonNumericValues }                     from "../utils/specs.util";
import { FlightsResultsPage }                                     from "../pages/FlightsResults";

use(chaiAsPromised);

describe('Kayak.com', function () {
  beforeAll((done) => {
    browser.waitForAngularEnabled(false).then(() => done())
  });
  
  let page: LandingPage;
  
  beforeEach(done => {
    page = new LandingPage();
    page.load().then(done)
  });
  
  it('should visit flights page', async function () {
    // step-1
    expect(page.searchForm.origin.get().isPresent()).eventually.to.be.true;
    expect(page.searchForm.destination.get().isPresent()).eventually.to.be.true;
    expect(page.searchForm.dateRange.getDepartureDateDisplayValue()).eventually.to.be.not.null;
    expect(page.searchForm.dateRange.getReturnDateDisplayValue()).eventually.to.be.not.null;
    expect(page.searchForm.trip.value()).eventually.to.equal('Round-trip');
    
    // step-2
    await page.searchForm.trip.select(TripType.OneWay);
    expect(page.searchForm.trip.value()).eventually.to.equal('One-way');
    
    // step-3
    await page.searchForm.trip.select(TripType.MultiCity);
    expect(page.searchForm.trip.value()).eventually.to.equal('Multi-city');
    //
    // step-4
    await page.searchForm.trip.select(TripType.RoundTrip);
    expect(page.searchForm.trip.value()).eventually.to.equal('Round-trip');
    
    // step-5
    await page.searchForm.passengers.openDialog();
    page.searchForm.passengers.increment(PassengerType.Adults, 9);
    browser.sleep(1000);
    expect(page.searchForm.passengers.errorMessage()).eventually.to.equal('Searches cannot have more than 9 adults');
    await page.searchForm.passengers.closeDialog();
    
    // step-6
    await page.searchForm.origin.type('PAR');
    await page.searchForm.origin.select(1);
    browser.sleep(2000);
    expect(page.searchForm.origin.getSelectedValue()).eventually.to.equal('Paris (PAR)');
    
    // step-7
    await page.searchForm.destination.type('NYC');
    await page.searchForm.destination.select(1);
    browser.sleep(2000);
    expect(page.searchForm.destination.getSelectedValue()).eventually.to.equal('New York (NYC)');
    
    // step-8
    await page.searchForm.passengers.set(PassengerType.Adults, 4);
    expect(page.searchForm.passengers.value()).eventually.to.equal('4 Travelers');
    
    // step-9
    await page.searchForm.passengers.set(PassengerType.Child, 2);
    page.searchForm.passengers.closeDialog();
    expect(page.searchForm.passengers.value()).eventually.to.equal('6 Travelers');
    
    // step-{10,11}
    await page.searchForm.dateRange.open();
    const date = new Date();
    const currentDate = new Date(`${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`);
    const departureDate = new Date(currentDate.setDate(currentDate.getDate() + 3));
    const returnDate = new Date(currentDate.setDate(currentDate.getDate() + 6));
    await page.searchForm.dateRange.selectDate(departureDate, returnDate);
    
    expect(page.searchForm.dateRange.getDepartureDateDisplayValue())
      .eventually.to.equal(formatDate(departureDate));
    
    expect(page.searchForm.dateRange.getReturnDateDisplayValue())
      .eventually.to.equal(formatDate(returnDate));
    
    // step-12
    await page.searchForm.compare.selectNone();
    
    // step-13
    const results: FlightsResultsPage = await page.searchForm.submit();
    await results.load();
    await results.dialog.closeIfOpen();
    
    const cheapestPrice: any = await results.header.getCost(FlightFilterType.Cheapest).then(price => {
      return Number(price.replace('$', ''))
    });
    const bestPrice: any = await results.header.getCost(FlightFilterType.Best).then(price => {
      return Number(price.replace('$', ''))
    });
    
    expect(results.form.trip.value()).eventually.to.equal('Round-trip');
    expect(results.form.passengers.value()).eventually.to.equal('6 Travelers');
    expect(results.form.dateRange.getReturnDateDisplayValue()).eventually.to.equal(formatDate(returnDate));
    expect(results.form.dateRange.getDepartureDateDisplayValue()).eventually.to.equal(formatDate(departureDate));
    expect(cheapestPrice).to.be.lte(bestPrice);
    
    const quickestTime = await results.header.getDuration(FlightFilterType.Quickest).then(toTimeString);
    const slowestTime = await results.header.getDuration(FlightFilterType.Cheapest).then(toTimeString);
    const isLessThanOrEqual: boolean = Date.parse(`01/01/1990 ${quickestTime}`) <= Date.parse(`01/01/1990 ${slowestTime}`);
    expect(isLessThanOrEqual).to.be.true;
    
  });
  
});

function toTimeString(timestring: string) {
  const [hours, minutes]: any = timestring.trim().split(' ').map(removeNonNumericValues).map(Number);
  return `${hours}:${minutes}:00`
}
