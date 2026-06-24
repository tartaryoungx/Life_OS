"use client";

import liff from "@line/liff";
import { useEffect, useState } from "react";

export default function LiffPage() {
  const [name, setName] = useState("Loading...");

  useEffect(() => {
    async function init() {
      try {
        await liff.init({
          liffId: process.env.NEXT_PUBLIC_LIFF_ID!,
        });

        if (liff.isLoggedIn()) {
          const profile = await liff.getProfile();
          setName(profile.displayName);
        }
      } catch (err) {
        console.error(err);
      }
    }

    init();
  }, []);

  return (
    <main style={{ padding: 24 }}>
      <h1>Life OS</h1>
      <p>Welcome, {name}</p>
    </main>
  );
}