use crate::constants::{
    DAYS_PER_L_YEAR, DAYS_PER_N_YEAR, DAY_OF_WEEK_TABLE, EPOCH_YEAR, MONTHS_OFFSETS,
    SECS_PER_100_YEARS, SECS_PER_400_YEARS, SECS_PER_4_YEARS, SECS_PER_DAY, SECS_PER_HOUR,
    SECS_PER_MIN, SECS_PER_YEAR, TM_DECEMBER, TM_JANUARY,
};

fn p(year: i32) -> i32 {
    year + year / 4 - year / 100 + year / 400
}

pub fn is_leap(year: i32) -> bool {
    year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)
}

pub fn is_long_year(year: i32) -> bool {
    (p(year) % 7 == 4) || (p(year - 1) % 7 == 3)
}

pub fn days_in_year(year: i32) -> u32 {
    if is_leap(year) {
        return DAYS_PER_L_YEAR;
    }

    DAYS_PER_N_YEAR
}

pub fn week_day(year: i32, month: u32, day: u32) -> u32 {
    let y: i32 = year - i32::from(month < 3);

    let w: i32 = (p(y) + DAY_OF_WEEK_TABLE[(month - 1) as usize] as i32 + day as i32) % 7;

    if w == 0 {
        return 7;
    }

    w.unsigned_abs()
}

pub fn day_number(year: i32, month: u8, day: u8) -> i32 {
    let m = i32::from((month + 9) % 12);
    let y = year - m / 10;

    365 * y + y / 4 - y / 100 + y / 400 + (m * 306 + 5) / 10 + (i32::from(day) - 1)
}

pub fn local_time(
    unix_time: f64,
    utc_offset: isize,
    microsecond: usize,
) -> (usize, usize, usize, usize, usize, usize, usize) {
    let mut year: usize = EPOCH_YEAR as usize;
    let mut seconds: i64 = unix_time.floor() as i64;

    // Shift to a base year that is 400-year aligned.
    if seconds >= 0 {
        seconds -= 10957 * SECS_PER_DAY as i64;
        year += 30; // == 2000
    } else {
        seconds += (146_097 - 10957) * SECS_PER_DAY as i64;
        year -= 370; // == 1600
    }

    seconds += utc_offset as i64;

    // Handle years in chunks of 400/100/4/1
    year += 400 * (seconds / SECS_PER_400_YEARS as i64) as usize;
    seconds %= SECS_PER_400_YEARS as i64;
    if seconds < 0 {
        seconds += SECS_PER_400_YEARS as i64;
        year -= 400;
    }

    let mut leap_year = 1; // 4-century aligned
    let mut sec_per_100years = SECS_PER_100_YEARS[leap_year].try_into().unwrap();

    while seconds >= sec_per_100years {
        seconds -= sec_per_100years;
        year += 100;
        leap_year = 0; // 1-century, non 4-century aligned
        sec_per_100years = SECS_PER_100_YEARS[leap_year].try_into().unwrap();
    }

    let mut sec_per_4years = SECS_PER_4_YEARS[leap_year].into();
    while seconds >= sec_per_4years {
        seconds -= sec_per_4years;
        year += 4;
        leap_year = 1; // 4-year, non century aligned
        sec_per_4years = SECS_PER_4_YEARS[leap_year].into();
    }

    let mut sec_per_year = SECS_PER_YEAR[leap_year].into();
    while seconds >= sec_per_year {
        seconds -= sec_per_year;
        year += 1;
        leap_year = 0; // non 4-year aligned
        sec_per_year = SECS_PER_YEAR[leap_year].into();
    }

    // Handle months and days
    let mut month = TM_DECEMBER + 1;
    let mut day: usize = (seconds / (SECS_PER_DAY as i64) + 1) as usize;
    seconds %= SECS_PER_DAY as i64;

    let mut month_offset: usize;
    while month != (TM_JANUARY + 1) {
        month_offset = MONTHS_OFFSETS[leap_year][month] as usize;
        if day > month_offset {
            day -= month_offset;
            break;
        }

        month -= 1;
    }

    // Handle hours, minutes and seconds
    let hour: usize = (seconds / SECS_PER_HOUR as i64) as usize;
    seconds %= SECS_PER_HOUR as i64;
    let minute: usize = (seconds / SECS_PER_MIN as i64) as usize;
    let second: usize = (seconds % SECS_PER_MIN as i64) as usize;

    (year, month, day, hour, minute, second, microsecond)
}
