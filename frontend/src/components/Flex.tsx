import { Box, BoxProps } from "@mui/material";
import { styled } from "@mui/system";

// Extends BoxProps for proper typing
const Flex = styled(Box)<BoxProps>({
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
});

export default Flex;