import React from "react";
import { usePlayer, usePlayers, useRound, useStage } from "@empirica/core/player/classic/react";
import { RefGameImage } from "../components/RefGameImage";

export function ExampleOptions() {
    const player = usePlayer();
    const round = useRound();
    const players = usePlayers();
    const stage = useStage(); 
  
    function onClick(choice) {
      if(player.get("role") == "guesser" & stage.get("name") == "example-choice") {
        round.set("decision", choice);
        // Guesser selection sets "submit" to "true" for all players, necessary for stage advance https://docs.empirica.ly/overview/lifecycle/customising-when-players-submit-stages
        player.stage.set("submit", true)
      }
    }

    const imgOrder = player.get("role") == "guesser" ? round.get("guesserOrder") : round.get("directorOrder")
    const label = player.get("role") == "director" ? (stage.get("name") == "example-choice" ? round.get("verb") : round.get("target")) : round.get("target")
  
    return (

        <div className="justify-center m-5">

          <table>
            <tbody>
              <tr>
              <td><RefGameImage tag={imgOrder[0]} handleClick={() => onClick(imgOrder[0])}></RefGameImage></td>
              <td><RefGameImage tag={imgOrder[1]} handleClick={() => onClick(imgOrder[1])}></RefGameImage></td>
              </tr>
              <tr>
              <td><RefGameImage tag={imgOrder[2]} handleClick={() => onClick(imgOrder[2])}></RefGameImage></td>
              <td><RefGameImage tag={imgOrder[3]} handleClick={() => onClick(imgOrder[3])}></RefGameImage></td>
              </tr>
            </tbody>
          </table>
          
          <div className="flex justify-center m-5">
            <strong className = 'text-2xl'>{label}</strong>
          </div>

        </div>

    );
  }