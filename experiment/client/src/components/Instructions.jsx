import React from "react";
import { useRound, usePlayer } from "@empirica/core/player/classic/react";
import { Button } from '../components/Button'

export function Instructions() {
  const round = useRound();
  const player = usePlayer();
  const title = round.get("instructions") == "train" ? 'Phase 1: Memorization' :
    round.get("instructions") == "recall" ? 'Phase 2: Recall' :
    round.get("instructions") == "example" ? 'Phase 3: Choice (Examples)' :
    round.get("instructions") == "choice" ? 'Phase 3: Choice' : null;
  const li1 = round.get("instructions") == "train" ? `In this phase, you will see a series of images. Each image has a corresponding label.` :
    round.get("instructions") == "recall" ? `In this phase, you will see the same images from the previous phase, without their corresponding labels.` :
    (round.get("instructions") == "choice" || round.get("instructions") == "example") & player.get("role") == 'director' ? <span>You are the <b>director</b>. In each round of this phase, you will see a verb and a set of four images (one is highlighted).</span> :
    (round.get("instructions") == "choice" || round.get("instructions") == "example") & player.get("role") == 'guesser' ? <span>You are the <b>guesser</b>. In each round of this last phase, you will see four images. The other participant has one of these images highlighted.</span> : null;
  const li2 = round.get("instructions") == "train" ? `Memorize the label for each image to the best of your ability.` :
    round.get("instructions") == "recall" ? `Correctly label each image to the best of your ability.` :
    round.get("instructions") == "example" & player.get("role") == 'director' ? <span>You need to communicate to the other participant which image is the target using <b>full sentences and the target verb.</b></span> :
    round.get("instructions") == "example" & player.get("role") == 'guesser' ? <span>You need to communicate with the other participant to figure out which image is the target. Once you have determined the target, click on it.</span> :
    round.get("instructions") == "choice" & player.get("role") == 'director' ? <span>Your partner will see the same images in a <b>different order.</b></span> :
    round.get("instructions") == "choice" & player.get("role") == 'guesser' ? <span>Your partner will see the same images in a <b>different order.</b></span> : null;
  const li3 = round.get("instructions") == "train" ? `Your partner will see and memorize the same labels.` :
    round.get("instructions") == "recall" ? `Use the specific labels you saw in the previous round.` :
    round.get("instructions") == "example" & player.get("role") == 'director' ? `You will first be shown two stimuli with examples of a valid full sentence description using the target verb.` :
    round.get("instructions") == "example" & player.get("role") == 'guesser' ? `You will first be shown two stimuli with examples of a valid full sentence description using the target verb.` :
    round.get("instructions") == "choice" & player.get("role") == 'director' ? <span>You need to communicate to the other participant which image is the target using <b>full sentences and the target verb.</b></span> :
    round.get("instructions") == "choice" & player.get("role") == 'guesser' ? <span>You need to communicate with the other participant to figure out which image is the target. Once you have determined the target, click on it.</span> : null;
  const li4 = round.get("instructions") == "train" ? `Once you have memorized the label for one image, click continue to move to the next.` :
    round.get("instructions") == "recall" ? `Once you have labelled one image, click submit to move to the next.` :
    round.get("instructions") == "example" & player.get("role") == 'director' ? `In the real task, you will be in an audio call with the other participant.` :
    round.get("instructions") == "example" & player.get("role") == 'guesser' ? `In the real task, you will be in an audio call with the other participant.` :
    round.get("instructions") == "choice" & player.get("role") == 'director' ? `You and your partner will be in an audio call throughout this phase. You should first describe the image in one sentence to your partner.` :
    round.get("instructions") == "choice" & player.get("role") == 'guesser' ? `You and your partner will be in an audio call throughout this phase. Wait for your partner to first describe the image before you speak to them.` : null;

  return (
    <div className="mt-3 sm:mt-5 p-50">
      <h2 className = "text-center text-lg mb-2"><strong>{title}</strong></h2>
      <p className = "text-center text-sm mb-2 text-red-500 font-bold">Read these instructions carefully.</p>
      <ul className="list-disc list-inside">
        <li> {li1} </li>
        <li> {li2} </li>
        <li> {li3} </li>
        <li> {li4} </li>
      </ul>
    </div>
  );
}