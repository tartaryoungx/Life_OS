"use client";

import { useState } from "react";
import { events, tasks } from "../../features/today/data/mockActivities";
import type { ActivityCard } from "../../features/today/type";

const initialCards: ActivityCard[] = [
  {
    title: "Events",
    emoji: "📆",
    variant: "green",
    items: events.map((item) => ({
      ...item,
      completed: false,
    })),
  },
  {
    title: "Tasks",
    emoji: "📋",
    variant: "teal",
    items: tasks.map((item) => ({
      ...item,
      completed: false,
    })),
  },
];

export default function Test() {
    console.log(initialCards)
  return (
    <p>a</p>
  )}