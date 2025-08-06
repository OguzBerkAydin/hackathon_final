export interface Source {
  title: string;
  url: string;
}

export interface EcommerceLinks {
  [productName: string]: {
    [siteName: string]: string;
  };
}

export interface RecommendationResponse {
  recommendation: string;
  product_category: string;
  recommended_products: string[];
  ecommerce_links: EcommerceLinks;
  sources: Source[];
}
