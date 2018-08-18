import workedDayActionTypes from "../constants/workedDay";

const initialState = [];

export default function workedDays(state = initialState, action) {
  switch (action.type) {
    case workedDayActionTypes.ADD_ALL_WORKED_DAYS:
      return [...action.workedDays];
    case workedDayActionTypes.CREATE_WORKED_DAY:
      return state.concat([action.workedDay]);
    case workedDayActionTypes.REMOVE_WORKED_DAY:
      return state.filter(workedDay => workedDay.id !== action.workedDayId)
    default:
      return state;
  }
}
