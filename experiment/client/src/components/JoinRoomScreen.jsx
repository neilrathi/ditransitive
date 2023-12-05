import React from "react";
import { AudioRoom } from "./AudioRoom";
import { useEffect } from 'react';
import { useHMSActions } from "@100mslive/react-sdk";

const base =
  "inline-flex items-center px-4 py-2 border text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-empirica-500";

export function JoinRoomScreen({
  userName,
  roomCode
}) {
  return(
    <div>
      <p>Click to join an audio call with your partner for Phase 3.</p>
      <div className = "flex justify-center m-5">
        <AudioRoom userName = {userName} roomCode = {roomCode} forceJoin = {false}/>
      </div>
      <p>Continue to the next round when you've successfully joined the call.</p>
    </div>
  );
}  