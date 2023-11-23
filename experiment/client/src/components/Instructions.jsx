import React from "react";
import { useRound, usePlayer } from "@empirica/core/player/classic/react";
import { Button } from '../components/Button'

export function Instructions() {
  const round = useRound();
  const player = usePlayer();
  const title = round.get("instructions") == "train" ? 'Phase 1: Memorization' :
    round.get("instructions") == "recall" ? 'Phase 2: Recall' :
    round.get("instructions") == "choice" ? 'Phase 3: Choice' : null;
  const li1 = round.get("instructions") == "train" ? `In this phase, you will see a series of images. Each image has a corresponding label.` :
    round.get("instructions") == "recall" ? `In this phase, you will see the same images from the previous phase, without their corresponding labels.` :
    round.get("instructions") == "choice" & player.get("role") == 'director' ? `You are the director. In each round of this phase, you will see a set of four images, one of which is highlighted.` :
    round.get("instructions") == "choice" & player.get("role") == 'guesser' ? `You are the ${<strong>guesser</strong>}. In each round of this last phase, you will see a set of four images. The other participant (the director), has one of these images highlighted.` : null;
  const li2 = round.get("instructions") == "train" ? `Memorize the label for each image to the best of your ability.` :
    round.get("instructions") == "recall" ? `Correctly label each image to the best of your ability.` :
    round.get("instructions") == "choice" & player.get("role") == 'director' ? `You need to communicate to the other participant, the guesser, which image is the target.` :
    round.get("instructions") == "choice" & player.get("role") == 'guesser' ? `You need to communicate with the other participant to figure out which image is the target. Once you have determined the target, click on it.` : null;
  const li3 = round.get("instructions") == "train" ? `Once you have memorized the label for one image, click continue to move to the next.` :
    round.get("instructions") == "recall" ? `Once you have labelled one image, click submit to move to the next.` :
    round.get("instructions") == "choice" & player.get("role") == 'director' ? `To speak to the other participant, click join to join an audio call.` :
    round.get("instructions") == "choice" & player.get("role") == 'guesser' ? `To speak to the other participant, click join to join an audio call.` : null;

  return (
    <div className="mt-3 sm:mt-5 p-50">
      <h2><strong>{title}</strong></h2>
      <ul className="list-disc list-inside">
        <li> {li1} </li>
        <li> {li2} </li>
        <li> {li3} </li>
      </ul>
    </div>
  );
}