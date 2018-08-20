import React from "react";
import { withFormik, Form, Field } from "formik";
import DateTimePicker from "react-datetime-picker";

const WorkInput = ({ values, errors, touched, setFieldValue }) => {
  return (
    <Form className="form-group" style={{ margin: 10 }}>
      <label>Title: </label>
      <label>Start-work: </label>
      <div>
        {touched.start_date && errors.start_date && <p>{errors.start_date}</p>}
      </div>
      <div>
        <DateTimePicker
          name="start_date"
          type="datetime"
          value={values.start_date}
          onChange={value => setFieldValue("start_date", value)}
        />
      </div>

      <label>End-work: </label>
      <div>
        {touched.end_date && errors.end_date && <p>{errors.end_date}</p>}
      </div>
      <div>
        <DateTimePicker
          name="end_date"
          type="datetime"
          value={values.end_date}
          onChange={value => setFieldValue("end_date", value)}
        />
      </div>
      <label>
        Paid:
        <Field name="paid" type="checkbox" checked={values.status} />
      </label>

      <button className="btn btn-primary form-control" type="submit">
        submit
      </button>
    </Form>
  );
};

const FormikProject = withFormik({
  mapPropsToValues({
    id,
    projectId,
    hourPaymentId,
    start_work,
    end_work,
    paid
  }) {
    return {
      id: id || null,
      start_work: (start_work ) || new Date(),
      end_work: (end_work ) || new Date(),
      projectId: projectId,
      hourPaymentId: hourPaymentId,
      paid: paid,
      

    };
  },
  handleSubmit(values, { props }) {
    props.onSubmit(values);
  }
})(WorkInput);

export default FormikProject;
