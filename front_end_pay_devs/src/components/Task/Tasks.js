import React, { Component } from "react";
import { connect } from "react-redux";

import { tasklyActions } from "../../actions/taskly";
import TaskItem from "./TaskItem";
import CreateTask from "./CreateTask";

class Tasks extends Component {
  componentDidMount() {
    this.props.getAllTasks(this.props.projectId);
  }

  render() {
    const { tasks, projectId } = this.props;

    return (
      <div>
        {tasks.length > 0 && <h2>Your tasks</h2>}

        <div>
          {tasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onDelete={this.props.removeTask}
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
