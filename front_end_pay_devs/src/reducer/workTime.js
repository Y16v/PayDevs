
import { workTimeConstant } from "../constants/workTime";

const initialStateHour = {};

export function workTime(state = initialStateHour, action) {
  switch(action.type) {
    case workTimeConstant.CREATE:
      return action.workTime;
    case workTimeConstant.GET:
      return action.workTime;
    default:
      return state;
  }
}

const initialStateworkTimes = [];

export function workTimes(state = initialStateworkTimes, action) {
  switch(action.type) {
    case workTimeConstant.GET_ALL:
      return action.workTimes;
    case workTimeConstant.DELETE:
      return state.filter(workTime=>workTime.id !== action.workTime.id);
    default:
      return state;
  }
}