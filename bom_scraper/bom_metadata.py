def get_div_text(raw_text):
    return raw_text.strip().replace("\xa0", "").split("\n")


def process_grosses(mp_box):
    rows = mp_box.findAll("tr")
    domestic = ""
    foreign = ""
    worldwide = ""
    for row in rows:
        parsed_tr = get_div_text(row.text)
        if len(parsed_tr) < 2:
            continue
        header = parsed_tr[0]
        dollar_amount = parsed_tr[1]
        if "Domestic" in header:
            domestic = dollar_amount
        elif "Foreign" in header:
            foreign = dollar_amount
        elif "Worldwide" in header:
            worldwide = dollar_amount
    return domestic, foreign, worldwide


def get_opening(header):
    return header.split(":")[-1]


def get_widest_release(parsed_tr):
    return parsed_tr[-1].split(" ")[0]


def get_close_date_or_in_release(parsed_tr):
    return parsed_tr[-1]


def process_summary(mp_box):
    rows = mp_box.findAll("tr")

    limited_release_date = ""
    wide_release_date = ""
    limited_opening = ""
    wide_opening = ""
    widest_release = ""
    close_date = ""
    in_release = ""

    for row in rows:
        parsed_tr = get_div_text(row.text)
        header = parsed_tr[0]
        if "ReleaseDates" in header:
            limited_release_date, wide_release_date = process_release_date(parsed_tr)
        elif "LimitedOpeningWeekend" in header:
            limited_opening = get_opening(header)
        elif "WideOpeningWeekend" in header:
            wide_opening = get_opening(header)
        elif "WidestRelease" in header:
            widest_release = get_widest_release(parsed_tr)
        elif "CloseDate" in header:
            close_date = get_close_date_or_in_release(parsed_tr)
        elif "In Release" in header:
            in_release = get_close_date_or_in_release(parsed_tr)

    return (
        limited_release_date,
        wide_release_date,
        limited_opening,
        wide_opening,
        widest_release,
        close_date,
        in_release,
    )


def process_release_date(parsed_tr):
    release_dates = parsed_tr[1:]
    limited_release_date = ""
    wide_release_date = ""
    for release_date in release_dates:
        if "limited" in release_date:
            limited_release_date = release_date.replace(" (limited)", "")
        elif "wide" in release_date:
            wide_release_date = release_date.replace(" (wide)", "")
    return limited_release_date, wide_release_date
