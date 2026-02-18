===========================================================
quickadd
===========================================================

quickadd is a natural language date & time parser written in python. It builds on top of ctparse_ and is an actively maintained fork by Martin Antos.

Installation
----------

With ``pip install -e git+https://github.com/Acreom/quickadd.git#egg=quickadd``


or run ``python setup.py install`` in the root directory after forking.


Main upgrades include:
----------

**Recurring events**


.. code:: python

    r = ctparse("beer daily 4pm")
    r.resolution
    Recurring[5-14]{daily 1 2021-05-09 16:00 (X/X) 2021-05-09 16:00 (X/X)}
    
    r = ctparse("beer every thursday 4")
    r.resolution
    Recurring[5-21]{weekly 1 2021-04-15 16:00 (X/X) 2021-04-15 16:00 (X/X)}
    
    r = ctparse("beer every friday 9-5")
    r.resolution
    Recurring[5-21]{weekly 1 2021-05-14 09:00 (X/X) 2021-05-14 17:00 (X/X)}
    
    r = ctparse("beer september 24 / beer every 24.9")
    r.resolution
    Recurring[5-21]{YEARLY 1 2021-09-24 (X/X) 2021-09-24 (X/X)}

    r = ctparse("beer thursdays 3pm and wednesdays 4pm")
    r.resolution
    RecurringArray[5-37]{
    Recurring instance: weekly 1 2021-05-13 15:00 (X/X) 2021-05-13 15:00 (X/X) 
    Recurring instance: weekly 1 2021-05-12 16:00 (X/X) 2021-05-12 16:00 (X/X)
    }
    
    r = ctparse("beer 9pm weekdays")
    r.resolution
    RecurringArray[5-17]{
    Recurring instance: weekly 1 2021-05-10 21:00 (X/X) 2021-05-10 21:00 (X/X) 
    Recurring instance: weekly 1 2021-05-11 21:00 (X/X) 2021-05-11 21:00 (X/X) 
    Recurring instance: weekly 1 2021-05-12 21:00 (X/X) 2021-05-12 21:00 (X/X) 
    Recurring instance: weekly 1 2021-05-13 21:00 (X/X) 2021-05-13 21:00 (X/X) 
    Recurring instance: weekly 1 2021-05-14 21:00 (X/X) 2021-05-14 21:00 (X/X)}    


**More rules**

ruleNextFrequency

