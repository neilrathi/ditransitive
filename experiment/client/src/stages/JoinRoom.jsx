import React from "react";
import { Button } from "../components/Button";
import { usePlayer } from "@empirica/core/player/classic/react";

export function JoinRoom() {
  const player = usePlayer();

  return (
    <div>

      <table>
        You are the {player.get("role")}. Say hi to your partner!
      </table>          

    </div>
  );
}