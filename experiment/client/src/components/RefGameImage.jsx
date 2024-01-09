import React from "react";
import { usePlayer, useRound, useStage } from "@empirica/core/player/classic/react";

const base =
  "inline-flex items-center px-4 py-2 border text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-empirica-500";
const prim =
  "border-gray-300 shadow-sm text-gray-700 bg-white hover:bg-gray-50";
const sec =
  "border-transparent shadow-sm text-white bg-empirica-600 hover:bg-empirica-700";

export function RefGameImage({
  children,
  tag = "",
  handleClick = null,
}) {
  const player = usePlayer();
  const stage = useStage();
  const round = useRound();

  // certain images are highlighted for the director at the 'choice' stage, and for both players at the 'result' stage
  const highlightImage = (player.get("role") == "director" || stage.get("name") == "result" || stage.get("name") == "example-result") &
  (round.get("target") == tag || (stage.get("name") == "result" & round.get("decision") == tag ) || (stage.get("name") == "example-result" & round.get("decision") == tag )) 
  
  const borderWidth = highlightImage ? "5px" : "0px"

  const borderColor = (stage.get("name") == "choice" || stage.get("name") == "example-choice") ? "black" : round.get("target") == tag ? "green" : "red"

  return (
    <div style = {{width: "200px", border: "solid " + `${borderWidth}` + " " + `${borderColor}`, padding: '2px'}}>
    <img className = 'cursor-pointer' onClick = {handleClick} src={'../../img/' + tag + '.png'} />
    </div>
  );
}
