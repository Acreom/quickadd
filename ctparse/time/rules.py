from typing import Optional, Any, cast
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY
from ..rule import rule, predicate, dimension, _regex_to_join
from ..types import Time, Duration, Interval, pod_hours, RegexMatch, DurationUnit, Recurring, RecurringFrequency, \
    RecurringArray

# removed about, around, approx, ( the)? due to conflicts in regular sentences ("sync about their tech")
@rule(
    r"at|on|am|um|gegen|den|dem|der|ca\.?|(in|of)",
    dimension(Time),
)
def ruleAbsorbOnTime(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch, t: Time) -> Time:
    return t


@rule(r"von|vom|zwischen|from|between", dimension(Interval))
def ruleAbsorbFromInterval(ts: datetime, pm_bias: bool, date_format: str, _: Any, i: Interval) -> Interval:
    return i


_dows = [
    ("mon", r"\bmontag\b|\bmonday\b|\bmon\.?\b"),
    ("tue", r"\bdie?nstag\b|\bdie\.?\b|\btuesday\b|\btue\.?\b"),
    ("wed", r"\bmittwoch\b|\bmi\.?\b|\bwednesday\b|\bwed\.?\b"),
    ("thu", r"\bdonn?erstag\b|\bthursday\b|\bthur?\.?\b"),
    ("fri", r"\bfreitag\b|\bfriday\b|\bfri\.?\b"),
    ("sat", r"\bsamstag\b|\bsonnabends?\b|\bsaturday\b|\bsat\.?\b"),
    ("sun", r"\bsonntag\b|\bso\.?\b|\bsunday\b|\bsun\.?\b"),
]
_rule_dows = r"|".join(r"(?P<{}>{})".format(dow, expr) for dow, expr in _dows)
_rule_dows = r"({})\s*".format(_rule_dows)


@rule(_rule_dows)
def ruleNamedDOW(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Time]:
    for i, (name, _) in enumerate(_dows):
        if m.match.group(name):
            return Time(DOW=i)
    return None


_months = [
    ("january", r"\bjanuary?\b|\bjan\.?\b"),
    ("february", r"\bfebruary?\b|\bfeb\.?\b"),
    ("march", r"\bmärz\b|\bmarch\b|\bmar\.?\b|\bmrz\.?\b|\bmär\.?\b"),
    ("april", r"\bapril\b|\bapr\.?\b"),
    ("may", r"\bmai\b|\bmay\.?\b"),
    ("june", r"\bjuni\b|\bjune\b|\bjun\.?\b"),
    ("july", r"\bjuli\b|\bjuly\b|\bjul\.?\b"),
    ("august", r"\baugust\b|\baug\.?\b"),
    ("september", r"\bseptember\b|\bsept?\.?\b"),
    ("october", r"\boktober\b|\boctober\b|\boct\.?\b|\bokt\.?\b"),
    ("november", r"\bnovember\b|\bnov\.?\b"),
    ("december", r"\bdecember\b|\bdezember\b|\bdez\.?\b|\bdec\.?\b"),
]
_rule_months = "|".join(r"(?P<{}>{})".format(name, expr) for name, expr in _months)


@rule(_rule_months)
def ruleNamedMonth(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Time]:
    match = m.match
    for i, (name, _) in enumerate(_months):
        if match.group(name):
            return Time(month=i + 1)
    return None


_named_ts = (
    (1, r"\bone\b|\beins\b?"),
    (2, r"\btwo\b|\bzwei\b"),
    (3, r"\bthree\b|\bdrei\b"),
    (4, r"\bfour\b|\bvier\b"),
    (5, r"\bfive\b|\bfünf\b"),
    (6, r"\bsix\b|\bsechs\b"),
    (7, r"\bseven\b|\bsieben\b"),
    (8, r"\beight\b|\bacht\b"),
    (9, r"\bnine\b|\bneun\b"),
    (10, r"\bten\b|\bzehn\b"),
    (11, r"\beleven\b|\belf\b"),
    (12, r"\btwelve\b|\bzwölf\b"),
)
_rule_named_ts = "|".join(r"(?P<t_{}>{})".format(n, expr) for n, expr in _named_ts)
_rule_named_ts = r"({})\s*".format(_rule_named_ts)


@rule(_rule_named_ts + r"(uhr|h|o\'?clock)?")
def ruleNamedHour(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Time]:
    match = m.match
    for n, _, in _named_ts:
        if match.group("t_{}".format(n)):
            return Time(hour=n, minute=0)
    return None


@rule("mitternacht|midnight")
def ruleMidnight(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch) -> Time:
    return Time(hour=0, minute=0)


def _pod_from_match(pod: str, m: RegexMatch) -> str:
    mod = ""
    if m.match.group("mod_early"):
        mod = "early"
    elif m.match.group("mod_late"):
        mod = "late"
    if m.match.group("mod_very"):
        mod = "very" + mod
    return mod + pod


@rule(
    r"(?P<mod_very>(sehr|very)\s+)?"
    "((?P<mod_early>früh(e(r|n|m))?|early)"
    "|(?P<mod_late>(spät(e(r|n|m))?|late)))",
    predicate("isPOD"),
)
def ruleEarlyLatePOD(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch, p: Time) -> Time:
    return Time(POD=_pod_from_match(p.POD, m))


_pods = [
    # (
    #     "first",
    #     (
    #         r"(erster?|first|earliest|as early|frühe?st(ens?)?|so früh)"
    #         "( (as )?possible| (wie )?möglich(er?)?)?"
    #     ),
    # ),
    # (
    #     "last",
    #     (
    #         r"(letzter?|last|latest|as late as possible|spätest möglich(er?)?|"
    #         "so spät wie möglich(er?)?)"
    #     ),
    # ),
    # ("earlymorning", r"very early|sehr früh"),
    # ("lateevening", r"very late|sehr spät"),
    ("morning", r"\bmorning\b|\bmorgend?s?\b"),
    ("forenoon", r"\bforenoon\b|\bvormittags?\b"),
    ("afternoon", r"\bafternoon\b|\bnachmittags?\b"),
    ("noon", r"\bnoon\b|\bmittags?\b"),
    ("evening", r"\bevening\b|\btonight\b|\babend?s?\b|\bspät\b"),
    ("night", r"\bnight\b|\bnachts?\b"),
]

_rule_pods = "|".join("(?P<{}>{})".format(pod, expr) for pod, expr in _pods)


@rule(_rule_pods)
def rulePOD(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Time]:
    for _, (pod, _) in enumerate(_pods):
        if m.match.group(pod):
            return Time(POD=pod)
    return None


