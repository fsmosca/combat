# Combat
A python script to run engine vs engine game matches.

### Requirements
* Python 3.7.x or later
* Python-chess

### Guide
Edit the source combat.py to define engine locations, options, names and others, then execute combat.py.
```python
    opening_file = 'grand_swiss_2019_6plies.epd'
    outpgn = 'combat_auto_games.pgn'
    
    eng_file1 = 'engines/Deuterium_v2019.2.37.73_64bit_pop.exe'
    eng_file2 = 'engines/Deuterium_v2019.2.37.73_64bit_pop.exe'
    
    # Engine uci options
    eng_opt1 = {'hash': 128}
    eng_opt2 = {'hash': 128,
                'mobilityweight': 150,
                'kingshelterweight': 200
                }
    
    eng_name1 = 'Deuterium 2019.2'
    eng_name2 = 'Deuterium 2019.2 mob150 ks200'
    
    # Match options    
    randomize_pos = True
    reverse_start_side = True
    max_round = 50
    parallel = 6  # No. of game matches to run in parallel
    
    # Time control
    base_time_ms = 5000
    inc_time_ms = 50
    
    # Adjust time odds, must be 1 or more.
    # The first 1 in [1, 1] will be for engine1. If [2, 1], time of
    # engine1 will be reduced by half.
    bt_time_odds = [1, 1]  # bt is base time
    it_time_odds = [1, 1]  # it is increment time
    
    bt1 = base_time_ms/max(1, bt_time_odds[0])
    bt2 = base_time_ms/max(1, bt_time_odds[1])
    
    it1 = inc_time_ms/max(1, it_time_odds[0])
    it2 = inc_time_ms/max(1, it_time_odds[1])
```
Example run:
```
rounds        : 50
revese side   : True
total games   : 100
opening file  : grand_swiss_2019_6plies.epd
randomize fen : True
base time(ms) : 5000
inc time(ms)  : 50
parallel      : 6

Starting game 1 / 100, round: 1.1, (Deuterium 2019.2 mob150 ks200 vs Deuterium 2019.2)
Starting game 2 / 100, round: 1.2, (Deuterium 2019.2 vs Deuterium 2019.2 mob150 ks200)
Starting game 3 / 100, round: 2.1, (Deuterium 2019.2 mob150 ks200 vs Deuterium 2019.2)
Starting game 4 / 100, round: 2.2, (Deuterium 2019.2 vs Deuterium 2019.2 mob150 ks200)
Starting game 5 / 100, round: 3.1, (Deuterium 2019.2 mob150 ks200 vs Deuterium 2019.2)
Starting game 6 / 100, round: 3.2, (Deuterium 2019.2 vs Deuterium 2019.2 mob150 ks200)
Done game 6, round: 3.2, (Deuterium 2019.2 vs Deuterium 2019.2 mob150 ks200): 1/2-1/2 (threefold repetition)

name                              score     games  score%   Draw%   tf
Deuterium 2019.2                    0.5         1    50.0   100.0    0
Deuterium 2019.2 mob150 ks200       0.5         1    50.0   100.0    0

Starting game 7 / 100, round: 4.1, (Deuterium 2019.2 mob150 ks200 vs Deuterium 2019.2)
Done game 1, round: 1.1, (Deuterium 2019.2 mob150 ks200 vs Deuterium 2019.2): 1-0 (checkmate)

name                              score     games  score%   Draw%   tf
Deuterium 2019.2                    0.5         2    25.0    50.0    0
Deuterium 2019.2 mob150 ks200       1.5         2    75.0    50.0    0

Starting game 8 / 100, round: 4.2, (Deuterium 2019.2 vs Deuterium 2019.2 mob150 ks200)
Done game 2, round: 1.2, (Deuterium 2019.2 vs Deuterium 2019.2 mob150 ks200): 1-0 (checkmate)

name                              score     games  score%   Draw%   tf
Deuterium 2019.2                    1.5         3    50.0    33.3    0
Deuterium 2019.2 mob150 ks200       1.5         3    50.0    33.3    0

....

Done game 100, round: 50.2, (Deuterium 2019.2 vs Deuterium 2019.2 mob150 ks200): 1/2-1/2 (fifty moves)

name                              score     games  score%   Draw%   tf
Deuterium 2019.2                   53.5       100    53.5    37.0    0
Deuterium 2019.2 mob150 ks200      46.5       100    46.5    37.0    0
```
Example pgn output:
```
[Event "?"]
[Site "?"]
[Date "????.??.??"]
[Round "3.2"]
[White "Deuterium 2019.2"]
[Black "Deuterium 2019.2 mob150 ks200"]
[Result "1/2-1/2"]
[BlackTimeControl "5s+0.05s"]
[FEN "rnbqkb1r/pp1p1ppp/4pn2/2p5/3P4/6P1/PPP1PPBP/RNBQK1NR w KQkq - 0 1"]
[Termination "threefold repetition"]
[WhiteTimeControl "5s+0.05s"]

1. Nf3 { +0.51/9 94ms } 1... Be7 { -0.17/9 141ms } 2. dxc5 { +0.44/10 94ms } 2... O-O { -0.23/11 94ms } 3. Be3 { +0.38/10 109ms } 3... Nc6 { -0.15/10 93ms } 4. O-O { +0.47/11 94ms } 4... b6 { -0.18/11 94ms } 5. cxb6 { +0.53/11 157ms } 5... axb6 { -0.17/11 156ms } 6. c4 { +0.18/9 94ms } 6... Bc5 { -0.17/11 234ms } 7. Nd4 { +0.53/10 94ms } 7... Bb7 { -0.57/12 125ms } 8. Nc3 { +0.71/10 94ms } 8... Qb8 { -0.40/11 109ms } 9. Ndb5 { +0.61/10 78ms } 9... Ne5 { -0.69/12 172ms } 10. Bxc5 { +0.41/12 78ms } 10... bxc5 { -0.46/12 141ms } 11. e4 { +0.82/11 93ms } 11... Nxc4 { -0.90/12 157ms } 12. Qe2 { +0.92/12 250ms } 12... Nb6 { -0.21/10 93ms } 13. a4 { +0.82/9 79ms } 13... d5 { -0.41/10 109ms } 14. e5 { +0.32/9 78ms } 14... Nfd7 { -0.57/10 78ms } 15. f4 { +0.53/10 125ms } 15... d4 { +0.05/12 110ms } 16. Bxb7 { +0.05/12 78ms } 16... Qxb7 { +0.18/12 109ms } 17. Nd6 { +0.39/13 94ms } 17... Qb8 { +0.04/13 141ms } 18. a5 { +0.00/11 172ms } 18... dxc3 { -0.01/14 94ms } 19. axb6 { -0.05/13 78ms } 19... Rxa1 { +0.07/15 109ms } 20. Rxa1 { +0.06/15 78ms } 20... cxb2 { +0.07/14 63ms } 21. Qxb2 { +0.01/14 109ms } 21... Qxb6 { -0.01/13 63ms } 22. Qxb6 { +0.08/13 93ms } 22... Nxb6 { +0.00/13 172ms } 23. Rb1 { +0.12/12 94ms } 23... Nd5 { -0.02/12 297ms } 24. Rc1 { +0.07/12 62ms } 24... f6 { +0.00/13 157ms } 25. Rxc5 { +0.05/12 62ms } 25... fxe5 { +0.00/15 109ms } 26. f5 { +0.00/14 157ms } 26... Ne3 { +0.00/15 62ms } 27. Rxe5 { +0.00/14 63ms } 27... Nxf5 { +0.00/14 62ms } 28. Rxe6 { +0.00/14 94ms } 28... Nxd6 { +0.00/13 94ms } 29. Rxd6 { +0.00/12 62ms } 29... Rc8 { +0.00/14 63ms } 30. h3 { -0.04/10 62ms } 30... Rc2 { +0.00/12 63ms } 31. Rd7 { -0.01/12 78ms } 31... h6 { +0.09/15 125ms } 32. h4 { +0.00/13 94ms } 32... Kh7 { +0.00/15 63ms } 33. Rd6 { -0.02/13 78ms } 33... h5 { +0.00/16 62ms } 34. Kf1 { +0.00/17 110ms } 34... Ra2 { +0.00/17 62ms } 35. Rb6 { +0.00/17 63ms } 35... Rd2 { +0.00/19 93ms } 36. Re6 { +0.00/18 63ms } 36... Rc2 { +0.00/18 62ms } 37. Rb6 { +0.00/21 63ms } 37... Ra2 { +0.00/20 62ms } 38. Rc6 { +0.00/21 79ms } 38... Rb2 { +0.00/20 62ms } 39. Ra6 { +0.00/20 94ms } 39... Rc2 { +0.00/21 125ms } 40. Rb6 { +0.00/26 62ms } 40... g6 { +0.00/18 63ms } 41. Rb7+ { +0.00/15 94ms } 41... Kh6 { +0.00/23 62ms } 42. Rd7 { +0.00/19 63ms } 42... Ra2 { +0.00/22 47ms } 43. Rb7 { +0.00/19 62ms } 43... Rc2 { +0.00/22 47ms } 44. Rd7 { +0.00/34 63ms } 44... Ra2 { +0.00/25 93ms } 45. Rb7 { +0.00/31 78ms } 45... Rc2 { +0.00/25 79ms } 46. Rd7 { +0.00/38 62ms } 46... Ra2 { +0.00/26 78ms } 47. Rb7 { +0.00/36 78ms } 47... Rc2 { +0.00/26 47ms } 48. Rd7 { +0.00/42 63ms } 48... Ra2 { +0.00/26 47ms } 49. Rb7 { +0.00/39 125ms } 49... Rc2 { +0.00/26 63ms } 1/2-1/2

```

### Features
* Can run game matches in parallel.
* Zero interface lags, engine will get its remaining time based on its reported spent time.
* Supports fen/epd and pgn files as a source of opening start positions.

### Limitations
* Can only run engine vs engine match.
* No command line support to modify engine and other settings. The source combat.py has to be modified.
* Only uci engines are supported.

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
