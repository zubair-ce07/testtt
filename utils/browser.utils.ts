import { browser, ElementFinder, ExpectedConditions as EC } from "protractor";

export async function scrollElementIntoView(element: ElementFinder): Promise<void> {
  return browser.executeScript((elm: HTMLElement) => elm.scrollIntoView(false), element);
}

export async function waitForElementToBeInteractive(element: ElementFinder, timeout?: number, message?: string) {
  await browser.wait(
    EC.and(
      EC.presenceOf(element),
      EC.visibilityOf(element),
      EC.elementToBeClickable(element)
    ),
    timeout,
    message
  );
}
