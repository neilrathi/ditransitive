import React from "react";
import { usePlayer, useRound, useStage } from "@empirica/core/player/classic/react";
import { Button } from '../components/Button'

export function RecallImage({}) {
  const round = useRound();
  const player = usePlayer();

  return (
    <div className = 'justify-center m-5' style = {{width: "400px", padding: '2px'}}>
      <div style = {{width: "400px", border: "solid 5px black", padding: '2px'}}>
        <img src={'../../unique/' + round.get('label') + '.png'} />
      </div><br></br>
      <div className="flex justify-center">
        <table>
          <tr>
            <td>
            <input 
              placeholder = "Label"
              type="text" 
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  player.stage.set("submit", true);
                }
              }}
            />
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
