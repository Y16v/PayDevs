import React, { Component } from "react";
import { connect } from "react-redux";

import { tasklyActions } from "../../actions/task";
import TaskItem from "./TaskItem";
import CreateTask from "./CreateTask";

class Tasks extends Component {
  componentDidMount() {
    if (!this.props.tasks.length) this.props.getAllTasks(this.props.projectId);
  }

  render() {
    const { tasks, projectId, removeTask } = this.props;

    return (
      <div>
        {tasks.length > 0 && <h3 className="taskHeader">Your tasks</h3>}

        <div>
          {tasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onDelete={removeTask}
              projectId={projectId}
            />
          ))}
        </div>

        <hr />

        <CreateTask projectId={projectId} />
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    tasks: state.tasks
  };
};

const mapDispatchToProps = dispatch => {
  return {
    getAllTasks: projectId => {
      dispatch(tasklyActions.getAll(projectId));
    },
    removeTask: taskId => {
      dispatch(tasklyActions.remove(taskId));
    }
  };
};

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Tasks);
