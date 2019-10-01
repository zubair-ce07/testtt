export interface PageFactory<T> {
  create(brand: string): T;
}
