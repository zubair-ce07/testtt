import { FlightsResultsPage } from "../core/pages/flightsResultsPage";
import { FlightsPage } from "../core/pages/flightsPage";

export function range(start: number, end: number): number[] {
  return Array.from(Array(end - start)).map((value, index) => start + index);
}

export function reduceIsSame(items: any[][]): boolean {
  return items.reduce((result, array) => (
    result && array.reduce((result, item) => result && (item === array[0]), true)
  ), true)
}

export function reduceHaveText(items: string[]): boolean {
  return items.reduce((result, text) => result && text.length > 0, true)
}

export async function removeFlightLegsUntilResults(flights: FlightsPage, results: FlightsResultsPage, maxLegsToRemove: number): Promise<boolean> {
  return Promise.resolve(false);
}
