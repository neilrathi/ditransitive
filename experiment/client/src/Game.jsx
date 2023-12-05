import { usePlayer, useStage } from "@empirica/core/player/classic/react";

import React from "react";
import { Profile } from "./Profile";
import { Options } from "./components/Options";
import { TrainImage } from "./components/TrainImage";
import { RecallImage } from "./components/RecallImage";
import { Instructions } from "./components/Instructions";
import { ExampleOptions } from "./components/ExampleOptions";
import { JoinRoomScreen } from "./components/JoinRoomScreen";

export function Game() {

  const stage = useStage()
  const player = usePlayer()

  // show images if on selection/result stage
  const options = stage.get("name") == "result" & player.stage.get("submit") ? null :
    stage.get("name") == "joinroom" ? <JoinRoomScreen userName = {player.id} roomCode = {player.get("roomCode")} /> :
    stage.get("name") == "train" ? <TrainImage /> :
    stage.get("name") == "recall" ? <RecallImage /> :
    stage.get("name") == "instructions" ? <Instructions /> :
    stage.get("name") == "example-choice" ? <ExampleOptions /> :
    stage.get("name") == "example-result" ? <ExampleOptions /> :
    <Options />

  return (
    <div className="h-full w-full flex">
      <div className="h-full w-full flex flex-col">
        <Profile />
        <div className="h-full flex items-center justify-center">
          {options}
        </div>
      </div>

    </div>

    
  );
}
