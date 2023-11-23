import React from "react";
import { usePlayer, useRound, useStage } from "@empirica/core/player/classic/react";
import { ReactMic } from 'react-mic';
import { Button } from '../components/Button'

export class MicTest extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      record: false,
      text: 'Start'
    }
  }
 
  startRecording = () => {
    if (this.state.record == true) {
      this.setState({ record: false, text: 'Start'});
    }
    else if (this.state.record == false) {
      this.setState({ record: true, text: 'Stop'});
    }
  }
 
  onData(recordedBlob) {
    console.log('chunk of real-time data is: ', recordedBlob);
  }
 
  onStop(recordedBlob) {
    console.log('recordedBlob is: ', recordedBlob);
  }
 
  render() {
    return (
      <div>
        <Button handleClick={this.startRecording}> {this.state.text} </Button>
        <ReactMic
          record={this.state.record}
          className="frequencyBars"
          onStop={this.onStop}
          onData={this.onData}
          strokeColor="#000000"
          backgroundColor="#FFFFFF" />
      </div>
    );
  }
}