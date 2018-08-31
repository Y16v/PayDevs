import React, { Component } from "react";
import { connect } from "react-redux";

import workTimeActions from "../../actions/workTime";
import WorkTime from "./WorkTime";
import FormikWorkTime from "../../forms/FormikWorkTime";

class WorkTimes extends Component {
  componentWillMount() {
    let { workTimes, getAllWorkTimes } = this.props;
    let hourPaymentId = +this.props.match.params.hourPaymentId;

    if (!workTimes.length || workTimes[0].hourPaymentId !== hourPaymentId)
      getAllWorkTimes(hourPaymentId);
  }

  render() {
    const { workTimes, createWorkTime, removeWorkTime } = this.props;

    return (
      <div>
        {workTimes.length > 0 && (
          <h3 className="workedHoursHeader">
            <b>Your Worked Hours</b>
          </h3>
        )}
        <div>
          {workTimes.map(workTime => (
            <WorkTime
              key={workTime.id}
              workTime={workTime}
              projectId={+this.props.match.params.id}
              hourPaymentId={+this.props.match.params.hourPaymentId}
              onRemove={removeWorkTime}
            />
          ))}
        </div>

        <h3>
          <b>Create a new Work Time</b>
        </h3>
        <FormikWorkTime
          onSubmit={createWorkTime}
          projectId={+this.props.match.params.id}
          hourPaymentId={+this.props.match.params.hourPaymentId}
        />
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    workTimes: state.workTimes
  };
};

const mapDispatchToProps = dispatch => {
  return {
    getAllWorkTimes: hourPaymentId =>
      dispatch(workTimeActions.getAll(hourPaymentId)),
    removeWorkTime: workTimeId => {
      dispatch(workTimeActions.remove(workTimeId));
    },
    createWorkTime: values => {
      dispatch(workTimeActions.create(values));
    }
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(WorkTimes);
