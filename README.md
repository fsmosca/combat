# Combat
A python script to run engine vs engine game matches.

### Requirements
* Python 3.7.x or later
* Python-chess

### Guide

#### 1. Help
combat.py -h
```
usage: combat [-h] --engine-config-file ENGINE_CONFIG_FILE --engine
              [ENGINE [ENGINE ...]] --opening [OPENING [OPENING ...]]
              [--round ROUND] [--reverse] [--parallel PARALLEL]
              [--win-adjudication [WIN_ADJUDICATION [WIN_ADJUDICATION ...]]]
              [--output OUTPUT] [-v]

Run engine vs engine match

optional arguments:
  -h, --help            show this help message and exit
  --engine-config-file ENGINE_CONFIG_FILE
                        This is used to define the file where
                        engine configurations are located. You may use included file combat.json
                        or you can use engines.json from cutechess.
                        example:
                        --engine-config-file combat.json
                        or using the engines.json from cutechess
                        --engine-config-file "d:/chess/cutechess/engines.json"
  --engine [ENGINE [ENGINE ...]]
                        This option is used to define the engines
                        playing in the match. It also include tc or time control. You need to call
                        this twice. See example below.
                        format:
                        --engine config-name=E1 tc=btms1+itms1 --engine config-name=E2 tc=btms2+itms2
                        where:
                            E1 = engine name from combat.json or engine config file
                            btms1 = base time in ms for engine 1
                            itms1 = increment time in ms for engine 1
                        example:
                        --engine config-name="Deuterium v2019.2" tc=60000+100 --engine config-name="Deuterium v2019.2 mobility130" tc=60000+100
                        note:
                            * engine1 will play as black, in the example above
                              this is Deuterium v2019.2
                            * engine2 will play as white
                            * When round reverse is true the side is reversed that is
                              engine1 will play as white and engine2 will play as black
  --opening [OPENING [OPENING ...]]
                        Opening file is used by engine to start the game. You
                        may use pgn or epd or fen formats.
                        example:
                        --opening file=start.pgn random=true
                        or with file path
                        --opening file="d:/chess/opening_start.pgn" random=true
                        or with epd file
                        --opening file="d:/chess/opening.epd" random=true
                        or to not use random
                        --opening file="d:/chess/opening.epd" random=false
  --round ROUND         number of games to play, twice if reverse is true
  --reverse             A flag when when set, changes start side, to play a position.
  --parallel PARALLEL   Option to run game matches in parallel
                        example:
                        --parallel 1
                        default is 1, but if your cpu has more than 1 cores or threads
                        lets say 8, you may use
                        --parallel 7
  --win-adjudication [WIN_ADJUDICATION [WIN_ADJUDICATION ...]]
                        Option to stop the game when one side is
                        already ahead on score. Both engines would agree that one side
                        is winning and the other side is lossing.
                        example:
                        --win-adjudication score=700 count=4
                        where:
                            score: engine score in cp
                            count: number of times the score is recorded
  --output OUTPUT       Save output games, default=output_games.pgn
  -v, --version         show program's version number and exit

combat v1.6
```

#### 2. Command line
```
combat.py --engine-config-file combat.json ^
--engine config-name="Deuterium v2019.2" tc=60000+100 --engine config-name="Deuterium v2019.2 mobility130" tc=60000+100 ^
--opening file="grand_swiss_2019_6plies.pgn" random=true ^
--round 8 ^
--reverse ^
--win-adjudication score=700 count=4 ^
--parallel 1
```

Also check the windows batch file run_combat.bat which can be found in this repo. You can modify and run it.

#### 3. How to find the config-name in combat.json file?
Open combat.json file and find a name key. Example below.
```
[
    {
        "command": "Deuterium_v2019.2.37.73_64bit_pop.exe",
        "workingDirectory": "./engines",
        "name": "Deuterium v2019.2",
        "protocol": "uci",
        "options": [
            {
                "name": "Hash",
                "default": 128,
                "value": 128,
                "type": "spin",
                "min": 8,
                "max": 2048
            },
        ......
        ......
```
That `Deuterium v2019.2` will be the engine's config-name.

### Features
* Supports time control with base time and increment, like TC 60+1, in combat,  
  you need to specify in ms and that would become TC 60000+1000. In command line  
  `--engine config-name=engine1 tc=60000+1000 --engine config-name=engine2 tc=30000+100`
* Can run game matches in parallel.
* Zero interface lags, engine will get its remaining time based on its reported spent time.
* Supports fen/epd and pgn files as a source of opening start positions.
* Can adjudicate games based on winning score.
* Can read engine settings from combat.json file or cutechess engines.json file.

### Limitations
* Can only run engine vs engine match.
* Only uci engines are supported.
* Does not support time control with periods, and movetime.

### Testing
Tested to run on the following conditions:
* Windows 10
* Python 3.7
* Python-chess v0.30.1

### Credits
* Python-chess  
  * https://github.com/niklasf/python-chess
  * Handles uci engine and pgn processings.
* The Week in Chess  
  * http://theweekinchess.com/
  * Good source to get chess pgn files.
