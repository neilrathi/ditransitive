import React from "react";
import { useEffect } from 'react';
import { useHMSActions } from "@100mslive/react-sdk";

const base =
  "inline-flex items-center px-4 py-2 border text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-empirica-500";

export function AudioRoom({
  userName,
  roomCode,
  className = "",
  forceJoin = false
}) {
  const hmsActions = useHMSActions();

  const handleSubmit = async (e) => {
    // use room code to fetch auth token
    const authToken = await hmsActions.getAuthTokenByRoomCode({ roomCode })

    try {
      await hmsActions.join({ userName, authToken });
    } catch (e) {
      console.error('Error joining room:', e)
    }
  };

  if (forceJoin) {
    handleSubmit();
    return null
  } else {
    return (
      <button className={`${base} ${className}`} onClick = {handleSubmit}>
        Join
      </button>
    );
  }
}  