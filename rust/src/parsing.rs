use core::str;
use std::{fmt, str::CharIndices};

use crate::{
    constants::MONTHS_OFFSETS,
    helpers::{days_in_year, is_leap, is_long_year, week_day},
};

#[derive(Debug, Clone)]
pub struct ParseError {
    index: usize,
    message: String,
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} (Position: {})", self.message, self.index)
    }
}

pub struct ParsedDateTime {
    pub year: u32,
    pub month: u32,
    pub day: u32,
    pub hour: u32,
    pub minute: u32,
    pub second: u32,
    pub microsecond: u32,
    pub offset: Option<i32>,
    #[allow(dead_code)]
    pub has_offset: bool,
    pub tzname: Option<String>,
    pub has_date: bool,
    pub has_time: bool,
    pub extended_date_format: bool,
    pub time_is_midnight: bool,
}

impl ParsedDateTime {
    pub fn new() -> ParsedDateTime {
        ParsedDateTime {
            year: 0,
            month: 1,
            day: 1,
            hour: 0,
            minute: 0,
            second: 0,
            microsecond: 0,
            offset: None,
            has_offset: false,
            tzname: None,
            has_date: false,
            has_time: false,
            extended_date_format: false,
            time_is_midnight: false,
        }
    }
}

pub struct ParsedDuration {
    pub years: u32,
    pub months: u32,
    pub weeks: u32,
    pub days: u32,
    pub hours: u32,
    pub minutes: u32,
    pub seconds: u32,
    pub microseconds: u32,
}

impl ParsedDuration {
    pub fn new() -> ParsedDuration {
        ParsedDuration {
            years: 0,
            months: 0,
            weeks: 0,
            days: 0,
            hours: 0,
            minutes: 0,
            seconds: 0,
            microseconds: 0,
        }
    }
}

pub struct Parsed {
    pub datetime: Option<ParsedDateTime>,
    pub duration: Option<ParsedDuration>,
    pub second_datetime: Option<ParsedDateTime>,
}

impl Parsed {
    pub fn new() -> Parsed {
        Parsed {
            datetime: None,
            duration: None,
            second_datetime: None,
        }
    }
}

pub struct Parser<'a> {
    /// Input to parse.
    src: &'a str,
    /// Iterator used for getting characters from `src`.
    chars: CharIndices<'a>,
    /// Current byte offset into `src`.
    idx: usize,
    /// Current character
    current: char,
}

