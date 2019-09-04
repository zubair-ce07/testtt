import request from 'request'
import {by, element, ElementArrayFinder, ElementFinder} from "protractor";

export default class KayakAirlineFees {
    airlineLinksContainer: ElementFinder = element(by.css('.airlineLinksSection'));
    allExternalURLs: ElementArrayFinder = this.airlineLinksContainer.all(by.css('a'));


    async getAllExternalURLs(): Promise<string> {
        return await this.allExternalURLs.getAttribute('href');
    }
    getRequest(currentURL: string): Promise<object> {
        return new Promise((resolve,reject) => {
            console.log('Request called for ',currentURL);
            request({
                url: currentURL,
                method: 'GET',
                headers: {'Content-Type': 'text/html'},
                timeout: 5000
                },(error: any,response: any) => {
                if(error) return reject({url: currentURL,statusCode: 'undefined',error: error});
                return resolve({
                    url: currentURL,
                    statusCode: response.statusCode
                });
            });
        })
    }
    async getReportOfAllURLs(): Promise<object> {
        let allExternalURLs: any = await this.getAllExternalURLs();
        let index = 0;
        while (index < 20) {
            allExternalURLs[index] = await this.getRequest(allExternalURLs[index]).catch(error => {
                return {url: allExternalURLs[index], statusCode: 400}
            });
            index++;
        }
        return allExternalURLs.splice(0,index);
    }
}