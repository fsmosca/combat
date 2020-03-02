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
              [--output OUTPUT] [--log-filename LOG_FILENAME] [--engine-log]
              [-v]

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
  --reverse             A flag to reverse start side.
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
  --log-filename LOG_FILENAME
                        A filename to save its logs. default=combat_log.txt
  --engine-log          A flag to save engine log to a file.
  -v, --version         show program's version number and exit

combat v1.14
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

To enable engine logging and saved in engine_log.txt, use the --engine-log flag.  
`combat.py --engine-config-name ... --engine-log`

All logs are saved in combat_log.txt, to save in a different log, use the --log-filename option.  
`combat.py --engine-config-name ... --log-filename mylog.txt`

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

#### 4. Sample run
```
combat v1.11
Preparing start opening from my_startpos.pgn ...
status: done, games prepared: 6, elapse: 0h:00m:00s:005ms

rounds           : 6
reverse side     : True
total games      : 12
opening file     : D:\Chess\CuteChess-CLI\pos\my_startpos.pgn
randomize fen    : True
base time(ms)    : 10000
inc time(ms)     : 10
win adjudication : True
win score cp     : 700
win score count  : 4
parallel         : 6

Starting, game: 2 / 12, round: 1.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
Starting, game: 1 / 12, round: 1.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
Starting, game: 3 / 12, round: 2.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
Starting, game: 5 / 12, round: 3.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
Starting, game: 4 / 12, round: 2.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
Starting, game: 6 / 12, round: 3.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
Done, game: 5, round: 3.1, elapse: 0h:00m:14s:417ms
players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
result: 0-1 (adjudication: good score for black)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       1.0         1   100.0     0.0    0
Deuterium v2019.2                   0.0         1     0.0     0.0    0

Starting, game: 7 / 12, round: 4.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
Done, game: 3, round: 2.1, elapse: 0h:00m:17s:179ms
players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
result: 0-1 (adjudication: good score for black)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       2.0         2   100.0     0.0    0
Deuterium v2019.2                   0.0         2     0.0     0.0    0

Starting, game: 8 / 12, round: 4.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
Done, game: 6, round: 3.2, elapse: 0h:00m:17s:436ms
players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
result: 0-1 (adjudication: good score for black)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       2.0         3    66.7     0.0    0
Deuterium v2019.2                   1.0         3    33.3     0.0    0

Done, game: 1, round: 1.1, elapse: 0h:00m:17s:966ms
players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
result: 0-1 (adjudication: good score for black)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       3.0         4    75.0     0.0    0
Deuterium v2019.2                   1.0         4    25.0     0.0    0

Starting, game: 9 / 12, round: 5.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
Starting, game: 10 / 12, round: 5.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
Done, game: 4, round: 2.2, elapse: 0h:00m:18s:129ms
players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
result: 1-0 (adjudication: good score for white)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       4.0         5    80.0     0.0    0
Deuterium v2019.2                   1.0         5    20.0     0.0    0

Starting, game: 11 / 12, round: 6.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
Done, game: 2, round: 1.2, elapse: 0h:00m:19s:254ms
players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
result: 1-0 (adjudication: good score for white)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       5.0         6    83.3     0.0    0
Deuterium v2019.2                   1.0         6    16.7     0.0    0

Starting, game: 12 / 12, round: 6.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
Done, game: 7, round: 4.1, elapse: 0h:00m:12s:209ms
players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
result: 1/2-1/2 (threefold repetition)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       5.5         7    78.6    14.3    0
Deuterium v2019.2                   1.5         7    21.4    14.3    0

Done, game: 8, round: 4.2, elapse: 0h:00m:16s:075ms
players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
result: 1/2-1/2 (insufficient mating material)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       6.0         8    75.0    25.0    0
Deuterium v2019.2                   2.0         8    25.0    25.0    0

Done, game: 11, round: 6.1, elapse: 0h:00m:15s:798ms
players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
result: 1/2-1/2 (insufficient mating material)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       6.5         9    72.2    33.3    0
Deuterium v2019.2                   2.5         9    27.8    33.3    0

Done, game: 10, round: 5.2, elapse: 0h:00m:18s:905ms
players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
result: 0-1 (adjudication: good score for black)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       6.5        10    65.0    30.0    0
Deuterium v2019.2                   3.5        10    35.0    30.0    0

Done, game: 12, round: 6.2, elapse: 0h:00m:17s:767ms
players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
result: 0-1 (adjudication: good score for black)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       6.5        11    59.1    27.3    0
Deuterium v2019.2                   4.5        11    40.9    27.3    0

Done, game: 9, round: 5.1, elapse: 0h:00m:20s:166ms
players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
result: 1/2-1/2 (insufficient mating material)

name                              score     games  score%   Draw%   tf
Deuterium v2019.2 mobility130       7.0        12    58.3    33.3    0
Deuterium v2019.2                   5.0        12    41.7    33.3    0

Match: done, elapse: 0h:00m:39s:303ms
```

