import React from "react";
import { Button } from "../components/Button";
import { usePlayer } from "@empirica/core/player/classic/react";

export function JoinRoom() {
  const player = usePlayer();

  return (
    <div>

      <table>
        <tr>
          <td style = {{paddingRight: "10px"}}> You are the {player.get("role")}. Say hi to your partner! </td>
          <td> <Button handleClick={() => player.stage.set("submit", true)}> Continue </Button> </td>
        </tr>
      </table>          

    </div>
  );
}