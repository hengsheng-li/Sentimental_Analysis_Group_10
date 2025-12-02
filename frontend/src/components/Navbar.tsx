import React, { useState, MouseEvent } from "react";
import {
    LightModeOutlined,
    DarkModeOutlined,
    Menu as MenuIcon,
    Search,
    SettingsOutlined,
} from "@mui/icons-material";

import Flex from "../components/Flex";
import { useDispatch } from "react-redux";
import { setMode } from "../state";

import {
    AppBar,
    Box,
    IconButton,
    InputBase,
    Toolbar,
    useTheme
} from "@mui/material";

// Props interface
interface NavbarProps {
    isSidebarOpen: boolean;
    setIsSidebarOpen: (value: boolean) => void;
}

const Navbar: React.FC<NavbarProps> = ({ isSidebarOpen, setIsSidebarOpen }) => {
    const dispatch = useDispatch();
    const theme = useTheme();

    return (
        <AppBar
        sx = {{
            position: "static",
            background: "none",
            boxShadow: "none",
        }}
        >
            <Toolbar sx = {{ justifyContent: "space-between" }}>
                {/* Left Side */}
                <Flex>
                    <IconButton onClick = {() => setIsSidebarOpen(!isSidebarOpen)}>
                        <MenuIcon />
                    </IconButton>
                <Flex
                    backgroundColor = { theme.palette.background.default }
                    borderRadius = "9px"
                    gap = "3rem"
                    p = "0.1rem 1.5rem"
                >
                    <InputBase placeholder = "Search..." />
                    <IconButton>
                        <Search />
                    </IconButton>
                    </Flex>
                </Flex>

                {/* Right Side */}
                <Flex gap="1.5rem">
                    <IconButton onClick = {() => dispatch(setMode())}>
                        {theme.palette.mode === "dark" ? (
                            <DarkModeOutlined sx = {{ fontSize: "25px" }} />
                        ) : (
                            <LightModeOutlined sx = {{ fontSize: "25px"}} />
                        )}
                    </IconButton>
                </Flex>
            </Toolbar>
        </AppBar>
    );
};

export default Navbar