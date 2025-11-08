import type React from "react";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { createTheme, Theme } from "@mui/material/styles";
import { useMemo } from "react";
import { useSelector, TypedUseSelectorHook } from "react-redux";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { themeSettings } from "./theme";
import Layout from "./scenes/layout";
import Dashboard from "./scenes/dashboard";
import type { RootState } from "index";
import ProductsPage from "./scenes/products/ProductsPage";
import AnalyticsPage from "./scenes/analytics/AnalyticsPage";

const useTypedSelector: TypedUseSelectorHook<RootState> = useSelector;

function App(): React.JSX.Element {
  const mode = useTypedSelector((state) => state.global.mode);
  const theme: Theme = useMemo(() => createTheme(themeSettings(mode)), [mode]);

  return (
    <div className="app">
      <BrowserRouter>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <Routes>
            <Route element={<Layout />}>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/products" element={<ProductsPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
            </Route>
          </Routes>
        </ThemeProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;