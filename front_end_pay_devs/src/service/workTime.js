import axios from "axios";
import { authHeader } from "./helpers";
import { API_URL } from "../constants/host";

export const workTimeService = {
  create,
  getAll,
  remove,
  update
};

function create(values) {
  const headres = authHeader();
  const fetch_url = `${API_URL}project/${values.projectId}/hour_payment/${
    values.hourPaymentId
  }/work_time/create`;
  return axios({
    method: "post",
    url: fetch_url,
    headers: headres,
    data: values
  }).then(res => {
    return res.data;
  });
}

function getAll(hourPaymentId) {
  let headers = authHeader();
  return axios({
    method: "get",
    url: `${API_URL}project/hour_payment/${hourPaymentId}/work_time/all`,
    headers: headers
  }).then(res => {
    let projects = res.data;
    return projects;
  });
}

function remove(workTimeId) {
  let headers = authHeader();
  return axios({
    method: "delete",
    url: `${API_URL}project/work_time/${workTimeId}/delete`,
    headers: headers
  }).then(res => {
    let task = res.data;
    return task;
  });
}

function update(projectId, hourPaymentId, workTimeId, values) {
  const headres = authHeader();
  const fetch_url = `${API_URL}project/${projectId}/hour_payment/${hourPaymentId}/work_time/${workTimeId}/update`;
  return axios({
    method: "put",
    url: fetch_url,
    headers: headres,
    data: values
  }).then(res => {
    let updatedWorkTime = res.data;
    return updatedWorkTime;
  });
}