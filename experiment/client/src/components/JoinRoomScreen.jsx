import React, { useState } from 'react';
import { AudioRoom } from "./AudioRoom";
import { Button } from "../components/Button";
import { usePlayer } from "@empirica/core/player/classic/react";

const base =
  "inline-flex items-center px-4 py-2 border text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-empirica-500";

export function JoinRoomScreen({
  userName,
  roomCode
}) {
  const player = usePlayer();

  const [isAudioRoomClicked, setIsAudioRoomClicked] = useState(false);
  const audioRoomClick = () => {
    setIsAudioRoomClicked(true);
  };

  return(
    <div>
      <p>Click to join an audio call with your partner for Phase 3.</p>
      <div className = "flex justify-center m-5">
      {isAudioRoomClicked ? (
          <Button handleClick={() => player.stage.set("submit", true)}> Continue </Button>
        ) : (
          <AudioRoom userName = {userName} roomCode = {roomCode} forceJoin = {false} handleClick={audioRoomClick}/>
        )}
        
      </div>
      <p>Continue to the next round when you've successfully joined the call.</p>
    </div>
  );
}  