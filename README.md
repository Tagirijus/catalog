A programm for analyzing ODS spreadsheets.

# Install

You need the `pyexcel_ods` python3 module to run this program. You can install it with

	sudo pip3 install pyexcel-ods

# Usage

For me as a composer I want to keep track of my music pieces. For that reason I started to create a ODS spreadsheet with plenty of information for each track I ever made. Many information can already be "analyzed" in maybe OpenOffice or LibreOffice. Even more complex information could also be calculated with macros, but I did not want to dig into macro programming. So I wrote this little porgramm for giving me information about my spreadsheet OpenOffice / LibreOffice do not give me out of the box (or it can and I do not know how, haha!).

The programm is terminal based and works with parameter. You can get a brief help / overview of the possible parameters by running the programm with `-h` or `--help`.

	python3 run.py -h

Basically you have a spreadsheet and maybe want to analyze it. Maybe there are columns holding data and you want to count entries in the file `pieces.ods`:

| Title | Playing time | Genre |
| --- | --- | --- |
| Classiness | 1:54 min | Electro |
| Elephant On Tiptoes | 2:36 min | Big Band |
| Mice | 3:21 min | Big Band |
| Show Your Courage | 3:26 min | Soundtrack |
| Mysterious Cave Dwellers | 3:12 min | Soundtrack |
| Tricky | 1:00 min | Soundtrack |

If you want to know which genres occurs how often, you now could query it this way:

	python3 run.py pieces.ods -c Genre

It would output it like this:

	1: Electro
	2: Big Band
	3: Soundtrack

You can also let the program try to count according to values in a specific column. The column "Playing time" for examples holds the playing time of the pieces. So a query like this:

	python3 run.py pieces.ods -c Genre -t "Playing time"

... would output this:

	0:01:54: Electro
	0:05:57: Big Band
	0:07:38: Soundtrack

Another example table `instruments.ods`:

| Title | Instruments | Date |
| --- | --- | --- |
| Acapello | Vocals, Walking Bass, Drums | 2007-12-25 |
| Across The Street | Organ, Guitar, E-Bass, Drums | 2010-04-10 |
| Antiblues | Organ, E-Guitar, E-Bass, Drums | 2015-11-30 |
| Broken Mood | Tenor Saxophone, Clarinette, Vibraphone, Guitar, Walking Bass, Percussion | 2015-07-01 |


With a query like this:

	python3 run.py instruments.ods -c Instruments --csv

... would output this:

	1: Vocals
	1: E-Guitar
	1: Tenor Saxophone
	1: Clarinette
	1: Vibraphone
	1: Percussion
	2: Walking Bass
	2: Guitar
	2: E-Bass
	2: Organ
	3: Drums

Means: with `--csv` cell data with commas will be split. You can also narrow the search with a filter:

	python3 run.py instruments.ods -c Instruments --csv -f Date ">2008"

... would output this:

	1: E-Guitar
	1: Tenor Saxophone
	1: Clarinette
	1: Vibraphone
	1: Percussion
	1: Walking Bass
	2: Guitar
	2: E-Bass
	2: Organ
	2: Drums

Since it would search dates in the column `Date` which are higher than the year 2008. A bit more is possible here ('<' or '=' ... or '2008-01-15' to search above 15th January 2008). It also supports integer / floats, of course. It gets the correct type from the given column, if it finds this column.

In case you do not know what columns are possible for the file: `python3 run.py -l` will list all the possible columns.

Another method of working with dates is the `-d` parameter:

	python3 run.py instruments.ods -c Date -d year

... would output this:

	1: 2007
	1: 2010
	2: 2015

It counts the entries according to the date column and narrows it to only the year. With `-d month` for example, it would look like this instead:

	1: 2007-12
	1: 2010-04
	1: 2015-11
	1: 2015-07

... since this would also take the month into account.

I hope I could explain this little tool a bit ... maybe some will find it usefull, maybe somethign like this already exists and I wasted my time, I don't know. Have fun with it anyway. d-:

# ToDo

- -f / --filter should be possible to do `or` operations as well. E.g. something like `--filter-or Genre Soundtrack --filter-or Date "=2015"` would find entries which have "Soundtrack" in their Genre column _OR_ the year "2015" in their Date column.