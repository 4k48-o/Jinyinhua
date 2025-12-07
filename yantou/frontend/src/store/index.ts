import { configureStore } from '@reduxjs/toolkit'
import authReducer from './slices/authSlice'
import roleReducer from './slices/roleSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    role: roleReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

