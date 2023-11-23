import React from "react";
import { Button } from "../components/Button";
import { ReactMic } from 'react-mic';
import { MicTest } from "../components/MicTest";

export function MicInstructions({ next }) {
  return (
    <div className="mt-3 sm:mt-5 p-20">
      <div className="mt-2 mb-6">
        <p className="text-sm text-gray-500">
          As part of this game, you will be required to record and listen to audio. By continuing, you approve use of the anonymized recorded audio for research purposes.
        </p>
        <br></br>
        <p>
          Make sure you have a working microphone and audio output source (preferably headphones), and that you are in a private and quiet space.
        </p>
        <br></br>
        <p>
          Before continuing, test your mic below. Click <strong>start</strong> to record audio, and <strong>play</strong> to play back the recorded audio.
        </p>
      </div>
      <div>
        <MicTest />
        <Button handleClick={next} autoFocus>
          <p>Next</p>
        </Button>
      </div>
    </div>
  );
}