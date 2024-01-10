import React from "react";
import { Button } from "../components/Button";

export function Introduction({ next }) {
  return (
    <div className="mt-3 sm:mt-5 p-20 w-2/3 mx-auto">
      <h3 className="text-xl leading-6 font-bold text-gray-900 text-center">
        Instructions
      </h3>
      <div className="mt-2 mb-6">
        <p>
          This game has three parts. You will be paired up with another participant for all three parts. For each round, you and your partner must both complete the round before moving to the next one together (even for tasks where you are not directly interacting).
        </p>
        <br></br>
        <ul className = 'list-disc list-inside'>
          <li> Stage One: <strong>Memorize</strong> the names of some objects. </li>
          <li> Stage Two: <strong> Test </strong> your memory of the names you just learned. </li>
          <li> Stage Three: <strong> Communicate </strong> with your partner about some images, using the names you just learned. </li>
        </ul>
        <br></br>
        <p>First, we need to test your mic and speaker.</p>
        {/*<h4 className="text-lg leading-6 font-medium text-gray-900">
          Stage One:
        </h4>
        <ul class = 'list-disc list-inside'>
          <li> In this stage, you will be shown a series of images, each with a label </li>
          <li> Your goal is to <strong>memorize</strong> which label corresponds to which image </li>
        </ul>
        <br></br>
        <h4 className="text-lg leading-6 font-medium text-gray-900">
          Stage Two:
        </h4>
        <ul class = 'list-disc list-inside'>
          <li> In this stage, you will be shown the same images as the previous stage, in a random order</li>
          <li> Your task is to <strong>identify</strong> the images using the labels you learned </li>
        </ul>
        <br></br>
        <h4 className="text-lg leading-6 font-medium text-gray-900">
          Stage Three:
        </h4>
        <ul class = 'list-disc list-inside'>
          <li> In this stage, you will be assigned a role: either the <strong>director</strong> or the <strong>guesser</strong></li>
          <li> You will be shown four images. If you are the director, one of these will be labeled as the <strong>target</strong> </li>
          <li> You will join an audio call with your partner. The <strong>director</strong> should describe the target image to the guesser. </li>
          <li> Your goal as a team is to correctly identify the target image. </li>
        </ul>*/}
      </div>
      <div className = "flex justify-center">
        <Button handleClick={next} autoFocus>
          <p>Next</p>
        </Button>
      </div>
    </div>
  );
}