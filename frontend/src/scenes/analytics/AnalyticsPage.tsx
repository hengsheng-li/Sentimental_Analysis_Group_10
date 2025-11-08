import React from "react";
import reviewSummary from "../../data/AirpodReview.json";
import { Box, Typography, Card, CardContent } from "@mui/material";

const ProductAnalytics: React.FC = () => {
  const { summary, attribute_analysis } = reviewSummary;

  return (
    <Box m="2rem">
      <Card sx={{ p: 2 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            {summary.product_analyzed} Review Summary
          </Typography>

          <Typography>
            Total Reviews: {summary.total_reviews_analyzed}
          </Typography>
          <Typography>Valid Analyses: {summary.valid_analyses}</Typography>

          <Typography sx={{ mt: 2, fontWeight: "bold" }}>
            Review Sentiment Breakdown:
          </Typography>
          <Typography>
            Positive: {summary.review_categorization.positive}
          </Typography>
          <Typography>
            Neutral: {summary.review_categorization.neutral}
          </Typography>
          <Typography>
            Negative: {summary.review_categorization.negative}
          </Typography>

          <Typography sx={{ mt: 2, fontWeight: "bold" }}>
            Battery Life Analysis:
          </Typography>
          <Typography>
            Average: {attribute_analysis.battery_life.average}
          </Typography>
          <Typography>Min: {attribute_analysis.battery_life.min}</Typography>
          <Typography>Max: {attribute_analysis.battery_life.max}</Typography>
          <Typography>
            Standard Deviation: {attribute_analysis.battery_life.std_dev}
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ProductAnalytics;