impl<'a> Parser<'a> {
    /// Creates a new parser from a &str.
    pub fn new(input: &'a str) -> Parser<'a> {
        let mut p = Parser {
            src: input,
            chars: input.char_indices(),
            idx: 0,
            current: '\0',
        };
        p.inc();
        p
    }

    /// Increments the parser if the end of the input has not been reached.
    /// Returns whether or not it was able to advance.
    fn inc(&mut self) -> Option<char> {
        if let Some((i, ch)) = self.chars.next() {
            self.idx = i;
            self.current = ch;
            Some(ch)
        } else {
            self.idx = self.src.len();
            self.current = '\0';
            None
        }
    }

    fn parse_error(&mut self, message: String) -> ParseError {
        ParseError {
            index: self.idx,
            message,
        }
    }

    fn unexpected_character_error(
        &mut self,
        field_name: &str,
        expected_character_count: usize,
    ) -> ParseError {
        if self.end() {
            return self.parse_error(format!(
                "Unexpected end of string while parsing {}. Expected {} more character{}.",
                field_name,
                expected_character_count,
                if expected_character_count == 1 {
                    ""
                } else {
                    "s"
                }
            ));
        }

        self.parse_error(format!(
            "Invalid character while parsing {}: {}.",
            field_name, self.current,
        ))
    }

    /// Returns true if the parser has reached the end of the input.
    fn end(&self) -> bool {
        self.idx >= self.src.len()
    }

    fn parse_integer(&mut self, length: usize, field_name: &str) -> Result<u32, ParseError> {
        let mut value: u32 = 0;

        for i in 0..length {
            if self.end() {
                return Err(self.parse_error(format!(
                    "Unexpected end of string while parsing \"{}\". Expected {} more character{}",
                    field_name,
                    length - i,
                    if (length - i) != 1 { "s" } else { "" }
                )));
            }

            if let Some(digit) = self.current.to_digit(10) {
                value = 10 * value + digit;
                self.inc();
            } else {
                return Err(self.unexpected_character_error(field_name, length - i));
            }
        }

        Ok(value)
    }

    pub fn parse(&mut self) -> Result<Parsed, ParseError> {
        let mut parsed = Parsed::new();

        if self.current == 'P' {
            // Duration (and possibly time interval)
            self.parse_duration(&mut parsed)?;
        } else {
            self.parse_datetime(&mut parsed)?;
        }

        Ok(parsed)
    }

    fn parse_datetime(&mut self, parsed: &mut Parsed) -> Result<(), ParseError> {
        let mut datetime = ParsedDateTime::new();

        if self.current == 'T' {
            self.parse_time(&mut datetime, false)?;

            if !self.end() {
                return Err(self.parse_error("Unconverted data remains".to_string()));
            }

            match &parsed.datetime {
                Some(_) => {
                    parsed.second_datetime = Some(datetime);
                }
                None => match &parsed.duration {
                    Some(_) => {
                        parsed.second_datetime = Some(datetime);
                    }
                    None => {
                        parsed.datetime = Some(datetime);
                    }
                },
            }

            return Ok(());
        }

        datetime.year = self.parse_integer(2, "year")?;

        if self.current == ':' {
            // Time in extended format
            datetime.hour = datetime.year;
            datetime.year = 0;
            datetime.extended_date_format = true;
            self.parse_time(&mut datetime, true)?;

            if !self.end() {
                return Err(self.parse_error("Unconverted data remains".to_string()));
            }

            match &parsed.datetime {
                Some(_) => {
                    parsed.second_datetime = Some(datetime);
                }
                None => match &parsed.duration {
                    Some(_) => {
                        parsed.second_datetime = Some(datetime);
                    }
                    None => {
                        parsed.datetime = Some(datetime);
                    }
                },
            }

            return Ok(());
        }

        datetime.has_date = true;
        datetime.year = datetime.year * 100 + self.parse_integer(2, "year")?;

        if self.current == '-' {
            self.inc();
            datetime.extended_date_format = true;

            if self.current == 'W' {
                // ISO week and day in extended format (i.e. Www-D)
                self.inc();

                let iso_week = self.parse_integer(2, "iso week")?;
                let mut iso_day: u32 = 1;

                if !self.end() && self.current != ' ' && self.current != 'T' {
                    // Optional day
                    if self.current != '-' {
                        return Err(self.parse_error(format!(
                            "Invalid character \"{}\" while parsing {}",
                            self.current, "date separator"
                        )));
                    }

                    self.inc();

                    iso_day = self.parse_integer(1, "iso day")?;
                }

                let (year, month, day) = self.iso_to_ymd(datetime.year, iso_week, iso_day)?;

                datetime.year = year;
                datetime.month = month;
                datetime.day = day;
            } else {
                /*
                Month and day in extended format (MM-DD) or ordinal date (DDD)
                We'll assume first that the next part is a month and adjust if not.
                */
                datetime.month = self.parse_integer(2, "month")?;

                if !self.end() && self.current != ' ' && self.current != 'T' {
                    if self.current == '-' {
                        // Optional day
                        self.inc();
                        datetime.day = self.parse_integer(2, "day")?;
                    } else {
                        // Ordinal day
                        let ordinal_day =
                            (datetime.month * 10 + self.parse_integer(1, "ordinal day")?) as i32;

                        let (year, month, day) =
                            self.ordinal_to_ymd(datetime.year, ordinal_day, false)?;

                        datetime.year = year;
                        datetime.month = month;
                        datetime.day = day;
                    }
                } else {
                    datetime.day = 1;
                }
            }
        } else if self.current == 'W' {
            // Compact ISO week and day (WwwD)
            self.inc();

            let iso_week = self.parse_integer(2, "iso week")?;
            let mut iso_day: u32 = 1;

            if !self.end() && self.current != ' ' && self.current != 'T' {
                iso_day = self.parse_integer(1, "iso day")?;
            }

            match self.iso_to_ymd(datetime.year, iso_week, iso_day) {
                Ok((year, month, day)) => {
                    datetime.year = year;
                    datetime.month = month;
                    datetime.day = day;
                }
                Err(error) => return Err(error),
            }
        } else {
            /*
            Month and day in compact format (MMDD) or ordinal date (DDD)
            We'll assume first that the next part is a month and adjust if not.
            */
            datetime.month = self.parse_integer(2, "month")?;
            let mut ordinal_day = self.parse_integer(1, "ordinal day")? as i32;

            if self.end() || self.current == ' ' || self.current == 'T' {
                // Ordinal day
                ordinal_day += datetime.month as i32 * 10;

                let (year, month, day) = self.ordinal_to_ymd(datetime.year, ordinal_day, false)?;

                datetime.year = year;
                datetime.month = month;
                datetime.day = day;
            } else {
                // Day
                datetime.day = ordinal_day as u32 * 10 + self.parse_integer(1, "day")?;
            }
        }

        if !self.end() {
            self.parse_time(&mut datetime, false)?;
        }

        if !self.end() {
            if self.current == '/' && parsed.datetime.is_none() && parsed.duration.is_none() {
                // Interval
                parsed.datetime = Some(datetime);

                self.inc();

                if self.current == 'P' {
                    // Duration
                    self.parse_duration(parsed)?;
                } else {
                    self.parse_datetime(parsed)?;
                }

                return Ok(());
            }

            return Err(self.parse_error("Unconverted data remains".to_string()));
        }

        match &parsed.datetime {
            Some(_) => {
                parsed.second_datetime = Some(datetime);
            }
            None => match &parsed.duration {
                Some(_) => {
                    parsed.second_datetime = Some(datetime);
                }
                None => {
                    parsed.datetime = Some(datetime);
                }
            },
        }

        Ok(())
    }

    fn parse_time(
        &mut self,
        datetime: &mut ParsedDateTime,
        skip_hour: bool,
    ) -> Result<(), ParseError> {
        // TODO: Add support for decimal units

        // Date/Time separator
        if self.current != 'T' && self.current != ' ' && !skip_hour {
            return Err(self.parse_error(format!(
                "Invalid character \"{}\" while parsing {}",
                self.current, "date and time separator (\"T\" or \" \")"
            )));
        }

        datetime.has_time = true;

        if !skip_hour {
            self.inc();

            // Hour
            datetime.hour = self.parse_integer(2, "hour")?;
        }

        if !self.end() && self.current != 'Z' && self.current != '+' && self.current != '-' {
            // Optional minute and second
            if self.current == ':' {
                // Minute and second in extended format (mm:ss)
                self.inc();

                // Minute
                datetime.minute = self.parse_integer(2, "minute")?;

                if !self.end() && self.current != 'Z' && self.current != '+' && self.current != '-'
                {
                    // Optional second
                    if self.current != ':' {
                        return Err(self.parse_error(format!(
                            "Invalid character \"{}\" while parsing {}",
                            self.current, "time separator (\":\")"
                        )));
                    }

                    self.inc();

                    // Second
                    datetime.second = self.parse_integer(2, "second")?;

                    if self.current == '.' || self.current == ',' {
                        // Optional fractional second
                        self.inc();

                        datetime.microsecond = 0;
                        let mut i: u8 = 0;

                        while i < 6 {
                            if let Some(digit) = self.current.to_digit(10) {
                                datetime.microsecond = datetime.microsecond * 10 + digit;
                            } else if i == 0 {
                                // One digit minimum is required
                                return Err(self.unexpected_character_error("subsecond", 1));
                            } else {
                                break;
                            }

                            self.inc();
                            i += 1;
                        }

                        // Drop extraneous digits
                        while self.current.is_ascii_digit() {
                            self.inc();
                        }

                        // Expand missing microsecond
                        while i < 6 {
                            datetime.microsecond *= 10;
                            i += 1;
                        }
                    }

                    if !datetime.extended_date_format {
                        return Err(self.parse_error("Cannot combine \"basic\" date format with \"extended\" time format (Should be either `YYYY-MM-DDThh:mm:ss` or `YYYYMMDDThhmmss`).".to_string()));
                    }
                }
            } else {
                // Minute and second in compact format (mmss)

                // Minute
                datetime.minute = self.parse_integer(2, "minute")?;

                if !self.end() && self.current != 'Z' && self.current != '+' && self.current != '-'
                {
                    // Optional second

                    datetime.second = self.parse_integer(2, "second")?;

                    if self.current == '.' || self.current == ',' {
                        // Optional fractional second
                        self.inc();

                        datetime.microsecond = 0;
                        let mut i: u8 = 0;

                        while i < 6 {
                            if let Some(digit) = self.current.to_digit(10) {
                                datetime.microsecond = datetime.microsecond * 10 + digit;
                            } else if i == 0 {
                                // One digit minimum is required
                                return Err(self.unexpected_character_error("subsecond", 1));
                            } else {
                                break;
                            }

                            self.inc();
                            i += 1;
                        }

                        // Drop extraneous digits
                        while self.current.is_ascii_digit() {
                            self.inc();
                        }

                        // Expand missing microsecond
                        while i < 6 {
                            datetime.microsecond *= 10;
                            i += 1;
                        }
                    }
                }

                if datetime.extended_date_format {
                    return Err(self.parse_error("Cannot combine \"extended\" date format with \"basic\" time format (Should be either `YYYY-MM-DDThh:mm:ss` or `YYYYMMDDThhmmss`).".to_string()));
                }
            }
        }

        if datetime.hour == 24
            && datetime.minute == 0
            && datetime.second == 0
            && datetime.microsecond == 0
        {
            // Special case for 24:00:00, which is valid for ISO 8601.
            // This is equivalent to 00:00:00 the next day.
            // We will store the information for now.
            datetime.time_is_midnight = true;
        }

        if self.current == 'Z' {
            // UTC
            datetime.offset = Some(0);
            datetime.tzname = Some("UTC".to_string());
            self.inc();
        } else if matches!(self.current, '+' | '-') {
            // Optional timezone offset
            let tzsign = if self.current == '+' { 1 } else { -1 };
            self.inc();
            // Offset hour
            let tzhour = self.parse_integer(2, "timezone hour")? as i32;
            if self.current == ':' {
                // Optional separator
                self.inc();
            }
            let mut tzminute = if self.end() {
                0
            } else {
                // Optional minute
                self.parse_integer(2, "timezone minute")? as i32
            };
            tzminute += tzhour * 60;
            tzminute *= tzsign;
            if tzminute > 24 * 60 {
                return Err(self.parse_error("Timezone offset is too large".to_string()));
            }
            datetime.offset = Some(tzminute * 60);
        }

        Ok(())
    }

    fn parse_duration(&mut self, parsed: &mut Parsed) -> Result<(), ParseError> {
        // Removing P operator
        self.inc();

        let mut duration: ParsedDuration = ParsedDuration::new();
        let mut got_t: bool = false;
        let mut last_had_fraction = false;

        loop {
            match self.current {
                'T' => {
                    if got_t {
                        return Err(
                            self.parse_error("Repeated time declaration in duration".to_string())
                        );
                    }

                    got_t = true;
                }
                _c => {
                    let (value, op_fraction) = self.parse_duration_number_frac()?;
                    if last_had_fraction {
                        return Err(self.parse_error("Invalid duration fraction".to_string()));
                    }

                    if op_fraction.is_some() {
                        last_had_fraction = true;
                    }

                    if got_t {
                        match self.current {
                            'H' => {
                                if duration.minutes != 0
                                    || duration.seconds != 0
                                    || duration.microseconds != 0
                                {
                                    return Err(
                                        self.parse_error("Duration units out of order".to_string())
                                    );
                                }

                                duration.hours += value;

                                if let Some(fraction) = op_fraction {
                                    let extra_minutes = fraction * 60_f64;
                                    let extra_full_minutes: f64 = extra_minutes.trunc();
                                    duration.minutes += extra_full_minutes as u32;
                                    let extra_seconds =
                                        ((extra_minutes - extra_full_minutes) * 60.0).round();
                                    let extra_full_seconds = extra_seconds.trunc();
                                    duration.seconds += extra_full_seconds as u32;
                                    let micro_extra = ((extra_seconds - extra_full_seconds)
                                        * 1_000_000.0)
                                        .round()
                                        as u32;
                                    duration.microseconds += micro_extra;
                                }
                            }
                            'M' => {
                                if duration.seconds != 0 || duration.microseconds != 0 {
                                    return Err(
                                        self.parse_error("Duration units out of order".to_string())
                                    );
                                }

                                duration.minutes += value;

                                if let Some(fraction) = op_fraction {
                                    let extra_seconds = fraction * 60_f64;
                                    let extra_full_seconds = extra_seconds.trunc();
                                    duration.seconds += extra_full_seconds as u32;
                                    let micro_extra = ((extra_seconds - extra_full_seconds)
                                        * 1_000_000.0)
                                        .round()
                                        as u32;
                                    duration.microseconds += micro_extra;
                                }
                            }
                            'S' => {
                                duration.seconds = value;

                                if let Some(fraction) = op_fraction {
                                    duration.microseconds +=
                                        (fraction * 1_000_000.0).round() as u32;
                                }
                            }
                            _ => {
                                return Err(
                                    self.parse_error("Invalid duration time unit".to_string())
                                )
                            }
                        }
                    } else {
                        match self.current {
                            'Y' => {
                                if last_had_fraction {
                                    return Err(self.parse_error(
                                        "Fractional years in duration are not supported"
                                            .to_string(),
                                    ));
                                }

                                if duration.months != 0 || duration.days != 0 {
                                    return Err(
                                        self.parse_error("Duration units out of order".to_string())
                                    );
                                }

                                duration.years = value;
                            }
                            'M' => {
                                if last_had_fraction {
                                    return Err(self.parse_error(
                                        "Fractional months in duration are not supported"
                                            .to_string(),
                                    ));
                                }

                                if duration.days != 0 {
                                    return Err(
                                        self.parse_error("Duration units out of order".to_string())
                                    );
                                }

                                duration.months = value;
                            }
                            'W' => {
                                if duration.years != 0 || duration.months != 0 {
                                    return Err(self.parse_error(
                                        "Basic format durations cannot have weeks".to_string(),
                                    ));
                                }

                                duration.weeks = value;

                                if let Some(fraction) = op_fraction {
                                    let extra_days = fraction * 7_f64;
                                    let extra_full_days = extra_days.trunc();
                                    duration.days += extra_full_days as u32;
                                    let extra_hours = (extra_days - extra_full_days) * 24.0;
                                    let extra_full_hours = extra_hours.trunc();
                                    duration.hours += extra_full_hours as u32;
                                    let extra_minutes =
                                        ((extra_hours - extra_full_hours) * 60.0).round();
                                    let extra_full_minutes: f64 = extra_minutes.trunc();
                                    duration.minutes += extra_full_minutes as u32;
                                    let extra_seconds =
                                        ((extra_minutes - extra_full_minutes) * 60.0).round();
                                    let extra_full_seconds = extra_seconds.trunc();
                                    duration.seconds += extra_full_seconds as u32;
                                    let micro_extra = ((extra_seconds - extra_full_seconds)
                                        * 1_000_000.0)
                                        .round()
                                        as u32;
                                    duration.microseconds += micro_extra;
                                }
                            }
                            'D' => {
                                if duration.weeks != 0 {
                                    return Err(self.parse_error(
                                        "Week format durations cannot have days".to_string(),
                                    ));
                                }

                                duration.days += value;
                                if let Some(fraction) = op_fraction {
                                    let extra_hours = fraction * 24.0;
                                    let extra_full_hours = extra_hours.trunc();
                                    duration.hours += extra_full_hours as u32;
                                    let extra_minutes =
                                        ((extra_hours - extra_full_hours) * 60.0).round();
                                    let extra_full_minutes: f64 = extra_minutes.trunc();
                                    duration.minutes += extra_full_minutes as u32;
                                    let extra_seconds =
                                        ((extra_minutes - extra_full_minutes) * 60.0).round();
                                    let extra_full_seconds = extra_seconds.trunc();
                                    duration.seconds += extra_full_seconds as u32;
                                    let micro_extra = ((extra_seconds - extra_full_seconds)
                                        * 1_000_000.0)
                                        .round()
                                        as u32;
                                    duration.microseconds += micro_extra;
                                }
                            }
                            _ => {
                                return Err(
                                    self.parse_error("Invalid duration time unit".to_string())
                                )
                            }
                        }
                    }
                }
            }
            self.inc();

            if self.end() {
                break;
            }
        }

        parsed.duration = Some(duration);

        Ok(())
    }

    fn parse_duration_number_frac(&mut self) -> Result<(u32, Option<f64>), ParseError> {
        let value = self.parse_duration_number()?;
        let fraction = matches!(self.current, '.' | ',').then(|| {
            let mut decimal = 0_f64;
            let mut denominator = 1_f64;

            while let Some(digit) = self.inc().and_then(|ch| ch.to_digit(10)) {
                decimal *= 10.0;
                decimal += f64::from(digit);
                denominator *= 10.0;
            }

            decimal / denominator
        });

        Ok((value, fraction))
    }

    fn parse_duration_number(&mut self) -> Result<u32, ParseError> {
        let Some(mut value) = self.current.to_digit(10) else {
            return Err(self.parse_error("Invalid number in duration".to_string()));
        };

        while let Some(digit) = self.inc().and_then(|ch| ch.to_digit(10)) {
            value *= 10;
            value += digit;
        }

        Ok(value)
    }

    fn iso_to_ymd(
        &mut self,
        iso_year: u32,
        iso_week: u32,
        iso_day: u32,
    ) -> Result<(u32, u32, u32), ParseError> {
        if iso_week > 53 || iso_week > 52 && !is_long_year(iso_year as i32) {
            return Err(ParseError {
                index: self.idx,
                message: format!(
                    "Invalid ISO date: week {iso_week} out of range for year {iso_year}"
                ),
            });
        }

        if iso_day > 7 {
            return Err(ParseError {
                index: self.idx,
                message: "Invalid ISO date: week day is invalid".to_string(),
            });
        }

        let ordinal: i32 =
            iso_week as i32 * 7 + iso_day as i32 - (week_day(iso_year as i32, 1, 4) as i32 + 3);

        self.ordinal_to_ymd(iso_year, ordinal, true)
    }

    fn ordinal_to_ymd(
        &mut self,
        year: u32,
        ordinal: i32,
        allow_out_of_bounds: bool,
    ) -> Result<(u32, u32, u32), ParseError> {
        let mut ord: i32 = ordinal;
        let mut y: u32 = year;
        let mut leap: usize = usize::from(is_leap(y as i32));

        if ord < 1 {
            if !allow_out_of_bounds {
                return Err(self.parse_error(format!(
                    "Invalid ordinal day: {ordinal} is too small for year {year}"
                )));
            }
            // Previous year
            ord += days_in_year((year - 1) as i32) as i32;
            y -= 1;
            leap = usize::from(is_leap(y as i32));
        }

        if ord > days_in_year(y as i32) as i32 {
            if !allow_out_of_bounds {
                return Err(self.parse_error(format!(
                    "Invalid ordinal day: {ordinal} is too large for year {year}"
                )));
            }

            // Next year
            ord -= days_in_year(y as i32) as i32;
            y += 1;
            leap = usize::from(is_leap(y as i32));
        }

        for i in 1..14 {
            if ord < MONTHS_OFFSETS[leap][i] {
                let day = ord as u32 - MONTHS_OFFSETS[leap][i - 1] as u32;
                let month = (i - 1) as u32;

                return Ok((y, month, day));
            }
        }

        Err(self.parse_error(format!(
            "Invalid ordinal day: {ordinal} is too large for year {year}"
        )))
    }
}
