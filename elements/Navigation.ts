import { by, element } from 'protractor'

export class Navigation {
  to(page: 'flights' | 'hotels' | 'cars' | 'packages' | 'cruises') {
    return element(by.className(`js-vertical-${page}`)).click();
  }
}
