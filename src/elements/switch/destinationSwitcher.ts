export interface DestinationSwitcher {
  getOptions(): Promise<string[]>;
}
