import { browser, by, element, ElementArrayFinder } from "protractor";
import SiteKayakPageObject from "./SiteKayakPageObject";
import SiteMomontoPageObject from "./SiteMomontoPageObject";

class BasePageObject {
    readonly currentSiteURL: string;
    protected page: SiteKayakPageObject | SiteMomontoPageObject = null;

    constructor() {
        this.currentSiteURL = browser.params.site_url;
        this.setPage();
    }

    setPage(): void {
        if (this.currentSiteURL.includes("kayak")) {
            this.page = new SiteKayakPageObject();
        }
        else {
            this.page = new SiteMomontoPageObject();
        }
    }
}

export default BasePageObject;