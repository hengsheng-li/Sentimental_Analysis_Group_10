import React, { useEffect, useState } from "react";

interface ProductData {
  review?: string;
  asin?: string;
}

const ProductData: React.FC = () => {
  const [products, setProducts] = useState<ProductData[]>([]);

  useEffect(() => {
    fetch("http://localhost:5002/api/products")
      .then(res => res.json())
      .then(data => {
        const formatted = data
          .map((item: any) => ({
            review: item["It drys up quickly; otherwise"] || item["review"] || "",
            asin: item["it appears to work"]?.["\""] || item["ASIN"] || "",
          }))
          .filter((p: ProductData) => p.asin || p.review);
        setProducts(formatted);
      })
      .catch(err => console.error("Error fetching products:", err));
  }, []);

  return (
    <div className="p-6 grid gap-4">
  {products.map((p, i) => (
    <div key={i} className="border rounded-xl shadow p-4 bg-white">
      <p><strong>ASIN:</strong> {p.asin || "N/A"}</p>
      <p><strong>Review:</strong> {p.review || "N/A"}</p>
    </div>
  ))}
</div>
  );
};

export default ProductData;