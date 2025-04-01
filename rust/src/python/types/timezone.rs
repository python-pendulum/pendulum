#![allow(clippy::useless_conversion)]
use pyo3::prelude::*;
use pyo3::types::{PyDelta, PyDict, PyTzInfo};

#[pyclass(module = "_pendulum", extends = PyTzInfo)]
#[derive(Clone)]
pub struct FixedTimezone {
    offset: i32,
    name: Option<String>,
}

#[pymethods]
impl FixedTimezone {
    #[new]
    #[pyo3(signature = (offset, name=None))]
    pub fn new(offset: i32, name: Option<String>) -> Self {
        Self { offset, name }
    }

    fn utcoffset<'p>(
        &self,
        py: Python<'p>,
        _dt: &Bound<'p, PyAny>,
    ) -> Result<pyo3::Bound<'p, PyDelta>, PyErr> {
        PyDelta::new(py, 0, self.offset, 0, true)
    }

    fn tzname(&self, _dt: &Bound<PyAny>) -> String {
        self.__str__()
    }

    fn dst<'p>(
        &self,
        py: Python<'p>,
        _dt: &Bound<'p, PyAny>,
    ) -> Result<pyo3::Bound<'p, PyDelta>, PyErr> {
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
        if let Some(n) = &self.name {
            n.clone()
        } else {
            let sign = if self.offset < 0 { "-" } else { "+" };
            let minutes = self.offset.abs() / 60;
            let (hour, minute) = (minutes / 60, minutes % 60);
            format!("{sign}{hour:.2}:{minute:.2}")
        }
    }

    fn __deepcopy__(&self, py: Python, _memo: &Bound<PyDict>) -> PyResult<Py<Self>> {
        Py::new(py, self.clone())
    }
}
