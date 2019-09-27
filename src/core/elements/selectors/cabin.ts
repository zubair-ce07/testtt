export interface CabinSelector {
  select(option: 'Economy' | 'Business' | 'Premium Economy' | 'First'): Promise<void>;
  
  getDisplayText(): Promise<string>;
}
