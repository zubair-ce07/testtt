export interface Page {
  getURL(): string;
  
  visit(): Promise<void>;
}
