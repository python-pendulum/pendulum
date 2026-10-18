#![allow(clippy::useless_conversion)]
use std::cmp::Ordering;

use pyo3::{
    prelude::*,
    types::{PyDate, PyDateAccess, PyDateTime, PyDelta, PyDeltaAccess, PyString, PyTimeAccess},
    PyTypeInfo,
};

use crate::{
    constants::{DAYS_PER_MONTHS, SECS_PER_DAY, SECS_PER_HOUR, SECS_PER_MIN},
    helpers,
};

use crate::python::types::PreciseDiff;

struct DateTimeInfo<'py> {
    pub year: i32,
    pub month: i32,
    pub day: i32,
    pub hour: i32,
    pub minute: i32,
    pub second: i32,
    pub microsecond: i32,
    pub total_seconds: i32,
    pub offset: i32,
    pub tz: &'py str,
    pub is_datetime: bool,
}

impl DateTimeInfo<'_> {
    /// Subtract the UTC offset from the wall-clock fields,
    /// carrying over into the day, month and year as needed.
    fn shift_to_utc(&mut self) {
        let seconds =
            self.hour * SECS_PER_HOUR as i32 + self.minute * SECS_PER_MIN as i32 + self.second
                - self.offset;
        let day_shift = seconds.div_euclid(SECS_PER_DAY as i32);
        let seconds = seconds.rem_euclid(SECS_PER_DAY as i32);

        self.hour = seconds / SECS_PER_HOUR as i32;
        self.minute = seconds % SECS_PER_HOUR as i32 / SECS_PER_MIN as i32;
        self.second = seconds % SECS_PER_MIN as i32;

        // UTC offsets are strictly less than a day,
        // so the date moves by at most one day.
        match day_shift.cmp(&0) {
            Ordering::Less => {
                self.day -= 1;

                if self.day == 0 {
                    if self.month == 1 {
                        self.month = 12;
                        self.year -= 1;
                    } else {
                        self.month -= 1;
                    }

                    self.day = DAYS_PER_MONTHS[usize::from(helpers::is_leap(self.year))]
                        [self.month as usize];
                }
            }
            Ordering::Greater => {
                self.day += 1;

                if self.day
                    > DAYS_PER_MONTHS[usize::from(helpers::is_leap(self.year))][self.month as usize]
                {
                    self.day = 1;

                    if self.month == 12 {
                        self.month = 1;
                        self.year += 1;
                    } else {
                        self.month += 1;
                    }
                }
            }
            Ordering::Equal => {}
        }
    }
}

impl PartialEq for DateTimeInfo<'_> {
    fn eq(&self, other: &Self) -> bool {
        (
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
        )
            .eq(&(
                other.year,
                other.month,
                other.day,
                other.hour,
                other.minute,
                other.second,
                other.microsecond,
            ))
    }
}

impl PartialOrd for DateTimeInfo<'_> {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        (
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
        )
            .partial_cmp(&(
                other.year,
                other.month,
                other.day,
                other.hour,
                other.minute,
                other.second,
                other.microsecond,
            ))
    }
}

pub fn get_tz_name<'py>(dt: &Bound<'py, PyAny>) -> PyResult<String> {
    // let tz: &str = "";

    if !PyDateTime::is_type_of(dt) {
        return Ok(String::new());
    }

    let tzinfo: Bound<'py, PyAny> = dt.getattr("tzinfo")?;

    if tzinfo.is_none() {
        return Ok(String::new());
    }

    let tzname_attr: Option<Bound<'py, PyAny>> = if tzinfo.hasattr("key")? {
        Some(tzinfo.getattr("key")?)
    } else if tzinfo.hasattr("name")? {
        Some(tzinfo.getattr("name")?)
    } else if tzinfo.hasattr("zone")? {
        Some(tzinfo.getattr("zone")?)
    } else {
        None
    };

    if let Some(tzname_attr) = tzname_attr {
        let tzname: &Bound<PyString> = tzname_attr.cast()?;
        tzname.extract()
    } else {
        Ok(String::new())
    }
}

pub fn get_offset(dt: &Bound<PyAny>) -> PyResult<i32> {
    if !PyDateTime::is_type_of(dt) {
        return Ok(0);
    }

    let tzinfo = dt.getattr("tzinfo")?;

    if tzinfo.is_none() {
        return Ok(0);
    }
    let binding = tzinfo.call_method1("utcoffset", (dt,))?;
    let offset: &Bound<PyDelta> = binding.cast()?;

    Ok(offset.get_days() * SECS_PER_DAY as i32 + offset.get_seconds())
}

#[pyfunction]
pub fn is_leap(year: i32) -> bool {
    helpers::is_leap(year)
}

#[pyfunction]
pub fn is_long_year(year: i32) -> bool {
    helpers::is_long_year(year)
}

#[pyfunction]
pub fn week_day(year: i32, month: u32, day: u32) -> u32 {
    helpers::week_day(year, month, day)
}

#[pyfunction]
pub fn days_in_year(year: i32) -> u32 {
    helpers::days_in_year(year)
}

#[pyfunction]
pub fn local_time(
    unix_time: f64,
    utc_offset: isize,
    microsecond: usize,
) -> (usize, usize, usize, usize, usize, usize, usize) {
    helpers::local_time(unix_time, utc_offset, microsecond)
}

