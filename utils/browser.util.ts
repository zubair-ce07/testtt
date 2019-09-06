import { browser } from "protractor";

export function waitForPageLoad() {
  return (callback) => {
    if (document.readyState === 'complete') {
      return callback()
    }
    
    window.addEventListener('load', () => {
      if (document.readyState === 'complete') {
        callback()
      }
    });
  }
}

export function switchToNewTabIfOpened() {
  return browser.getAllWindowHandles()
    .then(windows => {
      if (windows.length > 1) {
        return browser.switchTo()
          .window(windows[windows.length - 1])
          .then(() => browser.executeAsyncScript(waitForPageLoad()))
      }
    })
}
