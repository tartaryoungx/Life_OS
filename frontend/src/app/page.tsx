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
        if (!liff.isLoggedIn()) {
          liff.login();
          return;
        }
        const profile = await liff.getProfile();

        setName(profile.displayName);
      
        const res = await fetch(
          "https://backend-xxxx.up.railway.app/api/users/sync",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              line_user_id: profile.userId,
              display_name: profile.displayName,
              picture_url: profile.pictureUrl,
            }),
          }
        );
        console.log(await res.json());
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