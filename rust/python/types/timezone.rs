use pyo3::prelude::*;
use pyo3::types::{PyDateTime, PyDelta, PyTzInfo};

#[pyclass(module = "_pendulum", extends = PyTzInfo)]
pub struct FixedTimezone {
    offset: i32,
    name: Option<String>,
}

#[pymethods]
impl FixedTimezone {
    #[new]
    pub fn new(offset: i32, name: Option<String>) -> Self {
        Self { offset, name }
    }

    fn utcoffset<'p>(&self, py: Python<'p>, _dt: &PyDateTime) -> PyResult<&'p PyDelta> {
        PyDelta::new(py, 0, self.offset, 0, true)
    }

    fn tzname(&self, _dt: &PyDateTime) -> String {
        self.__str__()
    }

    fn dst<'p>(&self, py: Python<'p>, _dt: &PyDateTime) -> PyResult<&'p PyDelta> {
        PyDelta::new(py, 0, 0, 0, true)
    }

    fn __repr__(&self) -> String {
        format!(
            "FixedTimezone({}, name=\"{}\")",
            self.offset,
            self.__str__()
        )
    }

    fn __str__(&self) -> String {
        match self.name.clone() {
            Some(n) => n,
            None => {
                let sign = if self.offset < 0 { "-" } else { "+" };
                let minutes = self.offset / 60;
                let (hour, minute) = (minutes.abs() / 60, minutes.abs() % 60);
                format!("{}{:.2}:{:.2}", sign, hour, minute)
            }
        }
    }
}
