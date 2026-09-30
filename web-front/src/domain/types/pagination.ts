export interface Paginated<T> {
  items: T[];
  page: number;
  per_page: number;
  total: number;
}

export interface PageParams {
  page?: number;
  per_page?: number;
  search?: string;
}
