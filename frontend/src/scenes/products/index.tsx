import React, { useState } from "react";
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
//import { useGetProductsQuery } from "state/api";

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

  // Temporary mock data to visualize the cards on screen
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

export default Products;