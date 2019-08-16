import { browser, by, element, ElementFinder , $ , $$, ElementArrayFinder } from 'protractor';

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

}
