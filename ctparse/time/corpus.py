corpus = [
    # ruleYear
    ("Time[]{2019-X-X X:X (X/X)}", "2018-03-07T12:43", ["2019"]),
    # ruleToday
    (
        "Time[]{2018-03-07 X:X (X/X)}",
        "2018-03-07T12:43",
        ["heute", "zu dieser zeit", "today"],
    ),
    # ruleNow
    (
        "Time[]{2018-03-07 12:43 (X/X)}",
        "2018-03-07T12:43",
        ["jetzt", "genau jetzt", "gerade eben", "rightnow", "just now"],
    ),
    # ruleTomorrow
    ("Time[]{2019-01-01 X:X (X/X)}", "2018-12-31T12:43", ["morgen", "tomorrow", "tom", "tmrw"]),
    # ruleAfterTomorrow
    ("Time[]{2019-01-02 X:X (X/X)}", "2018-12-31T12:43", ["übermorgen"]),
    # ruleTomorrow + time
    (
        "Time[]{2019-01-01 19:25 (X/X)}",
        "2018-12-31T12:43",
        ["morgen 19:25", "tomorrow 7:25 pm"],
    ),
    # ruleYesterday
    # test on a leap-year
    ("Time[]{2020-02-29 X:X (X/X)}", "2020-03-01T12:43", ["gestern", "yesterday"]),
    # ruleBeforeYesterday
    # test on a leap-year
    ("Time[]{2020-02-28 X:X (X/X)}", "2020-03-01T12:43", ["vorgestern"]),
    # ruleEOM
    (
        "Time[]{2018-03-31 X:X (X/X)}",
        "2018-03-07T12:43",
        ["ende des Monats", "eom", "end of the month"],
    ),
    # ruleEOY
    (
        "Time[]{2018-12-31 X:X (X/X)}",
        "2018-03-07T12:43",
        ["ende des Jahres", "eoy", "end of the year"],
    ),
    # ruleNamedDOW
    ("Time[]{2018-03-12 X:X (X/X)}", "2018-03-07T12:43", ["Montag", "mon", "monday"]),
    (
        "Time[]{2018-03-13 X:X (X/X)}",
        "2018-03-07T12:43",
        ["Dienstag", "tuesday", "tue"],
    ),
    # ruleNamedDOW + POD
    # ("Time[]{2018-03-12 X:X (X/morning)}", "2018-03-07T12:43", ["Montagmorgen"]),
    # ("Time[]{2018-03-14 X:X (X/forenoon)}", "2018-03-07T12:43", ["Mittwochvormittag"]),
    # ("Time[]{2018-03-10 X:X (X/morning)}", "2018-03-07T12:43", ["Samstagfrüh"]),
    # (
    #     "Time[]{2018-03-11 X:X (X/night)}",
    #     "2018-03-07T12:43",
    #     ["sunday night", "Sonntagnacht"],
    # ),
    # ruleNamedMonth
    ("Time[]{2023-01-01 X:X (X/X)}", "2022-11-28T12:43", ["1st January", "1st jan."]),
    ("Time[]{2023-04-15 X:X (X/X)}", "2022-11-28T12:43", ["15 April", "15 apr."]),
    ("Time[]{X-07-X X:X (X/X)}", "2022-11-28T12:43", ["Juli", "July", "Jul"]),
    (
        "Time[]{2022-12-24 X:X (X/X)}",
        "2022-11-28T12:43",
        ["24 Dezember", "December 24", "24 Dec.", "24 Dez."],
    ),
    # ruleAtDOW
    ("Time[]{2018-03-13 X:X (X/X)}", "2018-03-07T12:43", ["am Dienstag", "on Tue"]),
    (
        "Time[]{2018-03-14 X:X (X/X)}",
        "2018-03-07T12:43",
        ["this Wednesday", "diesen Mittwoch"],
    ),
    # ruleNextDOW
    (
        "Time[]{2018-03-16 X:X (X/X)}",
        "2018-03-07T12:43",
        [
            "am nächsten Freitag",
            "next Friday",
            "nächste Woche Freitag",
            "Friday next week",
            "on the following Friday",
        ],
    ),
    # ruleDOYYear, ruleDDMM, ruleDDMMYYYY
    (
        "Time[]{2018-05-08 X:X (X/X)}",
        "2018-03-07T12:43",
        [
            "8.5.2018",
            "8. Mai 2018",
            "8. Mai 18",
            "8 May 2018",
            "8 May",
            "May 8",
            "8.5.",
            "am 8. Mai 2018",
            "diesen 8. Mai 18",
            "den 8.5.",
            "8th May",
            "8th of May",
            "May 8th",
            "at 8th May",
            "on 8th of May",
            "this May 8th",
            "may 8",
        ],
    ),
    (
        "Time[]{2022-12-24 X:X (X/X)}",
        "2022-11-29T12:43",
        [
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            # "12/24",
            "24/12",
            "24/12",
            "24/12",
        ],
    ),
    # ruleDOWDOM
    (
        "Time[]{2022-11-29 X:X (X/X)}",
        "2022-11-28T12:43",
        ["Tuesday 29th", "Tuesday the 29th", "Dienstag der 29."],
    ),
    (
        "Time[]{2018-06-02 X:X (X/X)}",
        "2018-03-07T12:43",
        ["Saturday 2nd", "Jun 2nd", "am 2ten Juni"],
    ),
    # ruleDOWDate, ruleDateDOW
    (
        "Time[]{2018-05-08 X:X (X/X)}",
        "2018-03-07T12:43",
        ["Tuesday 8.5", "8.5 Tuesday"],
    ),
    # (
    #     "Time[]{2018-05-08 X:X (X/morning)}",
    #     "2018-03-07T12:43",
    #     ["Dienstagmorgen 8.5.", "8.5. Dienstagmorgen"],
    # ),
    # rulePOD, ruleLatentPOD
    # (
    #     "Time[]{2018-03-08 X:X (X/morning)}",
    #     "2018-03-07T12:43",
    #     ["morgens", "früh", "in der früh", "early", "morning"],
    # ),
    # (
    #     "Time[]{2018-03-08 X:X (X/earlymorning)}",
    #     "2018-03-07T12:43",
    #     ["früh morgens", "sehr früh", "early morning"],
    # ),
    # (
    #     "Time[]{2018-03-08 X:X (X/forenoon)}",
    #     "2018-03-07T12:43",
    #     ["vormittags", "forenoon"],
    # ),
    # before noon case
    # (
    #     "Interval[]{None - 2018-03-08 X:X (X/noon)}",
    #     "2018-03-07T12:43",
    #     ["vor mittags", "before noon"],
    # ),
    # (
    #     "Time[]{2018-03-08 X:X (X/afternoon)}",
    #     "2018-03-07T12:43",
    #     ["nachmittag", "afternoon"],
    # ),
    # # past noon case
    # (
    #     "Interval[]{2018-03-08 X:X (X/noon) - None}",
    #     "2018-03-07T12:43",
    #     ["nach mittag", "after noon"],
    # ),
    # ("Time[]{2018-03-08 X:X (X/noon)}", "2018-03-07T12:43", ["mittags", "noon"]),
    # (
    #     "Time[]{2018-03-07 X:X (X/evening)}",
    #     "2018-03-07T12:43",
    #     ["abends", "late", "spät"],
    # ),
    # (
    #     "Time[]{2018-03-07 X:X (X/lateevening)}",
    #     "2018-03-07T12:43",
    #     ["später abend", "very late", "late evening"],
    # ),
    # (
    #     "Time[]{2018-03-08 X:X (X/veryearlyafternoon)}",
    #     "2018-03-07T12:43",
    #     ["sehr früher nachmittag", "very early afternoon"],
    # ),
    # (
    #     "Time[]{2018-03-07 X:X (X/night)}",
    #     "2018-03-07T12:43",
    #     ["heute nacht", "this night", "nachts"],
    # ),
    # # First/Last
    # (
    #     "Time[]{2018-03-08 X:X (X/first)}",
    #     "2018-03-07T12:43",
    #     [
    #         "tomorrow first",
    #         "morgen erster",
    #         "morgen so früh wie möglich",
    #         "tomorrow earliest possible",
    #     ],
    # ),
    # (
    #     "Time[]{2018-03-08 X:X (X/last)}",
    #     "2018-03-07T12:43",
    #     [
    #         "tomorrow last",
    #         "morgen letzter",
    #         "tomorrow as late as possible",
    #         "morgen spätest möglicher",
    #     ],
    # ),
    # (
    #     "Time[]{2018-03-09 X:X (X/first)}",
    #     "2018-03-07T12:43",
    #     ["Friday first", "Freitag erster"],
    # ),
    # (
    #     "Time[]{2018-03-13 X:X (X/last)}",
    #     "2018-03-07T12:43",
    #     ["Tuesday last", "Dienstag letzter"],
    # ),
    # # Date + POD
    # (
    #     "Time[]{2017-01-25 X:X (X/evening)}",
    #     "2018-03-07T12:43",
    #     [
    #         "25.01.2017 abends",
    #         "evening of January 25th 2017",
    #         "25.01.2017 late",
    #         "25.01.2017 spät",
    #         "25.01.2017 (spät)",
    #     ],
    # ),
    # (
    #     "Time[]{2017-01-25 X:X (X/lateafternoon)}",
    #     "2018-03-07T12:43",
    #     [
    #         "25.01.2017 spät nachmittags",
    #         "am 25. Januar 2017 am späten Nachmittag",
    #         "am 25. Januar 2017 am späten Nachmittag",
    #         "am 25. Januar 2017 am späten Nachmittag",
    #         "late afternoon of January 25th 2017",
    #     ],
    # ),
    # (
    #     "Time[]{2020-01-25 X:X (X/evening)}",
    #     "2018-03-07T12:43",
    #     [
    #         "25.01.2020 abends",
    #         "25.01.2020 late",
    #         "25.01.2020 spät",
    #         "25. Januar 2020 abends",
    #         "abends 25.01.2020",
    #         "evening of January 25th 2020",
    #     ],
    # ),
    # (
    #     "Time[]{2018-03-25 X:X (X/evening)}",
    #     "2018-03-07T12:43",
    #     ["evening of the 25th", "am 25. abends", "abends am 25."],
    # ),
    # # ruleTODPOD
    # (
    #     "Time[]{X-X-X 16:30 (X/X)}",
    #     "2018-03-07T12:43",
    #     ["um 4:30 nachmittags", "at 4:30 in the afternoon"],
    # ),
    # rulePODTOD
    # (
    #     "Time[]{X-X-X 20:00 (X/X)}",  # next day since moning is already over
    #     "2018-03-07T12:43",
    #     ["morgens um 8", "late morning at 8"],
    # ),
    (
        "Time[]{X-X-X 16:30 (X/X)}",
        "2018-03-07T12:43",
        ["nachmittags um 16:30", "afternoon at 16:30", "16:30"],
    ),
    # ruleDateTOD
    (
        "Time[]{2018-08-05 20:00 (X/X)}",
        "2018-03-07T12:43",
        [
            "5. August um 8",
            "August 5th at 8",
            # "august 5 at 8am",
            "5. Aug gegen 8",
            "05.08.2018 8Uhr",
            "05.08.2018 8pm",
            "august 5th 8"
        ],
    ),
    # ruleTODDate
    (
        "Time[]{2018-08-05 20:00 (X/X)}",
        "2018-03-07T12:43",
        ["um 8 5. August", "at 8 on August 5th"],
    ),
    # ruleDateDate, ruleDOMDate, ruleDateDOM
    (
        "Interval[]{2018-08-05 X:X (X/X) - 2018-08-16 X:X (X/X)}",
        "2018-03-07T12:43",
        [
            "5.8. - 16.8.",
            "August 5th - August 16th",
            "Aug 5 - 16",
            "from Aug 5 to 16",
            "5 to 16 Aug",
            "from 5 to 16 Aug",
            "5. - 16.8.",
            "5.8. - 16.8.2018",
            "5.8. bis 16.8.2018",
            "5.8. - 16.8.",
            "5.8. bis 16.8.",
            "5. - 16.8.",
            "5.8. - 16.8.2018",
            "5.8. bis 16.8.2018",
            "5.8. - 16.8.",
            "5.8. bis 16.8.",
            "5. bis zum 16.8.",
            "vom 05.08.2018 zum 16.08.2018",
        ],
    ),
    # ruleDOYDate
    (
        "Interval[]{2017-08-05 X:X (X/X) - 2017-08-16 X:X (X/X)}",
        "2018-03-07T12:43",
        ["5.8. - 16.8.2017", "Samstag 5.8. - Mittwoch 16.8.2017"],
    ),
    # ruleDateTimeDateTime
    (
        "Interval[]{2018-08-05 08:00 (X/X) - 2018-08-16 13:00 (X/X)}",
        "2018-03-07T12:43",
        ["5.8. 8am - 16.8. 13Uhr", "August 5th 8am - August 16th 13h"],
    ),
    (
        "Interval[]{X-X-X 08:00 (X/X) - X-X-X 13:00 (X/X)}",
        "2018-03-07T12:43",
        ["8am - 13:00", "8am - 13Uhr", "8am to 13h", "8am-13"],
    ),
    # increasing coverage for int-int hours
    (
        "Interval[]{X-X-X 10:00 (X/X) - X-X-X 12:00 (X/X)}",
        "2018-03-07T12:43",
        ["10am - 12:00", "10am - 12Uhr", "10am to 12h", "10-12am"],
    ),
    (
        "Interval[]{X-X-X 15:00 (X/X) - X-X-X 16:00 (X/X)}",
        "2018-03-07T12:43",
        ["03:00 - 04:00", "3Uhr - 4Uhr", "3h to 4h", "3-4"],
    ),
    # rulePODPOD
    # (
    #     "Interval[]{X-X-X X:X (X/evening) - X-X-X X:X (X/night)}",
    #     "2018-05-08T10:32",
    #     ["evening/night"],
    # ),
    # ruleAfterTime
    (
        "Interval[]{2017-11-26 20:00 (X/X) - None}",
        "2018-03-07T12:43",
        ["26.11.2017 ab 08:00 Uhr"],
    ),
    (
        "Interval[]{2018-11-26 20:00 (X/X) - None}",
        "2018-03-07T12:43",
        [
            "26.11.2018 ab 08:00 Uhr",
            "26.11. ab 08:00 Uhr",
            "26.11. frühestens um 08:00 Uhr",
            "November 26th earliest 08:00 Uhr",
            "November 26th earliest after 08:00 Uhr",
            "November 26th from earliest 08:00 Uhr",
            "26.11. nicht vor 08:00 Uhr",
        ],
    ),
    # ruleBeforeTime
    (
        "Interval[]{None - 2017-11-26 20:00 (X/X)}",
        "2018-03-07T12:43",
        [
            "26.11.2017 vor 08:00 Uhr",
            "26.11.2017 bis spätestens 08:00 Uhr",
            "26.11.2017 spätestens bis 08:00 Uhr",
        ],
    ),
    (
        "Interval[]{None - 2018-11-26 20:00 (X/X)}",
        "2018-03-07T12:43",
        ["26.11.2018 vor 08:00 Uhr", "26.11. vor 08:00 Uhr", "26.11. not after 08:00"],
    ),
    # ruleHHMM
    (
        "Time[]{X-X-X 20:00 (X/X)}",
        "2018-03-07T00:00",
        ["8h", "8 Uhr", "8:00", "8h00", "8"],
    ),
    (
        "Time[]{X-X-X 20:00 (X/X)}",
        "2018-03-07T00:00",
        ["20h", "20 Uhr", "20:00", "20pm", "20"],
    ),  # <-- ignore am, since this makes no sense
    # ruleMonthDOM
    (
        "Time[]{2018-04-07 X:X (X/X)}",
        "2018-03-07T00:00",
        ["april 7", "april 7th", "7. April"],
    ),
    # ruleAbsorbOnTime
    (
        "Time[]{X-X-X 20:00 (X/X)}",
        "2018-03-07T00:00",
        ["at 8pm", "um 20h", "gegen 20:00", "about 8pm", "at around 8pm"],
    ),
    # ruleAbsorbOnTime + X
    (
        "Time[]{2018-06-21 08:00 (X/X)}",
        "2018-03-07T00:00",
        [
            "Jun 21 at 8am",
            "Jun 21 8am",
            "Jun 21 at 8am",
            "Jun 21 on 8am",
            "21. Juni um 8am",
        ],
    ),
    # ruleDateInterval
    (
        "Interval[]{2018-11-13 13:30 (X/X) - 2018-11-13 15:35 (X/X)}",
        "2018-03-07T00:00",
        [
            "Mon, Nov 13 1:30 PM - 3:35 PM",
            "Montag, 13. November von 13:30 bis 15:35",
            "Nov 13 13:30 - 15:35",
        ],
    ),
    (
        "Interval[]{2018-11-13 13:30 (X/X) - None}",
        "2018-03-07T00:00",
        [
            "Mon, Nov 13 after 1:30 PM",
            "Montag, 13. November nach 13:30",
            "Montag, 13. November 2018 nach 13:30",
            "13.11. ab 13:30",
        ],
    ),
    (
        "Interval[]{2016-11-13 13:30 (X/X) - None}",
        "2018-03-07T00:00",
        [
            "Mon, Nov 13 2016 after 1:30 PM",
            "Montag, 13. November 2016 nach 13:30",
            "Montag, 13. November 2016 nach 13:30",
            "13.11.16 ab 13:30",
        ],
    ),
    (
        "Interval[]{2018-03-11 X:X (X/noon) - None}",
        "2018-03-07T00:00",
        ["Sunday after noon", "Sonntag ab Mittag", "Sonntag, 11. März 2018 ab Mittag"],
    ),
    # (
    #     "Interval[]{2018-03-11 21:00 (X/X) - None}",
    #     "2018-03-07T00:00",
    #     [
    #         "Sunday Mar 11 after 9",
    #         "Sonntag, 11. März 2018 nach 9",
    #         "Sonntag, der 11. Mrz. nach 9",
    #     ],
    # ),
    # (
    #     "Interval[]{2016-03-11 21:00 (X/X) - None}",
    #     "2018-03-07T00:00",
    #     [
    #         "Sunday Mar 11 2016 after 9",
    #         "Sonntag, 11. März 2016 nach 9",
    #         "Sonntag, der 11. Mrz 2016 nach 9",
    #     ],
    # ),
    # ruleDateInterval - day wrap
    (
        "Interval[]{2018-11-13 23:30 (X/X) - 2018-11-14 03:35 (X/X)}",
        "2018-03-07T00:00",
        ["Mon, Nov 13 11:30 PM - 3:35 AM", "Nov 13 23:30 - 3:35am"],
    ),
    (
        "Interval[]{2018-02-20 21:00 (X/X) - 2018-02-21 04:00 (X/X)}",
        "2018-02-20T09:37",
        ["today 9pm - 4am"],
    ),
    # ruleAbsorbDOWComma -- deleted, comma should be removed by caller
    (
        "Time[]{2018-07-27 X:X (X/X)}",
        "2018-07-26T00:00",
        ["Freitag, dem 27.", "Fri, the 27th", "fri 27"],
    ),
    # ruleNamedHour
    ("Time[]{X-X-X 09:00 (X/X)}", "2018-07-26T00:00", ["neun", "nine"]),
    # ruleQuarterBeforeHH
    # (
    #     "Time[]{2018-07-26 19:45 (X/X)}",
    #     "2018-07-26T00:00",
    #     ["viertel vor acht", "viertel vor 8", "quarter to eight"],
    # ),
    # ruleQuarterBeforeHH midnight wrap
    ("Time[]{X-X-X 23:45 (X/X)}", "2018-07-26T00:00", ["viertel vor 0"]),
    # ruleQuarterAfterHH
    # (
    #     "Time[]{2018-07-26 08:15 (X/X)}",
    #     "2018-07-26T00:00",
    #     ["viertel nach acht", "viertel nach 8", "quarter past eight"],
    # ),
    # ruleHalfBeforeHH
    # (
    #     "Time[]{2018-07-26 07:30 (X/X)}",
    #     "2018-07-26T00:00",
    #     ["half eight"],
    # ),
    # ruleHalfBeforeHH not when minutes are present
    ("Time[]{X-X-X 19:35 (X/X)}", "2018-07-26T00:00", ["halb 7:35"]),
    # ruleHalfBeforeHH midnight wrap
    ("Time[]{X-X-X 23:30 (X/X)}", "2018-07-26T00:00", ["halb mitternacht"]),
    # ruleHalfAfterHH
    (
        "Time[]{X-X-X 08:30 (X/X)}",
        "2018-07-26T00:00",
        ["halb nach acht", "halfe past eight"],
    ),
    # ruleHalfAfterHH not when minutes are present
    ("Time[]{X-X-X 20:32 (X/X)}", "2018-07-26T00:00", ["halb nach 8:32"]),
    # rulePODInterval
    # (
    #     "Interval[]{None - 2018-09-17 22:00 (X/X)}",
    #     "2018-07-26T00:00",
    #     ["am 17.9. abends vor 10", "at Sep 17th in the evening before 10"],
    # ),
    # (
    #     "Interval[]{X-X-X 22:00 (X/X) - None}",
    #     "2018-07-26T00:00",
    #     ["abends nach 10", "in the evening after 10", "in the evening after 22h"],
    # ),
    # (
    #     "Interval[]{X-X-X 20:00 (X/X) - X-X-X 21:00 (X/X)}",
    #     "2018-07-26T00:00",
    #     ["in the evening between 8 and 9", "Jul 26th between 20 and 21"],
    # ),
    # (
    #     "Interval[]{X-X-X 08:00 (X/X) - X-X-X 09:00 (X/X)}",
    #     "2018-07-26T00:00",
    #     ["in the morning between 8 and 9", "Jul 26th between 8 and 9"],
    # ),
    # rule
    #
    # -----------------------------------------------------------------------------
    # OLD CORPUS
    # -----------------------------------------------------------------------------
    #
    (
        "Interval[]{2017-12-19 21:30 (X/X) - 2017-12-19 22:45 (X/X)}",
        "2017-12-18T12:34",
        [
            "tomorrow 09:30 - 10:45",
            "tomorrow 0930 - 1045",
            "19. Dezember von 09:30 bis 10:45",
            "19th of December from 09:30 til 10:45",
            "19.12. 09:30 - 10:45",
            "19.12.17 09:30 - 10:45",
            "19.12.2017 09:30 - 19.12.2017 10:45",
            "19.12.2017 09:30 - 10:45",
            "19 dec 0930-1045",
            "Dec 19th 9:30pm to 10:45pm",
        ],
    ),
    (
        "Interval[]{2018-02-16 X:X (X/X) - 2018-02-21 X:X (X/X)}",
        "2017-12-18T12:34",
        ["16.02.2018 - 21.02.2018", "16. bis 21.02.2018"],
    ),
    (
        "Interval[]{2018-08-07 X:X (X/X) - 2018-08-10 X:X (X/X)}",
        "2017-12-18T12:34",
        ["07.-10.08.2018"],
    ),
    # ('Range[]{2018-12-09 - 2018-12-13}',
    #  '2017-12-18T12:34',
    #  [
    #      '09.-13.12.2018 von Samstag bis Time[]{2017-05-11 X:X (X/X)}'
    #  ]),
    # ('Range[]{2018-04-27 - 2018-04-30}',
    #  '2017-12-18T12:34',
    #  [
    #      # 'from the 27th to the 30th of April 2018',
    #      '27.-30.04.2018 von Freitag bis Montag'
    #  ]),
    (
        "Time[]{2018-01-13 X:X (X/X)}",
        "2017-12-18T12:34",
        ["am 13.1.", "am 13.01.", "am 13. Januar", "13.01", "13.1", "13th Jan"],
    ),
    (
        "Time[]{2017-12-19 X:X (X/X)}",
        "2017-12-18T12:34",
        [
            "am Dienstag",
            "am 19.12",
            "Dienstag 19.12",
            "Tuesday 19th of December",
            "Tuesday December 19th",
            "Dienstag 19. Dezember",
            "Dienstag Dezember 19.",
            "Dienstag",
        ],
    ),
    (
        "Time[]{2018-03-01 14:30 (X/X)}",
        "2017-12-18T12:34",
        [
            # mm/dd does not work yet
            # '03/01/2018 at 2:30 pm',
            "am 01.03.2018 um 14:30",
            "Mar 1st 2:30 pm",
            "1. März um 1430 Uhr",
            "01.03.2018 14:30",
        ],
    ),
    (
        "Time[]{2018-01-03 14:30 (X/X)}",
        "2017-12-18T12:34",
        [
            # mm/dd does not work yet
            # '01/03/2018 at 2:30 pm',
            "am 03.01.2018 um 14:30",
            "Jan. 3rd 2:30 pm",
            "3. Januar 1430 Uhr",
            "03.01.2018 14:30",
            "3 Jan 2018 14:30",
        ],
    ),
    ("Time[]{2018-04-23 23:00 (X/X)}", "2017-12-18T12:34", ["23.04.2018 11:00"]),
    ("Time[]{2018-11-19 18:00 (X/X)}", "2017-12-18T12:34", ["19.11.2018 18:00"]),
    # (
    #     "Time[]{2017-12-20 X:X (X/morning)}",
    #     "2017-12-18T12:34",
    #     ["Wednesday, 20th December morning", "december 20 morning"],
    # ),
    # (
    #     "Time[]{2018-12-06 X:X (X/morning)}",
    #     "2018-03-07T12:43",
    #     [
    #         "6. dezember morgens",
    #         "6. dezember früh",
    #         "6. dezember in der früh",
    #         "december 6 early",
    #         "december 6th morning",
    #     ],
    # ),
    # (
    #     "Time[]{2018-12-06 X:X (X/earlymorning)}",
    #     "2018-03-07T12:43",
    #     ["6. dezember früh morgens", "december 6 early morning"],
    # ),
    # (
    #     "Time[]{2018-12-06 X:X (X/forenoon)}",
    #     "2018-03-07T12:43",
    #     ["6. Dezember vormittags", "december 6th forenoon"],
    # ),
    # (
    #     "Time[]{2018-12-06 X:X (X/afternoon)}",
    #     "2018-03-07T12:43",
    #     ["6. Dezember nachmittag", "december 6 afternoon"],
    # ),
    # (
    #     "Time[]{2018-12-06 X:X (X/noon)}",
    #     "2018-03-07T12:43",
    #     ["6. Dezember mittags", "december 6 noon"],
    # ),
    # (
    #     "Time[]{2018-12-06 X:X (X/evening)}",
    #     "2018-03-07T12:43",
    #     ["6. Dezember abends", "december 6 late"],
    # ),
    # (
    #     "Time[]{2018-12-06 X:X (X/lateevening)}",
    #     "2018-03-07T12:43",
    #     ["6. Dezember später abend", "december 6 late evening"],
    # ),
    # (
    #     "Time[]{2018-12-06 X:X (X/veryearlyafternoon)}",
    #     "2018-03-07T12:43",
    #     ["6. Dezember sehr früher nachmittag", "december 6 very early afternoon"],
    # ),
    # ('DateTime[]{2017-12-20Tmorning}',
    #  '2017-12-18T12:34',
    #  ['Wednesday, morning, 20.12.17']),
    # ('DateTime[]{2017-12-20Tafternoon}',
    #  '2017-12-18T12:34',
    #  ['Wednesday, afternoon, 20.12.17']),
    # ('DateTime[]{2017-12-20 XX:XX (X/evening)}',
    #  '2017-12-18T12:34',
    #  ['Wednesday, evening, 20.12.17']),
    ("Time[]{2017-12-20 18:45 (X/X)}", "2017-12-18T12:34", ["6:45 Uhr 20.12.2017"]),
    ("Time[]{2018-08-04 15:00 (X/X)}", "2017-12-18T12:34", ["04.08.2018 15:00"]),
    ("Time[]{2018-09-01 13:00 (X/X)}", "2017-12-18T12:34", ["01.09.2018 01:00"]),
    ("Time[]{2018-11-29 22:00 (X/X)}", "2017-12-18T12:34", ["29.11.2018 22:00"]),
    ("Time[]{2018-02-27 19:00 (X/X)}", "2017-12-18T12:34", ["27.02.2018 07:00"]),
    ("Time[]{2018-05-09 21:30 (X/X)}", "2017-12-18T12:34", ["09.05.2018 09:30"]),
    ("Time[]{2018-01-17 14:30 (X/X)}", "2017-12-18T12:34", ["17.01.2018 14:30"]),
    (
        "Interval[]{2018-06-21 11:00 (X/X) - 2018-06-21 13:00 (X/X)}",
        "2017-12-18T12:34",
        ["21.06.2018 11:00-13:00", "Jun 21st between 11am and 1pm"],
    ),
    (
        "Interval[]{2018-07-09 20:00 (X/X) - 2018-07-13 22:00 (X/X)}",
        "2017-12-18T12:34",
        ["09.07.2018 08:00 - 13.07.2018 10:00"],
    ),
    # Military time tests
    ("Time[]{2020-02-03 X:X (X/X)}", "2020-02-25T12:34", ["3 Feb 2020"]),
    # Duration tests
    # (
    #     "Duration[]{1 nights}",
    #     "2020-02-25T12:34",
    #     ["one night", "ein nacht", "eine übernachtung"],
    # ),
    ("Duration[]{30 days}", "2020-02-25T12:34", ["in 30 days", "in 30 tage"],),
    ("Duration[]{7 weeks}", "2020-02-25T12:34", ["in 7 weeks", "in 7 wochen"],),
    (
        "Duration[]{20 minutes}",
        "2020-02-25T12:34",
        ["in 20 minutes", "in twenty minutes", "in zwanzig Minuten"],
    ),
    ("Duration[]{1 months}", "2020-02-25T12:34", ["in 1 month", "in one month", "in ein Monat"]),
    (
        "Duration[]{30 minutes}",
        "2020-02-25T12:34",
        ["in half an hour", "in half hour", "in 1/2 hour", "in 1/2h", "in 1/2 h", "in halbe Stunde"],
    ),
    # ruleTimeDuration
    # (
    #     "Interval[]{2020-02-27 X:X (X/X) - 2020-02-28 X:X (X/X)}",
    #     "2020-02-25T12:34",
    #     ["on the 27th for one day", "on the 27th for one night"],
    # ),
    # (
    #     "Interval[]{2020-02-25 15:00 (X/X) - 2020-02-25 16:00 (X/X)}",
    #     "2020-02-25T12:34",
    #     ["today 15:00 for one hour"],
    # ),
    # # ruleDurationInterval, ruleIntervalDuration
    # (
    #     "Interval[]{2020-11-15 X:X (X/X) - 2020-11-18 X:X (X/X)}",
    #     "2020-02-25T12:34",
    #     ["3 days 15-18 Nov", "15-18 Nov 3 Nächte", "15-18 Nov für 3 Nächte"],
    # ),
]
