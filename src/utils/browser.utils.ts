import { browser, ElementFinder, ExpectedConditions as EC } from "protractor";

export async function waitUntilInteractive(element: ElementFinder, timeout?: number, message?: string): Promise<void> {
  return browser.wait(
    EC.and(
      EC.presenceOf(element),
      EC.visibilityOf(element),
      EC.elementToBeClickable(element)
    ),
    timeout,
    message,
  )
}

export function scrollIntoView(element: ElementFinder): void {
  browser.executeScript((element: HTMLElement) => element.scrollIntoView(false), element)
}

export async function switchToTab(index: number): Promise<void> {
  const windows = await browser.getAllWindowHandles();
  await browser.switchTo().window(windows[index]);
}
