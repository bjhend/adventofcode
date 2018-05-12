# Advent of Code Solutions

Solutions to _Advent of Code_ puzzles from [adventofcode.com](https://adventofcode.com).


## About

[Advent of Code](https://adventofcode.com) is a set of programming puzzles made by [Eric Wastl](http://was.tl/) released between December 1 and December 25 since 2015. See Advent of Code's [about page](https://adventofcode.com/about) for more.

This repository contains my personal solutions of these puzzles. The objectives of the code are:

- solve the problem
- understandable code
- efficiency

To run the solutions you need to download the puzzle input first. See section [Input](https://github.com/bjhend/adventofcode#input) below how to do that and where to put it.


## Thanks

Thanks to [Eric Wastl](http://was.tl/) for these wonderful programming puzzles. They cover many basic programming problems and are excellent examples to 
repeat and deepen the knowledge of a programming language.


## Documentation

Details of the daily solutions and the code itself are documented in the respective source files.


## Input

This repository does not provide the puzzle inputs itself, because they belong to _Advent of Code_. To make the input available for the solutions, log into [Advent of Code](https://adventofcode.com), download the input files and store them in a file per day. As far as I can see the URL scheme to download the input is `http://adventofcode.com/<year>/day/<day>/input`. This scheme seems to work also for days with single value input provided on the puzzle page itself.

By default the helper class `Input` expects the daily input files in a folder called `input` besides this repository. Create a subfolder with the puzzles' year as name in `ìnput` and store the daily input in files named like `day01.txt`. For example, the name for day 7 of year 2017 would be `input/2017/day07.txt` (on Windows with '`\`' of course).

You may change the folder and the naming scheme of the downloaded input files by adapting the constants at the top of file [helpers/puzzleInput.py](helpers/puzzleInput.py). If this is not sufficient change the code of `Input.__init__()` loading the input.


## Helpers

The folder `helpers` contains some modules useful for all or at least several daily solutions. First of all it contains the module to read the puzzle input and do some simple initial processing. Additionally, there is a module providing special containers which may grow infinitely somehow. More helper modules may follow.


## License

See [LICENSE](LICENSE) for the license itself and [www.gnu.org/licenses/#AGPL](https://www.gnu.org/licenses/#AGPL)
or [wikipedia.org/wiki/Affero_General_Public_License](https://en.wikipedia.org/wiki/Affero_General_Public_License)
for more info about the license.

