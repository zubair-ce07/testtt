import { by, element, ElementFinder , ElementArrayFinder, browser } from 'protractor';
import { browserWaitHandler } from '../shared/utils';

export class HotelDetailPage {
    getGoToMapLink () : ElementFinder {
        return element(by.css('[id$=filtersSection] > a '));
    }
    getHotelDetailLink () : ElementFinder {
    return element(by.css('.normalResults > div:nth-child(2) div.mainItemWrapper button.allowWrap'));
    }
    getMapTabLink () : ElementFinder {
        return element.all(by.css('[id$=detailsContent] div[data-tab=map]')).first();
    }
    getratesTabLInk () : ElementFinder {
        return element.all(by.css('[id$=detailsContent] div[data-tab=rates]')).first();
    }
    getReviewTabLink () : ElementFinder {
        return element.all(by.css('[id$=detailsContent] div[data-tab=reviews]')).first();
    }
    getHotelDetailSection () : ElementFinder {
       return element.all(by.css('[id$=detailsContent] .inlineTab.active')).first();
    }
    getHotelImages () : ElementFinder {
       return element.all(by.css('[id$=overviewContainer] .col-photos')).first();
    }
    getMapSection () : ElementFinder {
     return element.all(by.css('[id$=mapContainer]')).first();
    }
    getReviewsSection () : ElementFinder {
      return element.all(by.css('[id$=reviewsContainer]')).first();
    }
    getRatesSection () : ElementFinder {
      return element.all(by.css('[id$=ratesContainer]')).first();
    }
    getGoToMapSection () : ElementFinder {
      return element(by.css('[id$=rightRail] .rail-map-container > div'));
    }
    getAllHotelMarkers () : ElementArrayFinder {
        return element.all(by.css('.hotel-marker'));
    }
    getViewDealButton (viewDealBtnId : string) : ElementFinder {
       return element(by.id(viewDealBtnId));
    }
    getMarkerSummary () : ElementFinder {
      return  element(by.css('[id*=summaryCard]'));
    }
    async getHotelMarkerId () : Promise<string>   {
        browserWaitHandler(this.getAllHotelMarkers().get(0));
        await this.getAllHotelMarkers().get(0).click();
        const markerId = await this.getAllHotelMarkers().get(0).getAttribute('id');
        const  markerIdSuffix = markerId.split('-')[1];
        return markerIdSuffix;
    }
    async getViewDealBUttonId () : Promise<void>   {
      const  markerIdSuffix =  await this.getHotelMarkerId();
      const viewDealBtnId = `${markerIdSuffix}-booking-bookButton`;
      await this.getViewDealButton(viewDealBtnId).click();
      browser.wait(browser.getAllWindowHandles() , 10000);
      const handlers = await browser.getAllWindowHandles();
      await browser.switchTo().window(handlers[1]);
  }

}

