import React, { useState } from "react";
import { AudioTest } from "../components/AudioTest";
import { Button } from "../components/Button";

export function MicTest({ next }) {
  const [audioRecorded, setAudioRecorded] = useState(false);

  const handleAudioRecorded = (recorded) => {
    setAudioRecorded(recorded);
  };

  return (
    <div className="mt-3 sm:mt-5 p-20 w-2/3 mx-auto">
      <h3 className="text-lg leading-6 font-medium text-gray-900 text-center">
        Microphone Test
      </h3>
      <div className="mt-2 mb-6">
        <p className="text-sm text-gray-500 text-center">
          The task relies on a working microphone and speaker.
        </p>
      </div>
      <div className="mt-2 mb-6">
        <p>
          Record audio to check that you microphone is working. Make sure you have a working microphone and audio output source (preferably headphones), and that you are in a private and quiet space.
        </p>
      </div>
      <AudioTest onAudioRecorded={handleAudioRecorded} />
      {audioRecorded && (<div className = 'flex justify-center mt-2 mb-6'>
        <Button handleClick={next} autoFocus>Next</Button></div>
      )}
    </div>
  );
}