import React from "react";
import { usePlayer, useRound, useStage } from "@empirica/core/player/classic/react";

export function TrainImage({}) {
  const round = useRound();

  return (
    <div className = 'justify-center m-5' style = {{width: "400px", padding: '2px'}}>
      <img src={'../../unique/' + round.get('label') + '.png'} />
      <div className="flex justify-center m-5">
        <strong className = 'text-2xl'>{round.get('label')}</strong>
      </div>
    </div>
  );
}
