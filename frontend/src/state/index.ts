import { createSlice, PayloadAction } from "@reduxjs/toolkit";

// Define state type
interface GlobalState {
    mode: "light" | "dark";
    userId: string;
}

// Initial state with type
const initialState: GlobalState = {
    mode: "dark",
    userId: "63701cc1f03239b7f700000e",
};

// Creates slice
export const globalSlice = createSlice({
  name: "global",
  initialState,
  reducers: {
    setMode: (state) => {
      state.mode = state.mode === "light" ? "dark" : "light";
    },
  },
});

export const { setMode } = globalSlice.actions;

export default globalSlice.reducer;