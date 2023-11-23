import { ClassicListenersCollector } from "@empirica/core/admin/classic";
import axios from 'axios';
import _ from 'underscore';
const fs = require("fs");

export const Empirica = new ClassicListenersCollector();

Empirica.on("batch", "status", (ctx, { batch, status }) => {
  
  console.log(`Batch ${batch.id} changed status to "${status}"`);
  const treatment = batch.games[0].get("treatment")
  const { managementToken, templateId } = treatment;

  const axiosInstance = axios.create({
    baseURL: 'https://api.100ms.live/v2/',
    headers: {
      'Authorization': 'Bearer ' + managementToken,
      'Content-Type': 'application/json',
    },
  });

  if (status === "running") {
    batch.games.forEach((game, i) => {
          
      const createRoomCode = async () => {
        try {
          const getRoom = await axiosInstance.post('rooms', {
            name: game.id,
            description: 'audio call room',
            template_id: templateId,
            region: 'us',
            recording_info: {
              enabled: true
            },  
          });
      
          const roomId = getRoom.data.id;
          const getCode = await axiosInstance.post(`room-codes/room/${roomId}`);
          const roomCode = String(getCode.data.data[0].code)

          game.set("roomCode", roomCode)

        } catch (error) {
          console.error('Error creating room and getting guest code:', error);
          throw error;
        }
      }
    
      createRoomCode();

      console.log('All rooms created, and all roomCodes set!')
    });
  }
});

Empirica.onGameStart(({ game }) => {

  game.set("timestamps", [])

  const treatment = game.get("treatment")
  const { condition } = treatment;

  const roleList = _.shuffle(['director','guesser'])
  game.players.forEach((player, i) => {
		player.set("role", roleList[i]);
  });

  game.players.forEach((player, i) => {
    player.set("roomCode", game.get("roomCode"));
  });

  console.log(`Game ${game.id} initialized, all players are assigned roomCodes...`)

  const csv=require('csvtojson');

  const stims = csv()
  .fromFile(`./src/stims-${condition}.csv`)
  .then((jsonObj)=>{
      return(jsonObj);
  })

  let roundCounter = 1;
  stims.map(function(stim) {
    if (stim.phase == 'train') {
      if (stim.trialid == 1) {
        roundCounter = 1
        const instructRound = game.addRound({
          name: `Instructions for Phase 1: Memorization`,
          instructions: 'train'
        });
        instructRound.addStage({ name: "instructions", duration: 10000 })
      }
      const round = game.addRound({
        name: `Round ${roundCounter}`,
        label: stim.label,
        instructions: null
      });
      round.addStage({ name: "train", duration: 10000 });
      roundCounter++; 
    }
    if (stim.phase == 'recall') {
      if (stim.trialid == 1) {
        const instructRound = game.addRound({
          name: `Instructions for Phase 2: Recall`,
          instructions: 'recall'
        });
        instructRound.addStage({ name: "instructions", duration: 10000 })
      }
      const round = game.addRound({
        name: `Round ${roundCounter}`,
        label: stim.label,
        instructions: null
      });
      round.addStage({ name: "recall", duration: 10000 });
      roundCounter++; 
    }
    if (stim.phase == 'example') {
      if (stim.trialid == 1) {
        const instructRound = game.addRound({
          name: `Instructions for Phase 3: Choice`,
          instructions: 'choice'
        });
        instructRound.addStage({ name: "instructions", duration: 10000 })
      }
      const round = game.addRound({
        name: `Round ${roundCounter}`,
        target: stim.target,
        images: stim.images.split(","),
        verb: stim.verb,
        guesserOrder: _.shuffle(stim.images.split(",")),
        directorOrder: _.shuffle(stim.images.split(",")),
        instructions: null
      });
      round.addStage({ name: "example-choice", duration: 10000 });
      round.addStage({ name: "example-result", duration: 10000 });
      roundCounter++;
    }
    if (stim.phase == 'choice') {
      if (stim.trialid == 1) {
        const instructRound = game.addRound({
          name: `Instructions for Phase 3: Choice`,
          instructions: 'choice'
        });
        instructRound.addStage({ name: "instructions", duration: 10000 })
      }
      const round = game.addRound({
        name: `Round ${roundCounter}`,
        target: stim.target,
        images: stim.images.split(","),
        verb: stim.verb,
        guesserOrder: _.shuffle(stim.images.split(",")),
        directorOrder: _.shuffle(stim.images.split(",")),
        instructions: null
      });
      round.addStage({ name: "choice", duration: 10000 });
      round.addStage({ name: "result", duration: 10000 });
      roundCounter++;
    }
  })
});

Empirica.onRoundStart(({ round }) => {
  console.log(round.get("name"))
  const cur_date = new Date();
  const old_timestamps = round.currentGame.get("timestamps")
  old_timestamps.push(cur_date)
  round.currentGame.set("timestamps", old_timestamps)  
});

Empirica.onStageStart(({ stage }) => {});

Empirica.onStageEnded(({ stage }) => {});

Empirica.onRoundEnded(({ round }) => {});

Empirica.onGameEnded(({ game }) => {});