#### 5. Sample logs from combat_log.txt
```
2020-03-02 12:55:45,169 -     get_game_list -     INFO - Preparing start opening from grand_swiss_2019_6plies.epd ...
2020-03-02 12:55:45,169 -     get_game_list -     INFO - status: done, games prepared: 8, elapse: 0h:00m:00s:003ms

2020-03-02 12:55:45,169 -  match_conditions -     INFO - rounds           : 8
2020-03-02 12:55:45,169 -  match_conditions -     INFO - reverse side     : True
2020-03-02 12:55:45,169 -  match_conditions -     INFO - total games      : 16
2020-03-02 12:55:45,169 -  match_conditions -     INFO - opening file     : grand_swiss_2019_6plies.epd
2020-03-02 12:55:45,169 -  match_conditions -     INFO - randomize fen    : True
2020-03-02 12:55:45,169 -  match_conditions -     INFO - base time(ms)    : 5000
2020-03-02 12:55:45,169 -  match_conditions -     INFO - inc time(ms)     : 50
2020-03-02 12:55:45,169 -  match_conditions -     INFO - win adjudication : True
2020-03-02 12:55:45,169 -  match_conditions -     INFO - win score cp     : 700
2020-03-02 12:55:45,169 -  match_conditions -     INFO - win score count  : 4
2020-03-02 12:55:45,169 -  match_conditions -     INFO - parallel         : 7

2020-03-02 12:55:46,123 - Match.start_match -    DEBUG - Create end board from fen: rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 1
2020-03-02 12:55:46,123 - Match.start_match -     INFO - Starting, game: 1 / 16, round: 1.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
2020-03-02 12:55:46,326 - Match.start_match -    DEBUG - Create end board from fen: rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N5/PP2PPPP/R1BQKBNR w KQkq - 0 1
2020-03-02 12:55:46,326 - Match.start_match -     INFO - Starting, game: 2 / 16, round: 1.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
2020-03-02 12:55:46,498 - Match.start_match -    DEBUG - Create end board from fen: rnbqkb1r/pp1p1ppp/4pn2/2p5/2PP4/5N2/PP2PPPP/RNBQKB1R w KQkq - 0 1
2020-03-02 12:55:46,498 - Match.start_match -     INFO - Starting, game: 3 / 16, round: 2.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
2020-03-02 12:55:46,498 - Match.start_match -    DEBUG - Create end board from fen: rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/5N2/PP2PPPP/RNBQKB1R w KQkq - 0 1
2020-03-02 12:55:46,498 - Match.start_match -     INFO - Starting, game: 6 / 16, round: 3.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
2020-03-02 12:55:46,545 - Match.start_match -    DEBUG - Create end board from fen: rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/5N2/PP2PPPP/RNBQKB1R w KQkq - 0 1
2020-03-02 12:55:46,545 - Match.start_match -     INFO - Starting, game: 5 / 16, round: 3.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
2020-03-02 12:55:46,623 - Match.start_match -    DEBUG - Create end board from fen: rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/6P1/PP2PP1P/RNBQKBNR w KQkq - 0 1
2020-03-02 12:55:46,623 - Match.start_match -     INFO - Starting, game: 7 / 16, round: 4.1, players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
2020-03-02 12:55:46,638 - Match.start_match -    DEBUG - Create end board from fen: rnbqkb1r/pp1p1ppp/4pn2/2p5/2PP4/5N2/PP2PPPP/RNBQKB1R w KQkq - 0 1
2020-03-02 12:55:46,638 - Match.start_match -     INFO - Starting, game: 4 / 16, round: 2.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
2020-03-02 12:55:53,593 -      adjudication -    DEBUG - White wins by adjudication. White last 4 scores: [846, 845, 819, 853], Black last 4 scores: [-838, -820, -862, -841]
2020-03-02 12:55:53,639 -              main -     INFO - Done, game: 5, round: 3.1, elapse: 0h:00m:07s:072ms
2020-03-02 12:55:53,639 -              main -     INFO - players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
2020-03-02 12:55:53,639 -              main -     INFO - result: 1-0 (adjudication: good score for white)
2020-03-02 12:55:53,639 -      result_table -     INFO - 
2020-03-02 12:55:53,639 -      result_table -     INFO - name                                 score     games  score%   Draw%   tf
2020-03-02 12:55:53,639 -      result_table -     INFO - Deuterium v2019.2 mobility130          0.0         1     0.0     0.0    0
2020-03-02 12:55:53,639 -      result_table -     INFO - Deuterium v2019.2                      1.0         1   100.0     0.0    0
2020-03-02 12:55:53,639 -      result_table -     INFO - 
2020-03-02 12:55:53,936 - Match.start_match -    DEBUG - Create end board from fen: rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/6P1/PP2PP1P/RNBQKBNR w KQkq - 0 1
2020-03-02 12:55:53,936 - Match.start_match -     INFO - Starting, game: 8 / 16, round: 4.2, players: Deuterium v2019.2 mobility130 vs Deuterium v2019.2
2020-03-02 12:55:55,218 -      adjudication -    DEBUG - White wins by adjudication. White last 4 scores: [737, 906, 950, 1089], Black last 4 scores: [-794, -1021, -1094, -1303]
2020-03-02 12:55:55,264 -              main -     INFO - Done, game: 3, round: 2.1, elapse: 0h:00m:08s:749ms
2020-03-02 12:55:55,280 -              main -     INFO - players: Deuterium v2019.2 vs Deuterium v2019.2 mobility130
2020-03-02 12:55:55,280 -              main -     INFO - result: 1-0 (adjudication: good score for white)
2020-03-02 12:55:55,280 -      result_table -     INFO - 
2020-03-02 12:55:55,280 -      result_table -     INFO - name                                 score     games  score%   Draw%   tf
2020-03-02 12:55:55,280 -      result_table -     INFO - Deuterium v2019.2 mobility130          0.0         2     0.0     0.0    0
2020-03-02 12:55:55,280 -      result_table -     INFO - Deuterium v2019.2                      2.0         2   100.0     0.0    0
```

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
