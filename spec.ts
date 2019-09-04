import chai from 'chai';
import chaiAsPromised from 'chai-as-promised'
import {browser} from "protractor";
import KayakAirlineFees from "./pages/KayakAirlineFees";
chai.use(chaiAsPromised);

const expect = chai.expect;
const assert = chai.assert;

describe('KAYAK Airline-Fees',async () => {
    const kayakAirlineFees = new KayakAirlineFees();
    let allExternalURLsReport: any = [];
    before(async () => {
        await browser.get('https://www.kayak.com/airline-fees');
        allExternalURLsReport = await kayakAirlineFees.getReportOfAllURLs();
        testAllURLs();
    });
    it('Data fetch completed',async () => {
        assert.isAbove(allExternalURLsReport.length,0);
    });
    function testAllURLs() {
        allExternalURLsReport.forEach((currentSite: any) => {
            describe('Test status code of all external links', async () => {
                it('Test url '+ currentSite.url,() => {
                    expect(currentSite.statusCode).to.equal(200);
                })
            })
        });
    }

});