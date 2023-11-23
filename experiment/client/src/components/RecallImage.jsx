import React from "react";
import { usePlayer, useRound, useStage } from "@empirica/core/player/classic/react";
import { Button } from '../components/Button'

export function RecallImage({}) {
  const round = useRound();
  const player = usePlayer();

  return (
    <div className = 'justify-center m-5' style = {{width: "400px", padding: '2px'}}>
      <img src={'../../unique/' + round.get('label') + '.png'} />
      <div className="justify-center">
        <table>
          <tr>
            <td>
              <input type = "text" />
            </td>
            <td>
              <Button handleClick={() => player.stage.set("submit", true)}> Submit </Button>
            </td>
          </tr>
        </table>
      </div>
    </div>
  );
}
