import chai from 'chai';
import chaiAsPromised from 'chai-as-promised'
import {browser} from "protractor";
import KayakAirlineFees from "./pages/KayakAirlineFees";
chai.use(chaiAsPromised);
const expect = chai.expect;

describe('KAYAK Airline-Fees',async () => {
    const kayakAirlineFees = new KayakAirlineFees();
    before(async () => {
        await browser.get('https://www.kayak.com/airline-fees');
    });
    it('Should get status code of all external links',async () => {
        const allExternalURLsReport: any = await kayakAirlineFees.getReportOfAllURLs();
        console.log(allExternalURLsReport);
        console.log('Failed tests report: ');
        allExternalURLsReport.forEach((currentSite: any) => {
            console.log(currentSite);
        });
    })
});