@rule(r"(?<!\d|\.)(?P<day>(?&_day))\.?(?!\d)")
def ruleDOM1(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    # Ordinal day "5."
    return Time(day=int(m.match.group("day")))


@rule(r"(?<!\d|\.)(?P<month>(?&_month))\.?(?!\d)")
def ruleMonthOrdinal(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    # Ordinal day "5."
    return Time(month=int(m.match.group("month")))


@rule(r"(?<!\d|\.)(?P<day>(?&_day))\s*(?:st|nd|rd|th|s?ten|ter)")
# a "[0-31]" followed by a th/st
def ruleDOM2(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    return Time(day=int(m.match.group("day")))


@rule(r"(?<!\d|\.)(?P<year>(?&_year))(?!\d)")
def ruleYear(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    # Since we may have two-digits years, we have to make a call
    # on how to handle which century does the time refers to.
    # We are using a strategy inspired by excel. Reference:
    # https://github.com/comtravo/ctparse/issues/56
    # https://docs.microsoft.com/en-us/office/troubleshoot/excel/two-digit-year-numbers
    y = int(m.match.group("year"))
    SAME_CENTURY_THRESHOLD = 10

    # Let the reference year be ccyy (e.g. 1983 => cc=19, yy=83)
    cc = ts.year // 100
    yy = ts.year % 100
    # Check if year is two digits
    if y < 100:
        # Then any two digit year between 0 and
        # yy+10 is interpreted to be within the
        #  century cc (e.g. 83 maps to 1983, 93 to 1993),
        # anything above maps to the previous century (e.g. 94 maps to 1894).
        if y < yy + SAME_CENTURY_THRESHOLD:
            return Time(year=cc * 100 + y)
        else:
            return Time(year=(cc - 1) * 100 + y)
    else:
        return Time(year=y)


@rule(
    r"heute|(um diese zeit|zu dieser zeit|um diesen zeitpunkt|zu diesem zeitpunkt)|"
    "todays?|(at this time)"
)
def ruleToday(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch) -> Time:
    return Time(year=ts.year, month=ts.month, day=ts.day)


@rule(
    r"(genau\s*)?jetzt|diesen moment|in diesem moment|gerade eben|"
    r"((just|right)\s*)?now|immediately"
)
def ruleNow(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch) -> Time:
    return Time(
        year=ts.year, month=ts.month, day=ts.day, hour=ts.hour, minute=ts.minute
    )


@rule(r"(morgen){e<=1}|tmrw?|(tomm?or?rows?){e<=1}|tom")
def ruleTomorrow(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch) -> Time:
    dm = ts + relativedelta(days=1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(r"übermorgen")
def ruleAfterTomorrow(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch) -> Time:
    dm = ts + relativedelta(days=2)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(r"gestern|yesterdays?")
def ruleYesterday(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch) -> Time:
    dm = ts + relativedelta(days=-1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(r"vor\s?gestern")
def ruleBeforeYesterday(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch) -> Time:
    dm = ts + relativedelta(days=-2)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(r"(das )?ende (des|dieses) monats?|(the )?(\bEOM\b|end of (the )?month)")
def ruleEOM(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch) -> Time:
    dm = ts + relativedelta(day=1, months=1, days=-1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(
    r"(das )?(\bEOY\b|jahr(es)? ?ende|ende (des )?jahr(es)?)|"
    r"(the )?(\bEOY\b|end of (the )?year)"
)
def ruleEOY(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch) -> Time:
    dm = ts + relativedelta(day=1, month=1, years=1, days=-1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(predicate("isDOM"), predicate("isMonth"))
def ruleDOMMonth(ts: datetime, pm_bias: bool, date_format: str, dom: Time, m: Time) -> Time:
    return Time(day=dom.day, month=m.month)


@rule(predicate("isDOM"), r"of", predicate("isMonth"))
def ruleDOMMonth2(ts: datetime, pm_bias: bool, date_format: str, dom: Time, _: RegexMatch, m: Time) -> Time:
    return Time(day=dom.day, month=m.month)


@rule(predicate("isMonth"), predicate("isDOM"))
def ruleMonthDOM(ts: datetime, pm_bias: bool, date_format: str, m: Time, dom: Time) -> Time:
    return Time(month=m.month, day=dom.day)


@rule(r"am|diese(n|m)|at|on|this", predicate("isDOW"))
def ruleAtDOW(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch, dow: Time) -> Time:
    dm = ts + relativedelta(weekday=dow.DOW)
    if dm.date() == ts.date():
        dm += relativedelta(weeks=1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(
    r"((am )?(dem |den )?((kommenden?|nächsten?)( Woche)?))|"
    "((on |at )?(the )?((next|following)( week)?))",
    predicate("isDOW"),
)
def ruleNextDOW(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch, dow: Time) -> Time:
    dm = ts + relativedelta(weekday=dow.DOW, weeks=1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(predicate("isDOW"), r"((kommende|nächste) Woche)|((next|following) week)")
def ruleDOWNextWeek(ts: datetime, pm_bias: bool, date_format: str, dow: Time, _: RegexMatch) -> Time:
    dm = ts + relativedelta(weekday=dow.DOW, weeks=1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(predicate("isDOY"), predicate("isYear"))
def ruleDOYYear(ts: datetime, pm_bias: bool, date_format: str, doy: Time, y: Time) -> Time:
    return Time(year=y.year, month=doy.month, day=doy.day)


@rule(predicate("isDOW"), predicate("isPOD"))
def ruleDOWPOD(ts: datetime, pm_bias: bool, date_format: str, dow: Time, pod: Time) -> Time:
    return Time(DOW=dow.DOW, POD=pod.POD)


@rule(predicate("isDOW"), predicate("isDOM"))
def ruleDOWDOM(ts: datetime, pm_bias: bool, date_format: str, dow: Time, dom: Time) -> Time:
    # Monday 5th
    # Find next date at this day of week and day of month
    dm = rrule(MONTHLY, dtstart=ts, byweekday=dow.DOW, bymonthday=dom.day, count=1)[0]
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(predicate("hasDOW"), predicate("isDate"))
def ruleDOWDate(ts: datetime, pm_bias: bool, date_format: str, dow: Time, date: Time) -> Time:
    # Monday 5th December - ignore DOW, but carry over e.g. POD from dow
    return Time(date.year, date.month, date.day, POD=dow.POD)


@rule(predicate("isDate"), predicate("hasDOW"))
def ruleDateDOW(ts: datetime, pm_bias: bool, date_format: str, date: Time, dow: Time) -> Time:
    # Monday 5th December - ignore DOW, but carry over e.g. POD from dow
    return Time(date.year, date.month, date.day, POD=dow.POD)


# LatentX: handle time entities that are not grounded to a date yet
# and assume the next date+time in the future
@rule(predicate("isDOM"))
def ruleLatentDOM(ts: datetime,pm_bias: bool, date_format: str, dom: Time) -> Time:
    dm = ts + relativedelta(day=dom.day)
    if dm <= ts:
        dm += relativedelta(months=1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(predicate("isDOW"))
def ruleLatentDOW(ts: datetime, pm_bias: bool, date_format: str, dow: Time) -> Time:
    dm = ts + relativedelta(weekday=dow.DOW)
    if dm <= ts:
        dm += relativedelta(weeks=1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(predicate("isDOY"))
def ruleLatentDOY(ts: datetime, pm_bias: bool, date_format: str, doy: Time) -> Time:
    dm = ts + relativedelta(month=doy.month, day=doy.day)
    if dm < ts:
        dm += relativedelta(years=1)
    return Time(year=dm.year, month=dm.month, day=dm.day)


@rule(predicate("isPOD"))
def ruleLatentPOD(ts: datetime, pm_bias: bool, date_format: str, pod: Time) -> Time:
    # Set the time to the pre-defined POD values, but keep the POD
    # information. The date is chosen based on what ever is the next
    # possible slot for these times
    h_from, h_to = pod_hours[pod.POD]
    t_from = ts + relativedelta(hour=h_from, minute=0)
    if t_from <= ts:
        t_from += relativedelta(days=1)
    return Time(year=t_from.year, month=t_from.month, day=t_from.day, POD=pod.POD)


@rule(
    r"(?<!\d|\.)(?P<day>(?&_day))[\.\/]"  # removed \-
    r"((?P<month>(?&_month))|(?P<named_month>({})))\.?"
    r"(?!\d|am|\s*pm)".format(_rule_months),
    date_format="EU"
)
# do not allow dd.ddam, dd.ddpm, but allow dd.dd am - e.g. in the German
# "13.06 am Nachmittag"
def ruleDDMM(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    if m.match.group("month"):
        month = int(m.match.group("month"))
    else:
        for i, (name, _) in enumerate(_months):
            if m.match.group(name):
                month = i + 1
    day = int(m.match.group("day"))
    # TODO remove the hack below and extend the DDMM and MMDD rules to be more readable and clear.
    if date_format == "US":
        if day <= 12:
            return Time(month=day, day=month)

    return Time(month=month, day=day)


@rule(
    r"(?<!\d|\.)((?P<month>(?&_month))|(?P<named_month>({})))[\.\/]"
    r"(?P<day>(?&_day))"
    r"(?!\d|am|\s*pm)".format(_rule_months),
    date_format="US"
)
def ruleMMDD(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    if m.match.group("month"):
        month = int(m.match.group("month"))
    else:
        for i, (name, _) in enumerate(_months):
            if m.match.group(name):
                month = i + 1
    return Time(month=month, day=int(m.match.group("day")))


@rule(
    r"(?<!\d|\.)(?P<day>(?&_day))[\/\.]"
    r"((?P<month>(?&_month))|(?P<named_month>({})))[\/\.]"
    r"(?P<year>(?&_year))(?!\d)".format(_rule_months),
    date_format="EU"
)
def ruleDDMMYYYY(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    y = int(m.match.group("year"))
    if y < 100:
        y += 2000
    if m.match.group("month"):
        month = int(m.match.group("month"))
    else:
        for i, (name, _) in enumerate(_months):
            if m.match.group(name):
                month = i + 1

    time = Time(year=y, month=month, day=int(m.match.group("day")))
    try:
        time.dt
        return time
    except ValueError:
        return None


@rule(
    r"(?<!\d|\.)\s*((?P<month>(?&_month))|(?P<named_month>({})))\s*[\/\.]"
    r"(?P<day>(?&_day))\s*[\/\.]"
    r"\s*(?P<year>(?&_year))(?!\d)".format(_rule_months),
    date_format="US"
)
def ruleMMDDYYYY(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    y = int(m.match.group("year"))
    if y < 100:
        y += 2000
    if m.match.group("month"):
        month = int(m.match.group("month"))
    else:
        for i, (name, _) in enumerate(_months):
            if m.match.group(name):
                month = i + 1

    day = int(m.match.group("day"))
    time = Time(year=y, month=month, day=day)

    try:
        time.dt
        return time
    except ValueError:
        return None


def _is_valid_military_time(ts: datetime, pm_bias: bool, date_format: str, t: Time) -> bool:
    if t.hour is None or t.minute is None:
        return False

    t_year = t.hour * 100 + t.minute
    # Military times (i.e. no separator) are notriously difficult to
    # distinguish from yyyy; these are some heuristics to avoid an abundance
    # of false positives for hhmm
    #
    # If hhmm is the current year -> assume it is a year
    if t_year == ts.year:
        return False
    # If hhmm is the year in 3 month from now -> same, prefer year
    if t_year == (ts + relativedelta(months=3)).year:
        return False
    # If the minutes is not a multiple of 5 prefer year.
    # Since military times are typically used for flights,
    # and flight times are only multiples of 5, we use this heuristic as evidence
    # for military times.
    if t.minute % 5:
        return False
    return True


def _maybe_apply_am_pm(t: Time, pm_bias: bool, date_format: str, ampm_match: str) -> Time:
    # add pm_bias, to access
    if not t.hour:
        return t
    if ampm_match is None:
        if not pm_bias:
            return Time(hour=t.hour, minute=t.minute)

        # PM bias
        if t.hour < 12:
            return Time(hour=t.hour + 12, minute=t.minute)
        else:
            t.period = "pm"
            return t

    if ampm_match.lower().startswith("a") and t.hour <= 12:
        if t.hour == 12:
            t.hour = 0
        t.period = "am"
        return t

    if ampm_match.lower().startswith("p") and t.hour < 12:
        return Time(hour=t.hour + 12, minute=t.minute, period='pm')
    # the case ampm_match.startswith('a') and t.hour >
    # 12 (e.g. 13:30am) makes no sense, lets ignore the ampm
    # likewise if hour >= 12 no 'pm' action is needed
    return t


@rule(
    # match hhmm
    r"(?<!\d|\.)(?P<hour>(?:[01]\d)|(?:2[0-3]))(?P<minute>(?&_minute))"
    r"\s*(?P<clock>uhr|h)?"  # optional uhr
    r"\s*(?P<ampm>\s*[ap]\.?m\.?)?(?!\d)"  # optional am/pm
)
def ruleHHMMmilitary(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Time]:
    t = Time(hour=int(m.match.group("hour")), minute=int(m.match.group("minute") or 0))
    if m.match.group("clock") or _is_valid_military_time(ts, pm_bias, date_format, t):
        return _maybe_apply_am_pm(t, pm_bias, date_format, m.match.group("ampm"))
    return None


@rule(
    r"(?<!\d)"  # We don't start matching with another number, or a dot
    r"(?P<hour>(?&_hour))"  # We certainly match an hour
    # We try to match also the minute
    r"((?P<sep>:|uhr|h|)(?P<minute>(?&_minute)))?"
    r"\s*(?P<clock>uhr|h)?"  # We match uhr with no minute
    r"(?P<ampm>\s*[ap]\.?m\.?)?"  # AM PM
    r"(?!\d)"
    r"(?<![a-zA-Z])-?\d+" # handle acr-01
)
def ruleHHMM(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    # hh [am|pm]
    # hh:mm
    # hhmm
    t = Time(hour=int(m.match.group("hour")), minute=int(m.match.group("minute") or 0))
    return _maybe_apply_am_pm(t, pm_bias, date_format, m.match.group("ampm"))


@rule(r"(?<!\d|\.)(?P<hour>(?&_hour))\s*(uhr|h|o\'?clock)")
def ruleHHOClock(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Time:
    return Time(hour=int(m.match.group("hour")))


@rule(r"(a |one )?quarter( to| till| before| of)|vie?rtel vor", predicate("isTOD"))
def ruleQuarterBeforeHH(ts: datetime, pm_bias: bool, date_format:str, _: RegexMatch, t: Time) -> Optional[Time]:
    # no quarter past hh:mm where mm is not 0 or missing
    if t.minute:
        return None
    if t.hour > 0:
        return Time(hour=t.hour - 1, minute=45)
    else:
        return Time(hour=23, minute=45)


@rule(r"((a |one )?quarter( after| past)|vie?rtel nach)", predicate("isTOD"))
def ruleQuarterAfterHH(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch, t: Time) -> Optional[Time]:
    if t.minute:
        return None
    return Time(hour=t.hour, minute=15)


@rule(r"halfe?( to| till| before| of)?|halb( vor)?", predicate("isTOD"))
def ruleHalfBeforeHH(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch, t: Time) -> Optional[Time]:
    if t.minute:
        return None
    if t.hour > 0:
        return Time(hour=t.hour - 1, minute=30)
    else:
        return Time(hour=23, minute=30)


@rule(r"halfe?( after| past)|halb nach", predicate("isTOD"))
def ruleHalfAfterHH(ts: datetime, pm_bias: bool, date_format: str, _: RegexMatch, t: Time) -> Optional[Time]:
    if t.minute:
        return None
    return Time(hour=t.hour, minute=30)


@rule(predicate("isTOD"), predicate("isPOD"))
def ruleTODPOD(ts: datetime, pm_bias: bool, date_format: str, tod: Time, pod: Time) -> Optional[Time]:
    # time of day may only be an hour as in "3 in the afternoon"; this
    # is only relevant for time <= 12
    if tod.hour < 12 and (
        "afternoon" in pod.POD
        or "evening" in pod.POD
        or "night" in pod.POD
        or "last" in pod.POD
    ):
        h = tod.hour + 12
    elif tod.hour > 12 and (
        "forenoon" in pod.POD or "morning" in pod.POD or "first" in pod.POD
    ):
        # 17Uhr morgen -> do not merge
        return None
    else:
        h = tod.hour
    return Time(hour=h, minute=tod.minute)


@rule(predicate("isPOD"), predicate("isTOD"))
def rulePODTOD(ts: datetime, pm_bias: bool, date_format: str, pod: Time, tod: Time) -> Optional[Time]:
    return cast(Time, ruleTODPOD(ts, pm_bias, date_format, tod, pod))


@rule(predicate("isDate"), predicate("isTOD"))
def ruleDateTOD(ts: datetime, pm_bias: bool, date_format: str, date: Time, tod: Time) -> Time:
    return Time(
        year=date.year, month=date.month, day=date.day, hour=tod.hour, minute=tod.minute
    )


@rule(predicate("isTOD"), predicate("isDate"))
def ruleTODDate(ts: datetime, pm_bias: bool, date_format: str, tod: Time, date: Time) -> Time:
    return Time(
        year=date.year, month=date.month, day=date.day, hour=tod.hour, minute=tod.minute
    )


@rule(predicate("isDate"), predicate("isPOD"))
def ruleDatePOD(ts: datetime, pm_bias: bool, date_format: str, d: Time, pod: Time) -> Time:
    return Time(year=d.year, month=d.month, day=d.day, POD=pod.POD)


@rule(predicate("isPOD"), predicate("isDate"))
def rulePODDate(ts: datetime, pm_bias: bool, date_format: str, pod: Time, d: Time) -> Time:
    return Time(year=d.year, month=d.month, day=d.day, POD=pod.POD)


@rule(
    r"((?P<not>not |nicht )?(vor|before))|(bis )?spätestens( bis)?|bis|latest",
    dimension(Time),
)
def ruleBeforeTime(ts: datetime, pm_bias: bool, date_format: str, r: RegexMatch, t: Time) -> Interval:
    if r.match.group("not"):
        return Interval(t_from=t, t_to=None)
    else:
        return Interval(t_from=None, t_to=t)


@rule(
    r"((?P<not>not |nicht )?(nach|after))|(ab )?frühe?stens( ab)?|ab|"
    "(from )?earliest( after)?|from",
    dimension(Time),
)
def ruleAfterTime(ts: datetime, pm_bias: bool, date_format: str, r: RegexMatch, t: Time) -> Interval:
    if r.match.group("not"):
        return Interval(t_from=None, t_to=t)
    else:
        return Interval(t_from=t, t_to=None)


@rule(predicate("isDate"), _regex_to_join, predicate("isDate"))
def ruleDateDate(ts: datetime, pm_bias: bool, date_format: str, d1: Time, _: RegexMatch, d2: Time) -> Optional[Interval]:
    if d1.year > d2.year:
        return None
    if d1.year == d2.year and d1.month > d2.month:
        return None
    if d1.year == d2.year and d1.month == d2.month and d1.day >= d2.day:
        return None
    return Interval(t_from=d1, t_to=d2)


@rule(predicate("isDOM"), _regex_to_join, predicate("isDate"))
def ruleDOMDate(ts: datetime, pm_bias: bool, date_format: str, d1: Time, _: RegexMatch, d2: Time) -> Optional[Interval]:
    if d1.day >= d2.day:
        return None
    return Interval(t_from=Time(year=d2.year, month=d2.month, day=d1.day), t_to=d2)


@rule(predicate("isDate"), _regex_to_join, predicate("isDOM"))
def ruleDateDOM(ts: datetime, pm_bias: bool, date_format: str, d1: Time, _: RegexMatch, d2: Time) -> Optional[Interval]:
    if d1.day >= d2.day:
        return None
    return Interval(t_from=d1, t_to=Time(year=d1.year, month=d1.month, day=d2.day))


@rule(predicate("isDOY"), _regex_to_join, predicate("isDate"))
def ruleDOYDate(ts: datetime, pm_bias: bool, date_format: str, d1: Time, _: RegexMatch, d2: Time) -> Optional[Interval]:
    if d1.month > d2.month:
        return None
    elif d1.month == d2.month and d1.day >= d2.day:
        return None
    return Interval(t_from=Time(year=d2.year, month=d1.month, day=d1.day), t_to=d2)


@rule(predicate("isDateTime"), _regex_to_join, predicate("isDateTime"))
def ruleDateTimeDateTime(
    ts: datetime, pm_bias: bool, date_format: str, d1: Time, _: RegexMatch, d2: Time
) -> Optional[Interval]:
    if d1.year > d2.year:
        return None
    if d1.year == d2.year and d1.month > d2.month:
        return None
    if d1.year == d2.year and d1.month == d2.month and d1.day > d2.day:
        return None
    if (
        d1.year == d2.year
        and d1.month == d2.month
        and d1.day == d2.day
        and d1.hour > d2.hour
    ):
        return None
    if (
        d1.year == d2.year
        and d1.month == d2.month
        and d1.day == d2.day
        and d1.hour == d2.hour
        and d1.minute >= d2.minute
    ):
        return None
    return Interval(t_from=d1, t_to=d2)


@rule(predicate("isTOD"), _regex_to_join, predicate("isTOD"))
def ruleTODTOD(ts: datetime, pm_bias: bool, date_format: str, t1: Time, _: RegexMatch, t2: Time) -> Interval:
    if not pm_bias:
        if (t2.hour < t1.hour):
            if t2.hour < 12:
                t2.hour += 12

            return Interval(t_from=t1, t_to=t2)

    # 9-5 handling on pm bias
    if (t2.hour < t1.hour) and (t2.hour >= 12 and t1.hour >= 12):
        t1.hour -= 12
        return Interval(t_from=t1, t_to=t2)
    # am override
    if not t1.period and t2.period == "am" and t1.hour > 12:
        t1.hour -= 12
        return Interval(t_from=t1, t_to=t2)
    else:
        return Interval(t_from=t1, t_to=t2)


@rule(predicate("isPOD"), _regex_to_join, predicate("isPOD"))
def rulePODPOD(ts: datetime, pm_bias: bool, date_format: str, t1: Time, _: RegexMatch, t2: Time) -> Interval:
    return Interval(t_from=t1, t_to=t2)


@rule(predicate("isDate"), dimension(Interval))
def ruleDateInterval(ts: datetime, pm_bias: bool, date_format: str, d: Time, i: Interval) -> Optional[Interval]:
    if not (
        (i.t_from is None or i.t_from.isTOD or i.t_from.isPOD)
        and (i.t_to is None or i.t_to.isTOD or i.t_to.isPOD)
    ):
        return None
    t_from = t_to = None
    if i.t_from is not None:
        t_from = Time(
            year=d.year,
            month=d.month,
            day=d.day,
            hour=i.t_from.hour,
            minute=i.t_from.minute,
            POD=i.t_from.POD,
        )
    if i.t_to is not None:
        t_to = Time(
            year=d.year,
            month=d.month,
            day=d.day,
            hour=i.t_to.hour,
            minute=i.t_to.minute,
            POD=i.t_to.POD,
        )
    if t_from and t_to and t_from.dt >= t_to.dt:
        t_to_dt = t_to.dt + relativedelta(days=1)
        t_to = Time(
            year=t_to_dt.year,
            month=t_to_dt.month,
            day=t_to_dt.day,
            hour=t_to_dt.hour,
            minute=t_to_dt.minute,
            POD=t_to.POD,
        )
    return Interval(t_from=t_from, t_to=t_to)


@rule(dimension(Interval), predicate("isDate"))
def ruleIntervalDate(ts: datetime, pm_bias: bool, date_format: str, i: Interval, d: Time) -> Optional[Interval]:
    if not (
        (i.t_from is None or i.t_from.isTOD or i.t_from.isPOD)
        and (i.t_to is None or i.t_to.isTOD or i.t_to.isPOD)
    ):
        return None
    t_from = t_to = None
    if i.t_from is not None:
        t_from = Time(
            year=d.year,
            month=d.month,
            day=d.day,
            hour=i.t_from.hour,
            minute=i.t_from.minute,
            POD=i.t_from.POD,
        )
    if i.t_to is not None:
        t_to = Time(
            year=d.year,
            month=d.month,
            day=d.day,
            hour=i.t_to.hour,
            minute=i.t_to.minute,
            POD=i.t_to.POD,
        )
    if t_from and t_to and t_from.dt >= t_to.dt:
        t_to_dt = t_to.dt + relativedelta(days=1)
        t_to = Time(
            year=t_to_dt.year,
            month=t_to_dt.month,
            day=t_to_dt.day,
            hour=t_to_dt.hour,
            minute=t_to_dt.minute,
            POD=t_to.POD,
        )
    return Interval(t_from=t_from, t_to=t_to)


@rule(predicate("isPOD"), dimension(Interval))
def rulePODInterval(ts: datetime, pm_bias: bool, date_format: str, p: Time, i: Interval) -> Optional[Interval]:
    def _adjust_h(t: Time) -> Optional[int]:
        if t.hour is None:
            return None
        if t.hour < 12 and (
            "afternoon" in p.POD
            or "evening" in p.POD
            or "night" in p.POD
            or "last" in p.POD
        ):
            return t.hour + 12
        else:
            return t.hour

    # only makes sense if i is a time interval
    if not (
        (i.t_from is None or i.t_from.hasTime) and (i.t_to is None or i.t_to.hasTime)
    ):
        return None
    t_to = t_from = None
    if i.t_to is not None:
        t_to = Time(
            year=i.t_to.year,
            month=i.t_to.month,
            day=i.t_to.day,
            hour=_adjust_h(i.t_to),
            minute=i.t_to.minute,
            DOW=i.t_to.DOW,
        )
    if i.t_from is not None:
        t_from = Time(
            year=i.t_from.year,
            month=i.t_from.month,
            day=i.t_from.day,
            hour=_adjust_h(i.t_from),
            minute=i.t_from.minute,
            DOW=i.t_from.DOW,
        )
    return Interval(t_from=t_from, t_to=t_to)


# We add named numbers at least until 31 (max number of days in a month)
_named_number = (
    (1, r"an?|one|ein[es]?"),
    (2, r"two|zwei"),
    (3, r"three|drei"),
    (4, r"four|vier"),
    (5, r"five|fünf"),
    (6, r"six|sechs"),
    (7, r"seven|sieben"),
    (8, r"eight|acht"),
    (9, r"nine|neun"),
    (10, r"ten|zehn"),
    (11, r"eleven|elf"),
    (12, r"twelve|zwölf"),
    (13, r"thirteen|dreizehn"),
    (14, r"fourteen|vierzehn"),
    (15, r"fifteen|fünfzehn"),
    (16, r"sixteen|sechszehn"),
    (17, r"seventeen|siebzehn"),
    (18, r"eighteen|achtzehn"),
    (19, r"nineteen|neunzehn"),
    (20, r"twenty|zwanzig"),
    (21, r"twentyone|einund?zwanzig"),
    (22, r"twentytwo|zweiund?zwanzig"),
    (23, r"twentythree|dreiund?zwanzig"),
    (24, r"twentyfour|vierund?zwanzig"),
    (25, r"twentyfive|fünfund?zwanzig"),
    (26, r"twentysix|sechsund?zwanzig"),
    (27, r"twentyseven|siebenud?zwanzig"),
    (28, r"twentyeight|achtund?zwanzig"),
    (29, r"twentynine|neunund?zwanzig"),
    (30, r"thirty|drei(ß|ss)ig"),
    (31, r"thirtyone|einundrei(ß|ss)ig"),
)
_rule_named_number = "|".join(
    r"(?P<n_{}>{}\b)".format(n, expr) for n, expr in _named_number
)
_rule_named_number = r"({})\s*".format(_rule_named_number)

_durations = [
    (DurationUnit.NIGHTS, r"\bn[aä]chte?\b|\bnights?\b|\b[üu]bernachtung\b"),
    (DurationUnit.DAYS, r"\btage?\b|days?|d"),
    (DurationUnit.MINUTES, r"\bmins?\b|m(inute[ns]?)?"),
    (DurationUnit.HOURS, r"\bstunden?\b|h(ours?)?|h|hrs?"),
    (DurationUnit.WEEKS, r"weeks?|\bwochen?\b|w"),
    (DurationUnit.MONTHS, r"\bmonate?\b|\bmonths?\b"),
    (DurationUnit.YEARS, r'\bjahre?\b|\byears?\b|\by\b|\byrs?\b'),
]

_rule_durations = r"|".join(
    r"(?P<d_{}>{}\b)".format(dur.value, expr) for dur, expr in _durations
)
_rule_durations = r"({})\s*".format(_rule_durations)


# Rules regarding durations
@rule(r"(in)\s*" + r"(?P<num>\d+)\s*" + _rule_durations)
def ruleDigitDuration(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Duration]:
    # 1 day, 1 night etc.
    num = m.match.group("num")
    if num:
        for n, _, in _durations:
            unit = m.match.group("d_" + n.value)
            if unit:
                return Duration(int(num), n)

    return None


@rule(r"(in)\s*" + _rule_named_number + _rule_durations)
def ruleNamedNumberDuration(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Duration]:
    # one day, two nights, thirty days etc.
    num = None
    for n, _ in _named_number:
        match = m.match.group("n_{}".format(n))
        if match:
            num = n
            continue

    if num:
        for d, _, in _durations:
            unit = m.match.group("d_" + d.value)
            if unit:
                return Duration(num, d)

    return None


@rule(r"(in)\s*" + r"(hal[fb]e?|1/2)(\s+an?)?\s*" + _rule_durations)
def ruleDurationHalf(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Duration]:
    # half day, half hour, 1/2 hour
    for n, _, in _durations:
        if m.match.group("d_" + n.value):
            if n == DurationUnit.HOURS:
                return Duration(30, DurationUnit.MINUTES)
            if n == DurationUnit.DAYS:
                return Duration(12, DurationUnit.HOURS)

    return None

# discarding these rules for now and adding their functional counterparts below.
# These have no use case for us at the moment
# TODO: update corpus.py and auto_corpus.py

# @rule(predicate("isDateInterval"), r"f[üo]r", dimension(Duration))
# def ruleIntervalConjDuration(
#     ts: datetime, interval: Interval, _: RegexMatch, dur: Duration
# ) -> Optional[Interval]:
#     # Example: people tend to repeat themselves when specifying durations
#     # 15-16 Nov für 1 Nacht
#     return ruleDurationInterval(ts, dur, interval)  # type: ignore


# @rule(predicate("isDateInterval"), dimension(Duration))
# def ruleIntervalDuration(
#     ts: datetime, interval: Interval, dur: Duration
# ) -> Optional[Interval]:
#     # Variant without conjunction
#     # 15-16 Nov 1 Nacht
#     return ruleDurationInterval(ts, dur, interval)  # type: ignore
#
#
# @rule(dimension(Duration), predicate("isDateInterval"))
# def ruleDurationInterval(
#     ts: datetime, dur: Duration, interval: Interval
# ) -> Optional[Interval]:
#     # 3 days 15-18 Nov
#     delta = interval.t_to.dt - interval.t_from.dt
#     dur_delta = _duration_to_relativedelta(dur)
#     if delta.days == dur_delta.days:
#         return interval
#     return None
#
@rule(dimension(Time), "(for)\s*" + r"(?P<num>\d+)\s*" + _rule_durations)
def ruleIntervalFromDuration(
    ts: datetime, pm_bias: bool, date_format: str, t: Time, m: RegexMatch,
) -> Optional[Interval]:
    # task 8pm for 30 minutes
    dur = ruleDigitDuration(ts, pm_bias, date_format, m)

    if t.hasDate:
        time_dt = t.dt
    else:
        t.day, t.month, t.year = ts.day, ts.month, ts.year
        time_dt = t.dt

    if dur.unit in (
        DurationUnit.DAYS,
        DurationUnit.NIGHTS,
        DurationUnit.WEEKS,
        DurationUnit.MONTHS,
    ):
        delta = _duration_to_relativedelta(dur)
        end_ts = time_dt + delta
        end = Time(year=end_ts.year, month=end_ts.month, day=end_ts.day)
        if t.hour:
            end = Time(year=end_ts.year, month=end_ts.month, day=end_ts.day, hour=end_ts.hour, minute=end_ts.minute)
        return Interval(t_from=t, t_to=end)

    if dur.unit in (DurationUnit.HOURS, DurationUnit.MINUTES):
        delta = _duration_to_relativedelta(dur)
        end_ts = time_dt + delta
        end = Time(
            year=end_ts.year,
            month=end_ts.month,
            day=end_ts.day,
            hour=end_ts.hour,
            minute=end_ts.minute,
        )
        return Interval(t_from=t, t_to=end)
    return None


def _duration_to_relativedelta(dur: Duration) -> relativedelta:
    return {
        DurationUnit.DAYS: relativedelta(days=dur.value),
        DurationUnit.NIGHTS: relativedelta(days=dur.value),
        DurationUnit.WEEKS: relativedelta(weeks=dur.value),
        DurationUnit.MONTHS: relativedelta(months=dur.value),
        DurationUnit.HOURS: relativedelta(hours=dur.value),
        DurationUnit.MINUTES: relativedelta(minutes=dur.value),
    }[dur.unit]


@rule(dimension(Time), dimension(Duration))
def ruleTimeDuration(ts: datetime, pm_bias: bool, date_format: str, t: Time, d: Duration) -> Time:
    # beer 4am in 3 days
    delta = d.time(ts)
    time = Time(
        year=delta.year,
        month=delta.month,
        day=delta.day,
        hour=t.hour,
        minute=t.minute
    )
    return time


@rule(dimension(Duration), dimension(Time))
def ruleDurationTime(ts: datetime, pm_bias: bool, date_format: str, d: Duration, t: Time) -> Time:
    # beer in 3 days 4am
    delta = d.time(ts)
    time = Time(
        year=delta.year,
        month=delta.month,
        day=delta.day,
        hour=t.hour,
        minute=t.minute
    )
    return time


@rule(dimension(Duration), dimension(Interval))
def ruleDurationInterval(ts: datetime, pm_bias: bool, date_format: str, d: Duration, i: Interval) -> Interval:
    # beer in 3 days 4-6pm

    if not i.isTimeInterval:
        return None

    delta = d.time(ts)
    start_time = Time(
        year=delta.year,
        month=delta.month,
        day=delta.day,
        hour=i.t_from.hour,
        minute=i.t_from.minute
    )
    end_time = Time(
        year=delta.year,
        month=delta.month,
        day=delta.day,
        hour=i.t_to.hour,
        minute=i.t_to.minute
    )
    return Interval(t_from=start_time, t_to=end_time)


@rule(dimension(Interval), dimension(Duration))
def ruleIntervalDuration(ts: datetime, pm_bias: bool, date_format: str, i: Interval, d: Duration) -> Interval:

    # beer 4-6pm in 3 days
    # TODO: "4-6 in 3 days" doesn't work

    if not i.isTimeInterval:
        return None

    delta = d.time(ts)
    start_time = Time(
        year=delta.year,
        month=delta.month,
        day=delta.day,
        hour=i.t_from.hour,
        minute=i.t_from.minute
    )
    end_time = Time(
        year=delta.year,
        month=delta.month,
        day=delta.day,
        hour=i.t_to.hour,
        minute=i.t_to.minute
    )
    return Interval(t_from=start_time, t_to=end_time)


######### Recurring events #########

_named_interval = (
    (2, r"2|2nd|second|other|two"),
    (3, r"3|3rd|third|three"),
    (4, r"4|4th|four"),
    (5, r"5|5th|five"),
    (6, r"6|6th|six"),
    (7, r"7|7th|seven"),
    (7, r"8|8th|eight"),
    (9, r"9|9th|nine"),
    (10, r"10|10th|ten"),
    (11, r"11|11th|eleven"),
)

_rule_named_interval = "|".join(
    r"(?P<n_{}>{}\b)".format(itv, expr) for itv, expr in _named_interval

)
_rule_named_interval = r"({})\s*".format(_rule_named_interval)

_single_frequencies = [
    (RecurringFrequency.DAILY, r"daily"),
    (RecurringFrequency.WEEKLY, r"weekly"),
    (RecurringFrequency.MONTHLY, r"monthly"),
    (RecurringFrequency.YEARLY, r"yearly"),
]

_rule_single_frequencies = r"|".join(
    r"(?P<f_{}>{}\b)".format(freq.value, expr) for freq, expr in _single_frequencies
)
_rule_single_frequencies = r"({})\s*".format(_rule_single_frequencies)

_frequencies = [
    (RecurringFrequency.DAILY, r"days?|d"),
    (RecurringFrequency.WEEKLY, r"weeks?|w"),
    (RecurringFrequency.MONTHLY, r"months?|m"),
    (RecurringFrequency.YEARLY, r"years?|y"),
]

_rule_frequencies = r"|".join(
    r"(?P<f_{}>{}\b)".format(freq.value, expr) for freq, expr in _frequencies
)
_rule_frequencies = r"({})\s*".format(_rule_frequencies)

_recurring_dows = [
    ("mon", r"\bmontags\b|\bmondays\b|\bmons\.?\b"),
    ("tue", r"\bdie?nstags\b|\bdies\.?\b|\btuesdays\b|\btues\.?\b"),
    ("wed", r"\bmittwochs\b|\bmis\.?\b|\bwednesdays\b|\bweds\.?\b"),
    ("thu", r"\bdonn?erstags\b|\bdons\.?\b|\bthursdays\b|\bthurs\.?\b"),
    ("fri", r"\bfreitags\b|\bfridays\b|\bfris\.?\b"),
    ("sat", r"\bsamstags\b|\bsonnabends\b|\bsaturdays\b|\bsats\.?\b"),
    ("sun", r"\bsonntags\b|\bsos\.?\b|\bsundays\b|\bsuns\.?\b"),
]
_rule_recurring_dows = r"|".join(r"(?P<{}>{})".format(dow, expr) for dow, expr in _recurring_dows)
_rule_recurring_dows = r"({})\s*".format(_rule_recurring_dows)


@rule(_rule_single_frequencies)
def ruleRecurringSingle(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Recurring]:
    # daily / weekly
    for f, _ in _single_frequencies:
        freq = m.match.group("f_" + f.value)
        if freq:
            time = Time(year=ts.year, month=ts.month, day=ts.day)
            return Recurring(f.value, 1, start_time=time, end_time=time)
    return None


# r"(?<!\S)every(?!\S)\s*|(?<!\S)each(?!\S)\s*" old case sensitive regex
@rule(r"(every|each)\s*" + _rule_frequencies)
def ruleRecurring(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Recurring]:
    # every day / every week
    for f, _ in _frequencies:
        freq = m.match.group("f_" + f.value)
        if freq:
            time = Time(year=ts.year, month=ts.month, day=ts.day)
            return Recurring(frequency=f.value, interval=1, start_time=time, end_time=time)

    return None


# r"(?<!\S)every(?!\S)\s*|(?<!\S)each(?!\S)\s*" old case sensitive regex
@rule(r"(every|each)\s*" + _rule_named_interval + _rule_frequencies)
def ruleRecurringIntervals(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Recurring]:
    # every other week / every 2nd day
    for i, _ in _named_interval:
        match = m.match.group("n_{}".format(i))
        if match:
            itv = i
    for f, _ in _frequencies:
        freq = m.match.group("f_" + f.value)
        if freq:
            time = Time(year=ts.year, month=ts.month, day=ts.day)
            return Recurring(frequency=f.value, interval=itv, start_time=time, end_time=time)
    return None


@rule(dimension(Recurring), r"(starting|beginning|from|starts?|begins?)\s*", predicate("isDate"))
def ruleDefinedRecurringIntervals(ts: datetime, pm_bias: bool, date_format: str, r: Recurring, m: RegexMatch, start: Time) -> Optional[Recurring]:
    # every other week from monday / every 2nd day from today / every day starting monday / beer 4am weekly from next monday
    start_time = Time(
        year=start.year,
        month=start.month,
        day=start.day,
        hour=r.start_time.hour or None,
        minute=r.start_time.minute
    )
    end_time = Time(
        year=start.year,
        month=start.month,
        day=start.day,
        hour=r.end_time.hour or None,
        minute=r.end_time.minute
    )

    return Recurring(frequency=r.frequency, interval=r.interval, start_time=start_time, end_time=end_time)


@rule(r"(starting|beginning|from|starts?|begins?)\s*", predicate("isDate"), dimension(Recurring))
def ruleDefinedRecurringIntervals2(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch, start: Time, r: Recurring) -> Optional[Recurring]:
    # beer from 25th every other week
    start_time = Time(
        year=start.year,
        month=start.month,
        day=start.day,
        hour=r.start_time.hour or None,
        minute=r.start_time.minute
    )
    end_time = Time(
        year=start.year,
        month=start.month,
        day=start.day,
        hour=r.end_time.hour or None,
        minute=r.end_time.minute
    )

    return Recurring(frequency=r.frequency, interval=r.interval, start_time=start_time, end_time=end_time)


@rule(dimension(Time), dimension(Recurring))
def ruleRecurringTime(ts: datetime, pm_bias: bool, date_format: str, t: Time, r: Recurring) -> Optional[Recurring]:
    # 4 every day / 4pm daily / 7am tomorrow weekly / friday 4pm daily
    r_time = r.start_time.dt
    if t.hasDate:
        r_time = t.dt

    dm = ts + relativedelta(hour=t.hour, minute=t.minute or 0, day=r_time.day)
    if dm <= ts:
        r_time += relativedelta(days=1)
    time = Time(
        year=r_time.year,
        month=r_time.month,
        day=r_time.day,
        hour=dm.hour,
        minute=dm.minute
    )
    return Recurring(frequency=r.frequency, interval=r.interval, start_time=time, end_time=time, byday=r.byday)


@rule(dimension(Recurring), dimension(Time))
def ruleRecurringTime2(ts: datetime, pm_bias: bool, date_format: str, r: Recurring, t: Time) -> Optional[Recurring]:
    # every day 4 / daily 4pm
    r_time = r.start_time.dt
    if t.hasDate:
        r_time = t.dt

    dm = ts + relativedelta(hour=t.hour, minute=t.minute or 0, day=r_time.day)
    if dm <= ts:
        r_time += relativedelta(days=1)
    time = Time(
        year=r_time.year,
        month=r_time.month,
        day=r_time.day,
        hour=dm.hour,
        minute=dm.minute
    )

    return Recurring(frequency=r.frequency, interval=r.interval, start_time=time, end_time=time, byday=r.byday)


@rule(dimension(Recurring), predicate("isTimeInterval"))
def ruleRecurringTimeInterval(ts: datetime, pm_bias: bool, date_format: str, r: Recurring, t: Interval) -> Optional[Recurring]:
    # every day 4-6 / daily 9-5
    r_time = r.start_time.dt
    dm = ts + relativedelta(hour=t.t_from.hour, minute=t.t_from.minute or 0, day=r_time.day)
    if dm <= ts:
        r_time += relativedelta(days=1)
    start_time = Time(
        year=r_time.year,
        month=r_time.month,
        day=r_time.day,
        hour=t.t_from.hour,
        minute=t.t_from.minute
    )
    end_time = Time(
        year=r_time.year,
        month=r_time.month,
        day=r_time.day,
        hour=t.t_to.hour,
        minute=t.t_to.minute
    )

    return Recurring(frequency=r.frequency, interval=r.interval, start_time=start_time, end_time=end_time, byday=r.byday)


@rule(predicate("isTimeInterval"), dimension(Recurring))
def ruleRecurringTimeInterval2(ts: datetime, pm_bias: bool, date_format: str, t: Interval, r: Recurring) -> Optional[Recurring]:
    # 4-6 every day / 9-5 daily
    r_time = r.start_time.dt
    dm = ts + relativedelta(hour=t.t_from.hour, minute=t.t_from.minute or 0, day=r_time.day)
    if dm <= ts:
        r_time += relativedelta(days=1)
    start_time = Time(
        year=r_time.year,
        month=r_time.month,
        day=r_time.day,
        hour=t.t_from.hour,
        minute=t.t_from.minute
    )
    end_time = Time(
        year=r_time.year,
        month=r_time.month,
        day=r_time.day,
        hour=t.t_to.hour,
        minute=t.t_to.minute
    )

    return Recurring(frequency=r.frequency, interval=r.interval, start_time=start_time, end_time=end_time, byday=r.byday)


@rule(r"(every|each)\s*", predicate("isDOW"))
def ruleRecurringDOW(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch, dow: Time) -> Optional[Recurring]:
    # every thursday
    dm = ts + relativedelta(weekday=dow.DOW)
    if dm <= ts:
        dm += relativedelta(weeks=1)
    time = Time(year=dm.year, month=dm.month, day=dm.day, DOW=dow.DOW)
    return Recurring(frequency=RecurringFrequency.WEEKLY.value, interval=1, start_time=time, end_time=time, byday=dm.weekday())


@rule(r"(every|each)\s*", predicate('isDOY'))
def ruleRecurringDOY(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch, doy: Time) -> Optional[Recurring]:
    # every 23.9 / every september 3rd
    dm = ts + relativedelta(month=doy.month, day=doy.day)
    if dm <= ts:
        dm += relativedelta(years=1)
    time = Time(year=dm.year, month=doy.month, day=doy.day)
    return Recurring(frequency=RecurringFrequency.YEARLY.value, interval=1, start_time=time, end_time=time, byday=dm.weekday())


@rule(r"(every|each)\s*" + _rule_named_interval, predicate("isDOW"))
def ruleRecurringIntervalDOW(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch, dow: Time) -> Optional[Recurring]:
    # every other thursday
    itv = None
    for i, _ in _named_interval:
        match = m.match.group("n_{}".format(i))
        if match:
            itv = i
    dm = ts + relativedelta(weekday=dow.DOW)
    if dm <= ts:
        dm += relativedelta(weeks=1)
    time = Time(year=dm.year, month=dm.month, day=dm.day, DOW=dow.DOW)
    return Recurring(frequency=RecurringFrequency.WEEKLY.value, interval=itv, start_time=time, end_time=time, byday=dm.weekday())


@rule(_rule_recurring_dows)
def ruleRecurringDOWS(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Recurring]:
    # thursdays
    for i, (name, _) in enumerate(_recurring_dows):
        if m.match.group(name):
            dow = i
            dm = ts + relativedelta(weekday=dow)
            if dm <= ts:
                dm += relativedelta(weeks=1)
            time = Time(year=dm.year, month=dm.month, day=dm.day, DOW=dow)
            return Recurring(frequency=RecurringFrequency.WEEKLY.value, interval=1, start_time=time, end_time=time, byday=dm.weekday())
    return None


@rule(dimension(Recurring), r"(and)\s*", dimension(Recurring))
def ruleRecurringSimpleDOWDOW(ts: datetime, pm_bias: bool, date_format: str, rec1: Recurring, m: RegexMatch, rec2: Recurring) -> Optional[Recurring]:
    # thursdays and wednesdays
    return Recurring(frequency=rec1.frequency, interval=rec1.interval, start_time=rec1.start_time, end_time=rec1.end_time, byday=(rec1.start_time.dt.weekday(), rec2.start_time.dt.weekday()))


@rule(r"(every|each)\s*", predicate("isDOW"), r"(and)\s*", predicate("isDOW"))
def ruleRecurringDOWDOW(ts: datetime, pm_bias: bool, date_format: str, m1: RegexMatch, dow1: Time, m2: RegexMatch, dow2: Time) -> Optional[Recurring]:
    # every thursday and wednesday
    dm = ts + relativedelta(weekday=dow1.DOW)
    if dm <= ts:
        dm += relativedelta(weeks=1)
    time1 = Time(year=dm.year, month=dm.month, day=dm.day, DOW=dow1.DOW)

    dm2 = ts + relativedelta(weekday=dow2.DOW)
    if dm2 <= ts:
        dm2 += relativedelta(weeks=1)
    time2 = Time(year=dm2.year, month=dm2.month, day=dm2.day, DOW=dow2.DOW)

    return Recurring(frequency=RecurringFrequency.WEEKLY.value, interval=1, start_time=time1, end_time=time1, byday=(time1.dt.weekday(), time2.dt.weekday()))


@rule(r"(every|each)\s*", predicate("isDOW"), r"(to)\s*", predicate("isDOW"))
def ruleRecurringDOW2DOW(ts: datetime, pm_bias: bool, date_format: str, m1: RegexMatch, dow1: Time, m2: RegexMatch, dow2: Time) -> Optional[Recurring]:
    # every wednesday to monday
    dows = []

    if dow1.DOW < dow2.DOW:
        dows = [day for day in range(dow1.DOW, dow2.DOW+1)]

    elif dow1.DOW > dow2.DOW:
        i = dow1.DOW
        dows.append(i)
        while i != dow2.DOW:
            if i == 6:
                i = 0
                dows.append(i)
                continue
            i += 1
            dows.append(i)

    dows = tuple(dows)

    for dow in dows:
        dm = ts + relativedelta(weekday=dow)
        if dm <= ts:
            dm += relativedelta(weeks=1)
            time = Time(year=dm.year, month=dm.month, day=dm.day)
        if dm >= ts:
            dm += relativedelta(weekday=dow)
            time = Time(year=dm.year, month=dm.month, day=dm.day)

    return Recurring(frequency=RecurringFrequency.WEEKLY.value, interval=1, start_time=time, end_time=time,
                     byday=dows)


# TODO 5-6 not working
@rule(r"(weekdays|every weekday)\s*")
def ruleRecurringWeekdays(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch) -> Optional[Recurring]:
    # weekdays 5-6 / every weekday 4pm
    dows = (0, 1, 2, 3, 4)

    for dow in dows:
        dm = ts + relativedelta(weekday=dow)
        if dm <= ts:
            dm += relativedelta(weeks=1)
            time = Time(year=dm.year, month=dm.month, day=dm.day)
        if dm >= ts:
            dm += relativedelta(weekday=dow)
            time = Time(year=dm.year, month=dm.month, day=dm.day)

    return Recurring(frequency=RecurringFrequency.WEEKLY.value, interval=1, start_time=time, end_time=time,
                     byday=dows)


@rule(dimension(Duration), dimension(Recurring))
def ruleDurationRecurring(ts: datetime, pm_bias: bool, date_format: str, d: Duration, r: Recurring) -> Optional[Recurring]:
    # beer in 3 days every week
    dur = d.time(ts=ts)
    time = Time(
        year=dur.year,
        month=dur.month,
        day=dur.day
    )
    return Recurring(frequency=r.frequency, interval=r.interval, start_time=time, end_time=time, byday=dur.dt.weekday())


@rule(r"(next)\s*" + _rule_durations)
def ruleNextFrequency(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch):
    for n, _, in _durations:
        unit = m.match.group("d_" + n.value)
        if unit:
            if unit == "week":
                d = ts + relativedelta(days=7)
                return Time(
                    year=d.year,
                    month=d.month,
                    day=d.day,
                )
            if unit == "month":
                d = ts + relativedelta(months=1)
                return Time(
                    year=d.year,
                    month=d.month,
                    day=d.day,
                )
    return None


@rule(r"(last)\s*" + _rule_dows)
def ruleLastDOM(ts: datetime, pm_bias: bool, date_format: str, m: RegexMatch):
    # last monday of the month
    for i, (name, _) in enumerate(_dows):
        if m.match.group(name):
            dom = i
            break
    last_dom = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1)
    while True:
        last_dom -= timedelta(days=1)
        if last_dom.weekday() == dom:
            return Time(month=last_dom.month, day=last_dom.day)

    return None
