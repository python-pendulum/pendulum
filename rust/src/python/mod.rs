use pyo3::prelude::*;

mod helpers;
mod parsing;
mod types;

use helpers::{days_in_year, is_leap, is_long_year, local_time, precise_diff, week_day};
use parsing::parse_iso8601;
use types::{Duration, PreciseDiff};

#[pymodule]
pub fn _pendulum(_py: Python<'_>, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(days_in_year, m)?)?;
    m.add_function(wrap_pyfunction!(is_leap, m)?)?;
    m.add_function(wrap_pyfunction!(is_long_year, m)?)?;
    m.add_function(wrap_pyfunction!(local_time, m)?)?;
    m.add_function(wrap_pyfunction!(week_day, m)?)?;
    m.add_function(wrap_pyfunction!(parse_iso8601, m)?)?;
    m.add_function(wrap_pyfunction!(precise_diff, m)?)?;
    m.add_class::<Duration>()?;
    m.add_class::<PreciseDiff>()?;

    Ok(())
}
