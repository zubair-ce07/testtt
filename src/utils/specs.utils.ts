import axios from 'axios';

export async function findCurrentLocation(): Promise<string> {
  const response = await axios.get('http://ip-api.com/json');
  const { city, country } = response.data;
  return [city, country].join(', ');
}

export function diffInDays(d1: string, d2: string): number {
  const ONE_DAY_IN_MS = 24 * 60 * 60 * 1000;
  return (toDate(d2).getTime() - toDate(d1).getTime()) / ONE_DAY_IN_MS;
}

export function toDate(text: string): Date {
  const [month, date] = text.split(' ')[1].split('/').map(Number);
  return new Date(new Date().getFullYear(), month - 1, date);
}
