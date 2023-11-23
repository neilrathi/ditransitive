import React from "react";
import { usePlayer, useRound, } from "@empirica/core/player/classic/react";
import { Button } from "../components/Button";

export function Result() {
  const player = usePlayer();
  const round = useRound();

  const rightSelection = (round.get("decision") == round.get("target"));

  const messageSubject = player.get("role") == "guesser" ? "You" : "Your partner";
  const messageContinuation = rightSelection ? " made the right selection!" : " made the wrong selection!"
  const message = messageSubject + messageContinuation

  return (
    <div>
      
      <table>
        <tr>
          <td style = {{paddingRight: "10px"}}> {message}  </td>
          <td> <Button handleClick={() => player.stage.set("submit", true)}> Continue </Button> </td>
        </tr>
      </table>
      
      

    </div>

  );
}