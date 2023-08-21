var target = "teacher student book"

// how informative is the alternation?
var informativity = dataFromR[0].informativity
var numstates = informativity == 'high' ? 6 :
                informativity == 'med' ? 4 :
                informativity == 'low' ? 2 : 1

// which type of alternation (T/R)?
var alternation = 'R'

// cost?
var useCost = true
var recipientcost = dataFromR[0].recipientcost

// priors?
var usePriors = true
var recipientprior = dataFromR[0].recipientprior

// generate all alternative states
var toDict = function(x){ return {string: x} }

var getStates = function(states, numstates) {
  var numstatesprime = numstates - 1
  if (numstatesprime != 0 && alternation == 'T') {
    var newstates = (states + ',teacher student Alt' + numstatesprime).split(',');
    getStates(newstates, numstatesprime)
  } else if (numstatesprime != 0 && alternation == 'R') {
    var newstates = (states + ',teacher Alt' + numstatesprime + ' book').split(',');
    getStates(newstates, numstatesprime)
  } else {
    return map(toDict, states)
  }
}

// generate all utterances
var getUtts = function(states, numstates) {
  var numstatesprime = numstates - 1
  if (numstatesprime != 0) {
    var newstates = (states + ',Alt' + numstatesprime).split(',')
    getUtts(newstates, numstatesprime)
  } else {
    return states
  }
}

// creates states, utterances
var states = getStates(target, numstates)
var utterances = getUtts('student,book', numstates)

// prior over world states
var objectPrior = function() {
  var obj = uniformDraw(states)
  return obj.string 
}

var cost = function(utt){
  useCost ? (utt == "book" ? recipientcost :
  utt == "student" ? 0.25 : 0) : 0
}

var prior = function(utt){
  usePriors ? (utt == "book" ? recipientprior :
  utt == "student" ? 0.25 : 0) : 0
}

// meaning function to interpret the utterances
var meaning = function(utterance, obj){
  _.includes(obj, utterance)
}

// literal listener
var literalListener = function(utterance){
  Infer({model: function(){
    var obj = objectPrior();
    var uttTruthVal = meaning(utterance, obj);
    condition(uttTruthVal == true)
    return obj
  }})
}

// set speaker optimality
var alpha = 5

var util = function(utterance, obj) {
  alpha * (literalListener(utterance).score(obj) - cost(utterance))
}

// pragmatic speaker
var speaker = function(obj) {
  Infer({model: function(){
    var utterance = uniformDraw(utterances)
    factor(alpha * (literalListener(utterance).score(obj) - cost(utterance)))
    return utterance
  }})
}

var getProbs = function(obj, utt1, utt2) {
  var utt1score = Math.exp(speaker(obj).score(utt1)) // 0.33
  var utt2score = Math.exp(speaker(obj).score(utt2)) // 0.66
  var a = usePriors ? Math.exp(utt1score) * prior(utt1) : Math.exp(utt1score)
  var b = usePriors ? Math.exp(utt2score) * prior(utt2) : Math.exp(utt2score)
  return [a/(a+b), b/(a+b)]
}

getProbs('teacher student book', 'book', 'student')