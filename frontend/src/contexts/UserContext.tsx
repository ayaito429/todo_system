"use client";
import { useState, useEffect, createContext, useContext } from "react";
import { getAccessToken } from "../lib/api/client";
import { getMe } from "../lib/api/auth";

type User = {
  user_id: number;
  email: string;
  role: string;
  name: string;
};

const UserContext = createContext<{
  user: User | null;
  setUser: (u: User | null) => void;
}>(null!);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const token = getAccessToken();

    if (!token) {
      setLoaded(true);
      return;
    }
    getMe(token)
      .then((data) => setUser(data))
      .catch(() => setUser(null))
      .finally(() => setLoaded(true));
  }, []);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  return useContext(UserContext);
}
