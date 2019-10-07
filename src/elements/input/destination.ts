export interface Destination {
  type(text: string): Promise<void>;
  
  getDisplayText(): Promise<string>;
}
