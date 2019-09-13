import { browser } from 'protractor';
import { expect, use } from 'chai';
import chaiAsPromised from 'chai-as-promised';

use(chaiAsPromised);

describe('Google.com', () => {
  beforeAll(done => {
    browser.waitForAngularEnabled(false).then(done)
  });
  
  it('should open google.com', async () => {
    const url = 'https://www.google.com';
    browser.get(url);
    expect(browser.getCurrentUrl()).eventually.to.contain(url);
  });
});
