export interface BrandPageFactory<T> {
  create(brand: string): T;
}
