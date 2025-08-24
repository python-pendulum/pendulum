#![allow(clippy::useless_conversion)]
use pyo3::exceptions;
use pyo3::prelude::*;
use pyo3::types::PyDate;
use pyo3::types::PyDateTime;
use pyo3::types::PyTime;
use pyo3::IntoPyObjectExt;

use crate::parsing::Parser;
use crate::python::types::{Duration, FixedTimezone};

#[pyfunction]
pub fn parse_iso8601(py: Python, input: &str) -> PyResult<PyObject> {
    let parsed = Parser::new(input).parse();

    match parsed {
        Ok(parsed) => match (parsed.datetime, parsed.duration, parsed.second_datetime) {
            (Some(datetime), None, None) => match (datetime.has_date, datetime.has_time) {
                (true, true) => match datetime.offset {
                    Some(offset) => {
                        let dt = PyDateTime::new(
                            py,
                            datetime.year as i32,
                            datetime.month as u8,
                            datetime.day as u8,
                            datetime.hour as u8,
                            datetime.minute as u8,
                            datetime.second as u8,
                            datetime.microsecond,
                            Some(
                                Py::new(py, FixedTimezone::new(offset, datetime.tzname))?
                                    .into_any()
                                    .downcast_bound(py)?,
                            ),
                        )?;

                        Ok(dt.into_any().unbind())
                    }
                    None => {
                        let dt = PyDateTime::new(
                            py,
                            datetime.year as i32,
                            datetime.month as u8,
                            datetime.day as u8,
                            datetime.hour as u8,
                            datetime.minute as u8,
                            datetime.second as u8,
                            datetime.microsecond,
                            None,
                        )?;

                        Ok(dt.into_any().unbind())
                    }
                },
                (true, false) => {
                    let dt = PyDate::new(
                        py,
                        datetime.year as i32,
                        datetime.month as u8,
                        datetime.day as u8,
                    )?;

                    Ok(dt.into_any().unbind())
                }
                (false, true) => match datetime.offset {
                    Some(offset) => {
                        let dt = PyTime::new(
                            py,
                            datetime.hour as u8,
                            datetime.minute as u8,
                            datetime.second as u8,
                            datetime.microsecond,
                            Some(
                                Py::new(py, FixedTimezone::new(offset, datetime.tzname))?
                                    .into_any()
                                    .downcast_bound(py)?,
                            ),
                        )?;

                        Ok(dt.into_any().unbind())
                    }
                    None => {
                        let dt = PyTime::new(
                            py,
                            datetime.hour as u8,
                            datetime.minute as u8,
                            datetime.second as u8,
                            datetime.microsecond,
                            None,
                        )?;

                        Ok(dt.into_any().unbind())
                    }
                },
                (_, _) => Err(exceptions::PyValueError::new_err(
                    "Parsing error".to_string(),
                )),
            },
            (None, Some(duration), None) => Ok(Py::new(
                py,
                Duration::new(
                    Some(duration.years),
                    Some(duration.months),
                    Some(duration.weeks),
                    Some(duration.days),
                    Some(duration.hours),
                    Some(duration.minutes),
                    Some(duration.seconds),
                    Some(duration.microseconds),
                ),
            )?
            .into_py_any(py)?),
            (_, _, _) => Err(exceptions::PyValueError::new_err(
                "Not yet implemented".to_string(),
            )),
        },
        Err(error) => Err(exceptions::PyValueError::new_err(error.to_string())),
    }
}
