export function all<T>(items: T[], callback: (item: T, idx: number) => void) {
  items.forEach((item, idx) => callback(item, idx));
}

export function getAirportCode(string: string): string {
  return string.match(/\(([^)]+)\)/)[1]
}

export function formatDate(date: Date) {
  return `${dayNumberToName(date.getDay()).slice(0, 3)} ${date.getMonth() + 1}/${date.getDate()}`
}

export function dayNumberToName(day) {
  return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][day]
}

export function removeNonNumericValues(string): string {
  return string.replace(/[^0-9]+/, '');
}

export function toTimeString(timestring: string) {
  const [hours, minutes]: any = timestring.trim().split(' ').map(removeNonNumericValues).map(Number);
  return `${hours}:${minutes}:00`
}
