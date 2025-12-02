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
} from "@mui/material";
import Header from "../../components/Header";
import appleProducts from "../../data/products.json";

interface Stat {
  yearlySalesTotal: number;
  yearlyTotalSoldUnits: number;
}

interface ProductProps {
  _id: string;
  name: string;
  description?: string;
  price: number;
  rating?: number;
  category: string;
  supply?: number;
  stat?: Stat;
  imgUrl?: string;
}

const ProductDisplay: React.FC<ProductProps> = ({
  _id,
  name,
  description = "Largest and most durable display in an Apple Watch at the time, advanced health tracking functionalities, and faster charging",
  price,
  rating = 0,
  category,
  supply = 0,
  stat = { yearlySalesTotal: 0, yearlyTotalSoldUnits: 0 },
  imgUrl,
}) => {
  const theme = useTheme();
  const [isExpanded, setIsExpanded] = useState<boolean>(false);

  return (
    <Card
      sx={{
        backgroundColor: "#fff",
        boxShadow: theme.shadows[8],
        borderRadius: "1rem",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        transition: "all 0.3s ease",
        width: "410px",
        "&:hover": {
          boxShadow: theme.shadows[12],
          transform: "translateY(-4px)",
        },
      }}
    >
      {imgUrl && (
        <Box
          sx={{
            width: "100%",
            height: "250px",
            overflow: "hidden", // prevents layout shifting
            borderBottom: "1px solid #eee",
          }}
        >
          <Box
            component="img"
            src={imgUrl}
            alt={name}
            sx={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
            }}
          />
        </Box>
      )}

      <CardContent>
        <Typography sx={{ fontSize: 14 }} color={"#000"} gutterBottom>
          {category}
        </Typography>
        <Typography
          variant="h4"
          component="div"
          sx={{ fontWeight: 900, color: "#000" }}
        >
          {name}
        </Typography>
        <Typography sx={{ mb: "1.5rem", fontSize: "1rem" }} color={"#000"}>
          ${Number(price).toFixed(2)}
        </Typography>
        <Rating value={rating} readOnly />
        <Typography variant="body2" sx={{ mt: 1 }} color={"#000"}>
          {description}
        </Typography>
      </CardContent>

      <CardActions sx={{ display: "flex", justifyContent: "center" }}>
        <Button
          variant="contained"
          size="small"
          onClick={() => setIsExpanded(!isExpanded)}
          sx={{
            textTransform: "none",
            borderRadius: "0.2rem",
            mt: 2,
          }}
        >
          {"View Analytics"}
        </Button>
      </CardActions>

      <Collapse
        in={isExpanded}
        timeout="auto"
        unmountOnExit
        sx={{ color: theme.palette.primary.light }}
      ></Collapse>
    </Card>
  );
};

const Products: React.FC = () => {
  const productsMapped: ProductProps[] = appleProducts.map((p) => ({
    _id: p.id.toString(),
    name: p.name,
    price: p.price,
    category: p.category,
    imgUrl: p.imgUrl,
  }));

  return (
    <Box m="2.5rem 3.5rem">
      <Header title="PRODUCTS" subtitle="View the Latest Apple Products" />
      <Box
        mt="20px"
        display="grid"
        gridTemplateColumns="repeat(auto-fill, minmax(250px, 1fr))"
        gap="20px"
      >
        {productsMapped.map((product) => (
          <ProductDisplay key={product._id} {...product} />
        ))}
      </Box>
    </Box>
  );
};

export default Products;
