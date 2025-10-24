import React, { useEffect, useState } from "react";

import {
  Box,
  Card,
  CardActions,
  CardContent,
  Collapse,
  Button,
  Typography,
  Rating,
  useTheme,
}

from "@mui/material";
import Header from "../../components/Header";

interface Stat {
  yearlySalesTotal: number;
  yearlyTotalSoldUnits: number;
}

interface ProductProps {
  _id: string;
  name: string;
  description: string;
  price: number;
  rating: number;
  category: string;
  supply: number;
  stat: Stat;
}

const Product: React.FC<ProductProps> = ({
  _id,
  name,
  description,
  price,
  rating,
  category,
  supply,
  stat,
}) => {
  const theme = useTheme();
  const [isExpanded, setIsExpanded] = useState<boolean>(false);

  return (
    <Card
      sx={{
        backgroundImage: "none",
        backgroundColor: theme.palette.primary.light,
        borderRadius: "0.55rem",
      }}
      >
        <CardContent>
          <Typography
            sx={{ fontSize: 14 }}
            color={theme.palette.secondary.main}
            gutterBottom
          >
            {category}
          </Typography>
          <Typography variant="h5" component="div">
            {name}
          </Typography>
          <Typography sx={{ mb: "1.5rem" }} color={theme.palette.secondary.light}>
                         ${Number(price).toFixed(2)}
          </Typography>
          <Rating value={rating} readOnly />

        <Typography variant="body2">{description}</Typography>
      </CardContent>
      <CardActions>
        <Button
          variant="contained"
          size="small"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          See More
        </Button>
      </CardActions>
      <Collapse
        in={isExpanded}
        timeout="auto"
        unmountOnExit
        sx={{
          color: theme.palette.primary.light,
        }}
      >
        <CardContent>
          <Typography>id: {_id}</Typography>
          <Typography>Supply Left: {supply}</Typography>
          <Typography>Yearly Sales This Year: {stat.yearlySalesTotal}</Typography>
          <Typography>Yearly Units Sold This Year: {stat.yearlyTotalSoldUnits}</Typography>
        </CardContent>
      </Collapse>
    </Card>
  );
};

const Products: React.FC = () => {
  const isLoading = false;

  // Temporary mock data with Material UI to visualize the cards on screen
  const mockData: ProductProps[] = [
    {
      _id: "1",
      name: "Laptop",
      description: "A powerful laptop with long battery life.",
      price: 1299.99,
      rating: 4.5,
      category: "Electronics",
      supply: 27,
      stat: { yearlySalesTotal: 50000, yearlyTotalSoldUnits: 250 },
    },
    {
      _id: "2",
      name: "Headphones",
      description: "Noise-cancelling headphones.",
      price: 299.99,
      rating: 4.7,
      category: "Audio",
      supply: 74,
      stat: { yearlySalesTotal: 15000, yearlyTotalSoldUnits: 400 },
    },
  ];

   return (
    <Box m="1.5rem 2.5rem">
      <Header title="PRODUCTS" subtitle="See your list of products." />
      {!isLoading ? (
        <Box
          mt="20px"
          display="grid"
          gridTemplateColumns="repeat(4, minmax(0, 1fr))"
          justifyContent="space-between"
          rowGap="20px"
          columnGap="1.33%"
        >
          {mockData.map((product) => (
            <Product key={product._id} {...product} />
          ))}
        </Box>
      ) : (
        <>Loading...</>
      )}
    </Box>
  );
};


interface ProductsPage {
  review: string;
  asin: string;
}

const ProductsPage = () => {
  const [products, setProducts] = useState<ProductData[]>([]);
  const [reviews, setReviews] = useState<{ asin: String; review: string }[]>([]);

  // Fetch product reviews from CSV file
  useEffect(() => {
    fetch("http://localhost:5002/api/products")
      .then((res) => res.json())
      .then((data) => {
        const formatted = data.map((item: any) => ({
          review: item['It drys up quickly; otherwise'] || "",
          asin: item['it appears to work']?.["\""] || "",
        }));
        setProducts(formatted);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="p-6 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {products.map((p, i) => (
        <div
          key={i}
          className="border rounded-xl shadow-lg p-4 bg-white hover:shadow-2xl transition-shadow duration-300"
        >
          <h3 className="text-lg font-bold mb-2">ASIN: {p.asin || "N/A"}</h3>
          <p className="text-gray-700">{p.review || "No review available"}</p>
        </div>
      ))}
    </div>
  );
};

export default Products;