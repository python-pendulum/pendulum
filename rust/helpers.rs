use crate::constants::{
    DAYS_PER_L_YEAR, DAYS_PER_N_YEAR, DAY_OF_WEEK_TABLE, EPOCH_YEAR, MONTHS_OFFSETS,
    SECS_PER_100_YEARS, SECS_PER_400_YEARS, SECS_PER_4_YEARS, SECS_PER_DAY, SECS_PER_HOUR,
    SECS_PER_MIN, SECS_PER_YEAR, TM_DECEMBER, TM_JANUARY,
};

fn p(year: u32) -> u32 {
    return year + year / 4 - year / 100 + year / 400;
}

pub fn is_leap(year: u32) -> bool {
    year % 4 == 0 && (year % 100 != 0 || year % 400 == 0)
}

pub fn is_long_year(year: u32) -> bool {
    (p(year) % 7 == 4) || (p(year - 1) % 7 == 3)
}

pub fn days_in_year(year: u32) -> u32 {
    if is_leap(year) {
        return DAYS_PER_L_YEAR;
    }

    DAYS_PER_N_YEAR
}

pub fn week_day(year: u32, month: u32, day: u32) -> u32 {
    let y: u32 = year - (month < 3) as u32;

    let w: u32 = (p(y) + DAY_OF_WEEK_TABLE[(month - 1) as usize] + day) % 7;

    if w == 0 {
        return 7;
    }

    w
}

pub fn local_time(
    unix_time: isize,
    utc_offset: isize,
    microsecond: usize,
) -> (usize, usize, usize, usize, usize, usize, usize) {
    let mut year: usize = EPOCH_YEAR as usize;
    let mut seconds: isize = unix_time;

    // Shift to a base year that is 400-year aligned.
    if seconds >= 0 {
        seconds -= (10957 * SECS_PER_DAY as usize) as isize;
        year += 30; // == 2000
    } else {
        seconds += ((146097 - 10957) * SECS_PER_DAY as usize) as isize;
        year -= 370; // == 1600
    }

    seconds += utc_offset;

    // Handle years in chunks of 400/100/4/1
    year += 400 * (seconds / SECS_PER_400_YEARS as isize) as usize;
    seconds %= SECS_PER_400_YEARS as isize;
    if seconds < 0 {
        seconds += SECS_PER_400_YEARS as isize;
        year -= 400;
    }

    let mut leap_year = 1; // 4-century aligned
    let mut sec_per_100years = SECS_PER_100_YEARS[leap_year] as isize;

    while seconds >= sec_per_100years {
        seconds -= sec_per_100years;
        year += 100;
        leap_year = 0; // 1-century, non 4-century aligned
        sec_per_100years = SECS_PER_100_YEARS[leap_year] as isize;
    }

    let mut sec_per_4years = SECS_PER_4_YEARS[leap_year] as isize;
    while seconds >= sec_per_4years {
        seconds -= sec_per_4years;
        year += 4;
        leap_year = 1; // 4-year, non century aligned
        sec_per_4years = SECS_PER_4_YEARS[leap_year] as isize;
    }

    let mut sec_per_year = SECS_PER_YEAR[leap_year] as isize;
    while seconds >= sec_per_year {
        seconds -= sec_per_year;
        year += 1;
        leap_year = 0; // non 4-year aligned
        sec_per_year = SECS_PER_YEAR[leap_year] as isize;
    }

    // Handle months and days
    let mut month = (TM_DECEMBER + 1) as usize;
    let mut day: usize = (seconds / (SECS_PER_DAY as isize) + 1) as usize;
    seconds %= SECS_PER_DAY as isize;

    let mut month_offset: usize;
    while month != (TM_JANUARY + 1) as usize {
        month_offset = MONTHS_OFFSETS[leap_year][month] as usize;
        if day > month_offset {
            day -= month_offset;
            break;
        }

        month -= 1;
    }

    // Handle hours, minutes and seconds
    let hour: usize = (seconds / SECS_PER_HOUR as isize) as usize;
    seconds %= SECS_PER_HOUR as isize;
    let minute: usize = (seconds / SECS_PER_MIN as isize) as usize;
    let second: usize = (seconds % SECS_PER_MIN as isize) as usize;

    (year, month, day, hour, minute, second, microsecond)
}
