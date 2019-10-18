export function addDays(date: Date, days: number): Date {
  const result = new Date(date.getDate());
  result.setDate(result.getDate() + days);
  return result;
}

export function toDateString(date: Date, withDay: boolean = false): string {
  const [day, month, _date] = date.toDateString().split(' ');
  const result = [month, _date].join(' ');
  
  return withDay ? `${day}, `.concat(result) : result;
}