#[pyfunction]
pub fn precise_diff<'py>(
    dt1: &Bound<'py, PyAny>,
    dt2: &Bound<'py, PyAny>,
) -> PyResult<PreciseDiff> {
    let mut sign = 1;
    let dt1_tz = get_tz_name(dt1)?;
    let dt2_tz = get_tz_name(dt2)?;
    let mut dtinfo1 = DateTimeInfo {
        year: dt1.cast::<PyDate>()?.get_year(),
        month: i32::from(dt1.cast::<PyDate>()?.get_month()),
        day: i32::from(dt1.cast::<PyDate>()?.get_day()),
        hour: 0,
        minute: 0,
        second: 0,
        microsecond: 0,
        total_seconds: 0,
        tz: dt1_tz.as_str(),
        offset: get_offset(dt1)?,
        is_datetime: PyDateTime::is_type_of(dt1),
    };
    let mut dtinfo2 = DateTimeInfo {
        year: dt2.cast::<PyDate>()?.get_year(),
        month: i32::from(dt2.cast::<PyDate>()?.get_month()),
        day: i32::from(dt2.cast::<PyDate>()?.get_day()),
        hour: 0,
        minute: 0,
        second: 0,
        microsecond: 0,
        total_seconds: 0,
        tz: dt2_tz.as_str(),
        offset: get_offset(dt2)?,
        is_datetime: PyDateTime::is_exact_type_of(dt2),
    };
    let in_same_tz: bool = dtinfo1.tz == dtinfo2.tz && !dtinfo1.tz.is_empty();
    let mut total_days = helpers::day_number(dtinfo2.year, dtinfo2.month as u8, dtinfo2.day as u8)
        - helpers::day_number(dtinfo1.year, dtinfo1.month as u8, dtinfo1.day as u8);

    if dtinfo1.is_datetime {
        let dt1dt: &Bound<PyDateTime> = dt1.cast()?;

        dtinfo1.hour = i32::from(dt1dt.get_hour());
        dtinfo1.minute = i32::from(dt1dt.get_minute());
        dtinfo1.second = i32::from(dt1dt.get_second());
        dtinfo1.microsecond = dt1dt.get_microsecond() as i32;

        if !in_same_tz && dtinfo1.offset != 0 || total_days == 0 {
            dtinfo1.shift_to_utc();
        }

        dtinfo1.total_seconds = dtinfo1.hour * SECS_PER_HOUR as i32
            + dtinfo1.minute * SECS_PER_MIN as i32
            + dtinfo1.second;
    }

    if dtinfo2.is_datetime {
        let dt2dt: &Bound<PyDateTime> = dt2.cast()?;

        dtinfo2.hour = i32::from(dt2dt.get_hour());
        dtinfo2.minute = i32::from(dt2dt.get_minute());
        dtinfo2.second = i32::from(dt2dt.get_second());
        dtinfo2.microsecond = dt2dt.get_microsecond() as i32;

        if !in_same_tz && dtinfo2.offset != 0 || total_days == 0 {
            dtinfo2.shift_to_utc();
        }

        dtinfo2.total_seconds = dtinfo2.hour * SECS_PER_HOUR as i32
            + dtinfo2.minute * SECS_PER_MIN as i32
            + dtinfo2.second;
    }

    if dtinfo1 > dtinfo2 {
        sign = -1;
        (dtinfo1, dtinfo2) = (dtinfo2, dtinfo1);

        total_days = -total_days;
    }

    let mut year_diff = dtinfo2.year - dtinfo1.year;
    let mut month_diff = dtinfo2.month - dtinfo1.month;
    let mut day_diff = dtinfo2.day - dtinfo1.day;
    let mut hour_diff = dtinfo2.hour - dtinfo1.hour;
    let mut minute_diff = dtinfo2.minute - dtinfo1.minute;
    let mut second_diff = dtinfo2.second - dtinfo1.second;
    let mut microsecond_diff = dtinfo2.microsecond - dtinfo1.microsecond;

    if microsecond_diff < 0 {
        microsecond_diff += 1_000_000;
        second_diff -= 1;
    }

    if second_diff < 0 {
        second_diff += 60;
        minute_diff -= 1;
    }

    if minute_diff < 0 {
        minute_diff += 60;
        hour_diff -= 1;
    }

    if hour_diff < 0 {
        hour_diff += 24;
        day_diff -= 1;
    }

    if day_diff < 0 {
        // If we have a difference in days,
        // we have to check if they represent months
        let mut year = dtinfo2.year;
        let mut month = dtinfo2.month;

        if month == 1 {
            month = 12;
            year -= 1;
        } else {
            month -= 1;
        }

        let leap = helpers::is_leap(year);

        let days_in_last_month = DAYS_PER_MONTHS[usize::from(leap)][month as usize];
        let days_in_month =
            DAYS_PER_MONTHS[usize::from(helpers::is_leap(dtinfo2.year))][dtinfo2.month as usize];

        match day_diff.cmp(&(days_in_month - days_in_last_month)) {
            Ordering::Less => {
                // We don't have a full month, we calculate days
                if days_in_last_month < dtinfo1.day {
                    day_diff += dtinfo1.day;
                } else {
                    day_diff += days_in_last_month;
                }
            }
            Ordering::Equal => {
                // We have exactly a full month
                // We remove the days difference
                // and add one to the months difference
                day_diff = 0;
                month_diff += 1;
            }
            Ordering::Greater => {
                // We have a full month
                day_diff += days_in_last_month;
            }
        }

        month_diff -= 1;
    }

    if month_diff < 0 {
        month_diff += 12;
        year_diff -= 1;
    }

    Ok(PreciseDiff {
        years: year_diff * sign,
        months: month_diff * sign,
        days: day_diff * sign,
        hours: hour_diff * sign,
        minutes: minute_diff * sign,
        seconds: second_diff * sign,
        microseconds: microsecond_diff * sign,
        total_days: total_days * sign,
    })
}
