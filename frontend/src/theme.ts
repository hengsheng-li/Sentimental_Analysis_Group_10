import { ThemeOptions } from "@mui/material/styles";

// Types for color tokens
type ColorShades = {
    [key: number]: string;
};

type Tokens = {
    grey: ColorShades;
    primary: ColorShades;
    secondary: ColorShades;
};

// Color design tokens export
export const tokensDark: Tokens = {
    grey: {
        0: "#ffffff",
        10: "#f6f6f6",
        50: "#f0f0f0",
        100: "#e0e0e0",
        200: "#c2c2c2",
        300: "#a3a3a3",
        400: "#858585",
        500: "#666666",
        600: "#525252",
        700: "#3d3d3d",
        800: "#292929",
        900: "#141414",
        1000: "#000000",
    },

    primary: {
        // Blue - Background Color
        50: "#e6e9f2",
        100: "#bfc9e0",
        200: "#96a6ca",
        300: "#6d84b5",
        400: "#4d6aa7",
        500: "#285199",
        600: "#214990",
        700: "#174085",
        800: "#282f45",
        900: "#070f24",
    },

    secondary: {
        // Purple - Text Color
        50: "#ebecff",
        100: "#cdcefe",
        200: "#abaefe",
        300: "#878dfe",
        400: "#6b70fc",
        500: "#5253f8",
        600: "#4c49ec",
        700: "#433ddf",
        800: "#3c30d3",
        900: "#3415bb",
    },
};


// Function for reversing the color palette
function reverseTokens(tokens: Tokens): Tokens {
    const reversedTokens = {} as Tokens;

    (Object.entries(tokens) as [keyof Tokens, ColorShades][]).forEach (
        ([key, val]) => {
            const keys = Object.keys(val);
            const values = Object.values(val)
            const length = keys.length;
            const reversedObj: ColorShades = {};

            for (let i = 0; i < length; i++) {
                reversedObj[Number(keys[i])] = values[length - i - 1];
            }

            reversedTokens[key] = reversedObj;
        }
    );

    return reversedTokens;
}

export const tokensLight: Tokens = reverseTokens(tokensDark);

// MUI Theme Settings
export const themeSettings = (mode: "light" | "dark") => {
    return {
        palette: {
            mode: mode,
            ...(mode === "dark"
                ?{
                    // DARK MODE palette values
                    primary: {
                        ...tokensDark.primary,
                        main: tokensDark.primary[500],
                        light: tokensDark.primary[400],
                    },

                    // Icon and Title Color
                    secondary: {
                        ...tokensDark.secondary,
                        main: tokensDark.secondary[50],
                    },

                    neutral: {
                        ...tokensDark.grey,
                        main: tokensDark.grey[500],
                    },

                    // Background Color
                    background: {
                        default: tokensDark.primary[900],
                        alt: tokensDark.primary[800],
                    },
                }
                : {

                    // LIGHT MODE palette values
                    primary: {
                        ...tokensLight.primary,
                        main: tokensDark.grey[50],
                        light: tokensDark.grey[100],
                    },

                    secondary: {
                        ...tokensLight.secondary,
                        main: tokensDark.secondary[500],
                        light: tokensDark.secondary[700],
                    },

                    neutral: {
                        ...tokensLight.grey,
                        main: tokensDark.grey[500],
                    },

                    background: {
                        default: tokensDark.grey[0],
                        alt: tokensDark.grey[50],
                    },
                }),
        },

        typography: {
            fontFamily: ["Inter", "sans-serif"].join(","),
            fontSize: 12,

            h1: {
                fontFamily: ["Inter", "sans-serif"].join(","), fontSize: 40
            },

            h2: {
                fontFamily: ["Inter", "sans-serif"].join(","), fontSize: 32
            },

            h3: {
                fontFamily: ["Inter", "sans-serif"].join(","), fontSize: 24
            },

            h4: {
                fontFamily: ["Inter", "sans-serif"].join(","), fontSize: 20
            },

            h5: {
                fontFamily: ["Inter", "sans-serif"].join(","), fontSize: 16
            },

            h6: {
                fontFamily: ["Inter", "sans-serif"].join(","), fontSize: 14
            },
        },
    };
};