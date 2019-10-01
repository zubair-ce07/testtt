export function formatDate(date: Date) {
  return `${dayNumberToName(date.getDay()).slice(0, 3)} ${date.getMonth() + 1}/${date.getDate()}`
}

export function dayNumberToName(day) {
  return ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][day]
}

export function addDays(date: Date, days: number): Date {
  return new Date(date.setDate(date.getDate() + days))
}
