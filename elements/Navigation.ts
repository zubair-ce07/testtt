import { by, element } from 'protractor'

export class Navigation {
  async to(page: 'flights' | 'hotels' | 'cars' | 'packages' | 'cruises'): Promise<void> {
    return element(by.className(`js-vertical-${page}`)).click();
  }
}
