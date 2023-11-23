import React from "react";
import { AudioRoom } from "../components/AudioRoom";
import { usePlayer } from "@empirica/core/player/classic/react";

export function Choice() {
  const player = usePlayer();
  const sec = "border-transparent shadow-sm text-white bg-empirica-600 hover:bg-empirica-700";
  const instructions = player.get("role") == 'director' ? 'Describe the target image.' : 'Identify the target image.'

  return (
    <div>

      You are the <strong>{player.get("role")}</strong>. {instructions} <AudioRoom userName = {player.id} roomCode = {player.get("roomCode")} forceJoin = {false}/>

    </div>
  );
}