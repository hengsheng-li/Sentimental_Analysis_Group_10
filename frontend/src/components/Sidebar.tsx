import React, { useEffect, useState } from "react";

import {
    Box,
    Divider,
    Drawer,
    IconButton,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Typography,
    useTheme,
} from "@mui/material";

import {
    ChevronLeft,
    ChevronRightOutlined,
    HomeOutlined,
    ShoppingCartOutlined,
    Groups2Outlined,
    ReceiptLongOutlined,
    PublicOutlined,
    PointOfSaleOutlined,
    TodayOutlined,
    CalendarMonthOutlined,
    AdminPanelSettingsOutlined,
    TrendingUpOutlined,
    PieChartOutlined,
} from "@mui/icons-material";

import { useLocation, useNavigate } from "react-router-dom";
import Flex from "./Flex";

// Navigation Items
interface NavItem {
    text: string;
    icon: React.ReactNode | null;
}

// Props for Sidebar
interface SidebarProps {
    drawerWidth: string;
    isSidebarOpen: boolean;
    setIsSidebarOpen: React.Dispatch<React.SetStateAction<boolean>>;
    isNonMobile: boolean;
}

const navItems: NavItem[] = [
    { text: "Dashboard", icon: <HomeOutlined /> },
    { text: "Products", icon: <ShoppingCartOutlined /> },
    { text: "Overview", icon: <PointOfSaleOutlined /> },
    { text: "Daily", icon: <TodayOutlined /> },
    { text: "Monthly", icon: <CalendarMonthOutlined /> },
    { text: "Breakdown", icon: <PieChartOutlined /> },
    { text: "Performance", icon: <TrendingUpOutlined /> },
];


const Sidebar: React.FC<SidebarProps> = ({
    drawerWidth,
    isSidebarOpen,
    setIsSidebarOpen,
    isNonMobile,
}) => {
    const { pathname } = useLocation();
    const [active, setActive] = useState<string>("");
    const navigate = useNavigate();
    const theme = useTheme();

    useEffect(() => {
        setActive(pathname.substring(1)); // Keeps track of url
    }, [pathname]);


    return (
        <Box component = "nav">
            {isSidebarOpen && (
                <Drawer
                    open = {isSidebarOpen}
                    onClose={() => setIsSidebarOpen(false)}
                    variant="persistent"
                    anchor="left"
                    sx={{
                        width: drawerWidth,
                        "& .MuiDrawer-paper": {
                            color: (theme.palette.secondary as any)[200], // Text color
                            backgroundColor: theme.palette.background.alt,
                            boxSizing: "border-box",
                            borderWidth: isNonMobile ? 0 : "2px",
                            width: drawerWidth,
                        },
                    }}
                    >
                        <Box width = "100%">
                            {/* Header */}
                            <Box m = "1.5rem 2rem 2rem 3rem">
                                <Flex color = { theme.palette.secondary.light }>
                                    <Box display="flex" alignItems="center" gap="0.5rem">
                                        <Typography variant="h4" fontWeight="bold">
                                            ANALYTICS
                                        </Typography>
                                    </Box>
                                    {!isNonMobile && (
                                        <IconButton onClick={() => setIsSidebarOpen(!isSidebarOpen)}>
                                            <ChevronLeft />
                                        </IconButton>
                                    )}
                                </Flex>
                            </Box>


                            {/* Navigation Items */}
                            <List>
                                {navItems.map(({ text, icon}) => {
                                    if (!icon) {
                                        return (
                                            <Typography key={text} sx={{ m: "2.25rem 0 1rem 3rem"}}>
                                                {text}
                                            </Typography>
                                        );
                                    }
                                    const lcText = text.toLowerCase();

                                    return (
                                        <ListItem key={text} disablePadding>
                                            <ListItemButton
                                            onClick={() => {
                                                navigate(`/${lcText}`); // Navigates to the url on click
                                                setActive(lcText); // Highlights color
                                            }}
                                            sx={{
                                                backgroundColor:
                                                active === lcText
                                                ? (theme.palette.secondary as any)[400] // Border color around text when active
                                                : "transparent",
                                            }}
                                            >
                                                <ListItemIcon
                                                sx={{
                                                    ml: "2rem",
                                                    color:
                                                    active === lcText
                                                    ? (theme.palette.secondary as any)[50] // Icon Color for Dashboard
                                                    : theme.palette.secondary.light, // Icon Color for Navigation items
                                                }}
                                                >
                                                    {icon}
                                                </ListItemIcon>
                                                <ListItemText primary={text} />
                                                {active === lcText && (
                                                    <ChevronRightOutlined sx={{ ml: "auto"}} />
                                                )}
                                            </ListItemButton>
                                        </ListItem>
                                    );
                                })}
                            </List>
                        </Box>
                    <Divider />
                </Drawer>
            )}
        </Box>
    );
};

export default Sidebar