import React, { useState } from "react";
import { Button } from "../components/Button";

const base =
  "inline-flex flex-col items-center px-4 py-2 border text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-empirica-500 m-5";

export function SpeakerTest({ next }) {
  const [userInput, setUserInput] = useState('');
  const correctAnswer = 'purple dinosaur'; // Replace with the actual correct answer
  const [isCorrect, setIsCorrect] = useState(false);
  const [showError, setShowError] = useState(false);

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
    setShowError(false); // Reset error message when user starts typing
  };

  const checkAnswer = () => {
    if (userInput.trim().toLowerCase() === correctAnswer.toLowerCase()) {
      setIsCorrect(true);
      setShowError(false);
    } else {
      setIsCorrect(false);
      setShowError(true); // Show error message for incorrect submission
    }
  };

  return (
    <div className="mt-3 sm:mt-5 p-20 w-2/3 mx-auto">
      <h3 className="text-lg leading-6 font-medium text-gray-900 text-center">
        Speaker Test
      </h3>
      <div className="mt-2 mb-6">
        <p className="text-sm text-gray-500 text-center">
          The task relies on a working microphone and speaker.
        </p>
      </div>
      <div className="mt-2 mb-6">
        <p>
          Play back the audio file below, and type what you hear. Make sure that you have a working audio output source (preferably headphones).
        </p>
      </div>
      <div className = 'text-center'>
        <audio className = {base} controls>
          <source src="../../public/test_audio.m4a" type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      </div>
      <div className="flex justify-center mt-2 mb-2">
        <table>
          <tr>
            <td>
            <input
              type="text"
              value={userInput}
              onChange={handleInputChange}
              placeholder="Enter what you heard"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  checkAnswer();
                }
              }}
            />
            </td>
            <td>
            {isCorrect ? (
              <Button handleClick={next} autoFocus>Next</Button>
            ) : (
              <Button handleClick={checkAnswer} autoFocus>Submit</Button>
            )}
            </td>
          </tr>
        </table>
      </div>
      <div className = 'flex justify-center mt-2 mb-6'>
        {showError && <p className="text-red-500 font-bold">Sorry, please check your speaker and try again!</p>}
      </div>
      {isCorrect && (<div className = 'flex justify-center mt-2 mb-6'>
        <p className="text-green-500 font-bold">Perfect, please continue!</p>
        </div>
      )}
    </div>
  );
}