import React from "react";
import { Button } from "../components/Button";
import { usePlayer, useRound } from "@empirica/core/player/classic/react";

export function InstructionsBar() {
  const player = usePlayer();
  const round = useRound();

  const phase = round.get("instructions") == "recall" ? `2: Recall` :
                round.get("instructions") == "train" ? `1: Memorization` :
                round.get("instructions") == "example" ? `3: Choice` :
                round.get("instructions") == "choice" ? `3: Choice` : null

  return (
    <div>
      
    <table>
      <tr>
        <td style = {{paddingRight: "10px"}}> Instructions for Phase {phase}</td>
        <td> <Button handleClick={() => player.stage.set("submit", true)}> Continue </Button> </td>
      </tr>
    </table>
    
  </div>
  );
}