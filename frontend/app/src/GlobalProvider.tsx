import React from "react";

import { AuthProvider } from "./context/authContext";
import { UserProvider } from "./context/userContext";

interface GlobalProviderProps {
  children: React.ReactNode;
}

export function GlobalProvider({ children }: GlobalProviderProps) {
  return (
    <AuthProvider>
      <UserProvider>{children}</UserProvider>
    </AuthProvider>
  );
}