.. code:: python
    
    #reference date = Dec 13th 2022
    r = ctparse("code next week 4pm")
    r.resolution
    Time[5-18]{2022-12-20 16:00
    
    r = ctparse("code next month")
    r.resolution
    Time[5-15]{2023-01-13 X:X (X/X)}


ruleLastDOM

.. code:: python
    
    #reference date = Dec 13th 2022
    r = ctparse("code last monday of the month")
    r.resolution
    Time[5-17]{2022-12-26 X:X (X/X)}


rrule_ **support**

.. code:: python

    r.resolution.to_rrule()
    Out[4]: 'RRULE:FREQ=DAILY;COUNT=1'
    

**Subject extraction**


.. code:: python

    r = ctparse("beers and burgers friday 8pm-9pm")
    r.subject
    Out[2]: 'beers and burgers'
    
    
**PM bias**


.. code:: python

    r = ctparse("fix the issue tmrw 2")
    r.resolution
    Time[14-20]{2022-11-23 14:00 (X/X)}
    
    r = ctparse("fix the issue tmrw 2", pm_bias=False)
    r.resolution
    Time[14-20]{2022-11-23 02:00 (X/X)}


**Rules for ambigious natural language expressions** 

.. code:: python

    r = ctparse("code 9-5")
    r.resolution
    Interval[0-0]{2022-11-23 09:00 (X/X) - 2022-11-23 17:00 (X/X)}


**US/EU date format**


.. code:: python

    r = ctparse("fix the issue 5.3")
    r.resolution
    Time[14-17]{2023-03-05 X:X (X/X)}
    
    r = ctparse("fix the issue 5.3", date_format="US")
    r.resolution
    Time[14-17]{2023-05-03 X:X (X/X)}


**Rule combinations** 

.. code:: python

    r = ctparse("beer in 3 days 4pm")
    r.resolution
    Time[5-18]{2021-05-12 16:00 (X/X)}
    
    
    r = ctparse("beer in 3 days 4pm every week")
    r.resolution
    Recurring[5-29]{weekly 1 2021-05-12 16:00 (X/X) 2021-05-12 16:00 (X/X)}


    r = ctparse("beer every friday 4-6:30pm")
    r.resolution
    Recurring[5-26]{WEEKLY 1 2022-11-25 16:00 (X/X) 2022-11-25 18:30 (X/X)}


``+`` **performance improvements**


Base Capabilities
----------
| **Time** 

.. code:: python

    "beer thursday 4"
    Time[5-15]{2021-05-13 16:00 (X/X)}


| **Interval** 

.. code:: python

    "beer 4-6"
    Interval[0-0]{2021-05-09 16:00 (X/X) - 2021-05-09 18:00 (X/X)}


| **Duration** 

.. code:: python

    "beer in 4 hours"
    Duration[5-15]{4 hours}


Ctparse
----------

The package ``ctparse`` is a pure python package to parse time
expressions from natural language (i.e. strings). In many ways it builds
on similar concepts as Facebook’s ``duckling`` package
(https://github.com/facebook/duckling). However, for the time being it
only targets times and only German and English text.

In principle ``ctparse`` can be used to **detect** time expressions in a
text, however its main use case is the semantic interpretation of such
expressions. Detecting time expressions in the first place can - to our
experience - be done more efficiently (and precisely) using e.g. CRFs or
other models targeted at this specific task.

``ctparse`` is designed with the use case in mind where interpretation
of time expressions is done under the following assumptions:

-  All expressions are relative to some pre-defined reference times
-  Unless explicitly specified in the time expression, valid resolutions
   are in the future relative to the reference time (i.e. ``12.5.`` will
   be the next 12th of May, but ``12.5.2012`` should correctly resolve
   to the 12th of May 2012).
-  If in doubt, resolutions in the near future are more likely than
   resolutions in the far future (not implemented yet, but any
   resolution more than i.e. 3 month in the future is extremely
   unlikely).

The specific comtravo use-case is resolving time expressions in booking
requests which almost always refer to some point in time within the next
4-8 weeks.

``ctparse`` currently is language agnostic and supports German and
English expressions. This might get an extension in the future. The main
reason is that in real world communication more often than not people
write in one language (their business language) but use constructs to
express times that are based on their mother tongue and/or what they
believe to be the way to express dates in the target language. This
leads to text in German with English time expressions and vice-versa.
Using a language detection upfront on the complete original text is for
obvious no solution - rather it would make the problem worse.

Example
-------

.. code:: python

   from ctparse import ctparse
   from datetime import datetime

   # Set reference time
   ts = datetime(2018, 3, 12, 14, 30)
   ctparse('May 5th 2:30 in the afternoon', ts=ts)

This should return a ``Time`` object represented as
``Time[0-29]{2018-05-05 14:30 (X/X)}``, indicating that characters
``0-29`` were used in the resolution, that the resolved date time is the
5th of May 2018 at 14:30 and that this resolution is neither based on a
day of week (first ``X``) nor a part of day (second ``X``).


Latent time
~~~~~~~~~~~

Normally, ``ctparse`` will anchor time expressions to the reference time. 
For example, when parsing the time expression ``8:00 pm``, ctparse will
resolve the expression to 8 pm after the reference time as follows

.. code:: python

   parse = ctparse("8:00 pm", ts=datetime(2020, 1, 1, 7, 0), latent_time=True) # default
   # parse.resolution -> Time(2020, 1, 1, 20, 00)

This behavior can be customized using the option ``latent_time=False``, which will
return a time resolution not anchored to a particular date

.. code:: python

   parse = ctparse("8:00 pm", ts=datetime(2020, 1, 1, 7, 0), latent_time=False)
   # parse.resolution -> Time(None, None, None, 20, 00)

Implementation
--------------

``ctparse`` - as ``duckling`` - is a mixture of a rule and regular
expression based system + some probabilistic modeling. In this sense it
resembles a PCFG.

Rules
~~~~~

At the core ``ctparse`` is a collection of production rules over
sequences of regular expressions and (intermediate) productions.

Productions are either of type ``Time``, ``Interval``, ``Duration`` or ``Recurring`` and can
have certain predicates (e.g. whether a ``Time`` is a part of day like
``'afternoon'``).

A typical rule than looks like this:

.. code:: python

   @rule(predicate('isDate'), dimension(Interval))

I.e. this rule is applicable when the intermediate production resulted
in something that has a date, followed by something that is in interval
(like e.g. in ``'May 5th 9-10'``).

The actual production is a python function with the following signature:

.. code:: python

   @rule(predicate('isDate'), dimension(Interval))
   def ruleDateInterval(ts, d, i):
     """
     param ts: datetime - the current refenrence time
     d: Time - a time that contains at least a full date
     i: Interval - some Interval
     """
     if not (i.t_from.isTOD and i.t_to.isTOD):
       return None
     return Interval(
       t_from=Time(year=d.year, month=d.month, day=d.day,
                   hour=i.t_from.hour, minute=i.t_from.minute),
       t_to=Time(year=d.year, month=d.month, day=d.day,
                 hour=i.t_to.hour, minute=i.t_to.minute))

This production will return a new interval at the date of
``predicate('isDate')`` spanning the time coded in
``dimension(Interval)``. If the latter does code for something else than
a time of day (TOD), no production is returned, e.g. the rule matched
but failed.


Technical Background
~~~~~~~~~~~~~~~~~~~~

Some observations on the problem:

-  Each rule is a combination of regular expressions and productions.
-  Consequently, each production must originate in a sequence of regular
   expressions that must have matched (parts of) the text.
-  Hence, only subsequence of **all** regular expressions in **all**
   rules can lead to a successful production.

To this end the algorithm proceeds as follows:

1. Input a string and a reference time
2. Find all matches of all regular expressions from all rules in the
   input strings. Each regular expression is assigned an identifier.
3. Find all distinct sequences of these matches where two matches do not
   overlap nor have a gap inbetween
4. To each such subsequence apply all rules at all possible positions
   until no further rules can be applied - in which case one solution is
   produced

Obviously, not all sequences of matching expressions and not all
sequences of rules applied on top lead to meaningful results. Here the
**P**\ CFG kicks in:

-  Based on example data (``corpus.py``) a model is calibrated to
   predict how likely a production is to lead to a/the correct result.
   Instead of doing a breadth first search, the most promising
   productions are applied first.
-  Resolutions are produced until there are no more resolutions or a
   timeout is hit.
-  Based on the same model from all resolutions the highest scoring is
   returned.


.. _ctparse: https://github.com/comtravo/ctparse
.. _rrule: https://dateutil.readthedocs.io/en/stable/rrule.html

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
