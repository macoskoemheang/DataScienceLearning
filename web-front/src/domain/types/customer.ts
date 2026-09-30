export interface Customer {
  id: number;
  name: string;
  phone: string;
  email: string;
  created_at: string;
}

export interface CustomerInput {
  name: string;
  phone?: string;
  email?: string;
}
