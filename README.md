# Combat
A python script to run engine vs engine game matches.

### Requirements
* Python 3.7.x or later
* Python-chess

### Guide
Edit the source combat.py to define engine locations, options, names and others, then execute combat.py.
```python
    outpgn = 'combat_auto_save_games.pgn'
    
    # Start opening file
    opening_file = 'grand_swiss_2019_6plies.pgn'
    
    # Define json file where engines are located. You can use
    # engines.json file from cutechess program or combat.json.
    engine_json = 'combat.json'
    
    # eng_name 1 and 2 should be present in engine json file.
    eng_name1 = 'Deuterium v2019.2'
    eng_name2 = 'Deuterium v2019.2 kingshelter150 kingattack150'
    
    # Get eng file and options from engine json file
    eng_file1, eng_opt1 = get_engine_data(engine_json, eng_name1)        
    eng_file2, eng_opt2 = get_engine_data(engine_json, eng_name2)
    
    # Match options    
    randomize_pos = True
    reverse_start_side = True
    max_round = 50
    parallel = 6  # No. of game matches to run in parallel
    
    # Time control
    base_time_ms = 5000
    inc_time_ms = 50
    
    # Adjust time odds, must be 1 or more. The first 1 in [1, 1] will be for engine1.
    # If [2, 1], time of engine1 will be reduced by half.
    bt_time_odds = [1, 1]  # bt is base time
    it_time_odds = [1, 1]  # it is increment time
    
    bt1 = base_time_ms/max(1, bt_time_odds[0])
    bt2 = base_time_ms/max(1, bt_time_odds[1])
    
    it1 = inc_time_ms/max(1, it_time_odds[0])
    it2 = inc_time_ms/max(1, it_time_odds[1])
    
    # Win score adjudication options
    win_adjudication = True
    win_score_cp = 700
    win_score_count = 4
```
Example run:
```
Preparing start openings...
elapse:  0.004s
Done preparing start openings!

rounds           : 10
reverse side     : True
total games      : 20
opening file     : grand_swiss_2019_6plies.pgn
randomize fen    : True
base time(ms)    : 5000
inc time(ms)     : 50
win adjudication : True
win score cp     : 700
win score count  : 4
parallel         : 6

Starting game 1 / 20, round: 1.1, (Deuterium mobility_wt_150 vs Deuterium kingattack_wt_150)
Starting game 2 / 20, round: 1.2, (Deuterium kingattack_wt_150 vs Deuterium mobility_wt_150)
Starting game 3 / 20, round: 2.1, (Deuterium mobility_wt_150 vs Deuterium kingattack_wt_150)
Starting game 4 / 20, round: 2.2, (Deuterium kingattack_wt_150 vs Deuterium mobility_wt_150)
Starting game 6 / 20, round: 3.2, (Deuterium kingattack_wt_150 vs Deuterium mobility_wt_150)
Starting game 5 / 20, round: 3.1, (Deuterium mobility_wt_150 vs Deuterium kingattack_wt_150)
Done game 1, round: 1.1, (Deuterium mobility_wt_150 vs Deuterium kingattack_wt_150): 1/2-1/2 (threefold repetition)

name                            score     games  score%   Draw%   tf
Deuterium kingattack_wt_150       0.5         1    50.0   100.0    0
Deuterium mobility_wt_150         0.5         1    50.0   100.0    0

Starting game 7 / 20, round: 4.1, (Deuterium mobility_wt_150 vs Deuterium kingattack_wt_150)
Done game 2, round: 1.2, (Deuterium kingattack_wt_150 vs Deuterium mobility_wt_150): 1/2-1/2 (threefold repetition)

name                            score     games  score%   Draw%   tf
Deuterium kingattack_wt_150       1.0         2    50.0   100.0    0
Deuterium mobility_wt_150         1.0         2    50.0   100.0    0

Starting game 8 / 20, round: 4.2, (Deuterium kingattack_wt_150 vs Deuterium mobility_wt_150)
Done game 6, round: 3.2, (Deuterium kingattack_wt_150 vs Deuterium mobility_wt_150): 1/2-1/2 (threefold repetition)

name                            score     games  score%   Draw%   tf
Deuterium kingattack_wt_150       1.5         3    50.0   100.0    0
Deuterium mobility_wt_150         1.5         3    50.0   100.0    0

....

Done game 19, round: 10.1, (Deuterium mobility_wt_150 vs Deuterium kingattack_wt_150): 0-1 (adjudication: good score for black)

name                            score     games  score%   Draw%   tf
Deuterium kingattack_wt_150       8.5        19    44.7    36.8    0
Deuterium mobility_wt_150        10.5        19    55.3    36.8    0

Done game 20, round: 10.2, (Deuterium kingattack_wt_150 vs Deuterium mobility_wt_150): 1/2-1/2 (threefold repetition)

name                            score     games  score%   Draw%   tf
Deuterium kingattack_wt_150       9.0        20    45.0    40.0    0
Deuterium mobility_wt_150        11.0        20    55.0    40.0    0

Match: done, elapse: 44s
```
Example pgn output:
```
[Event "Computer games"]
[Site "Combat"]
[Date "2020.02.28"]
[Round "1.1"]
[White "Deuterium mobility_wt_150"]
[Black "Deuterium kingattack_wt_150"]
[Result "0-1"]
[BlackTimeControl "5s+0.05s"]
[Termination "adjudication: good score for black"]
[WhiteTimeControl "5s+0.05s"]

1. d4 Nf6 2. c4 e6 3. Nf3 b6 4. Nc3 { +0.63/7 140ms } 4... d5 { -0.78/8 94ms } 5. Bg5 { +0.62/7 140ms } 5... Be7 { -0.19/9 94ms } 6. cxd5 { +0.82/9 110ms } 6... exd5 { -0.31/12 140ms } 7. e3 { +0.87/11 78ms } 7... O-O { -0.26/13 141ms } 8. Bd3 { +0.57/11 125ms } 8... h6 { -0.32/12 171ms } 9. Bxf6 { +0.63/12 172ms } 9... Bxf6 { -0.42/11 94ms } 10. O-O { +0.53/11 156ms } 10... c6 { -0.32/10 141ms } 11. h3 { +0.69/10 125ms } 11... Re8 { -0.46/9 125ms } 12. Re1 { +0.75/9 78ms } 12... Be6 { -0.60/9 94ms } 13. Rc1 { +0.91/8 109ms } 13... Nd7 { -0.59/9 109ms } 14. Kh1 { +0.75/9 94ms } 14... Nf8 { -0.17/8 94ms } 15. Qd2 { +0.38/8 78ms } 15... a6 { -0.11/9 110ms } 16. e4 { +0.59/8 78ms } 16... b5 { -0.40/11 140ms } 17. exd5 { +0.67/9 79ms } 17... cxd5 { -0.11/11 109ms } 18. a4 { +0.32/10 109ms } 18... b4 { -0.67/11 110ms } 19. Ne2 { +0.27/10 78ms } 19... Qa5 { -0.36/10 78ms } 20. b3 { +0.29/9 78ms } 20... Rac8 { -0.05/10 78ms } 21. g4 { +0.19/10 125ms } 21... Bd7 { +0.08/11 188ms } 22. Bf5 { +0.10/10 109ms } 22... Ne6 { +0.05/10 63ms } 23. Ne5 { +0.55/11 78ms } 23... Bxe5 { -0.11/11 63ms } 24. dxe5 { +0.45/10 79ms } 24... d4 { +0.33/11 93ms } 25. Bxe6 { +0.25/10 63ms } 25... Bxe6 { +1.15/10 62ms } 26. Rxc8 { -0.52/11 63ms } 26... Rxc8 { +0.97/12 62ms } 27. Nxd4 { -0.59/13 78ms } 27... Rd8 { +1.38/13 63ms } 28. Kg1 { -0.82/15 187ms } 28... Qb6 { +0.86/14 110ms } 29. Re4 { -0.69/13 94ms } 29... Bxb3 { +1.02/13 62ms } 30. a5 { -0.62/13 109ms } 30... Qb7 { +0.75/12 94ms } 31. Re1 { -0.66/12 110ms } 31... Bc4 { +1.14/12 125ms } 32. Rc1 { -1.01/11 78ms } 32... b3 { +1.01/11 62ms } 33. Qb2 { -0.81/12 94ms } 33... Bd5 { +0.99/10 62ms } 34. Nf5 { -0.81/10 78ms } 34... Bh1 { +0.91/8 63ms } 35. Ne3 { -0.93/11 93ms } 35... Be4 { +0.79/10 79ms } 36. Rc4 { -1.08/12 171ms } 36... Bd3 { +1.15/11 63ms } 37. Rc1 { -1.01/10 125ms } 37... Qf3 { +1.19/11 62ms } 38. Rd1 { -0.92/11 79ms } 38... Rd5 { +1.12/11 62ms } 39. Kh2 { -1.43/14 94ms } 39... Kh7 { +1.05/11 78ms } 40. h4 { -1.25/11 125ms } 40... Rd8 { +1.70/12 62ms } 41. h5 { -0.78/10 79ms } 41... Rd7 { +1.70/10 62ms } 42. Rd2 { -0.93/12 63ms } 42... Bb5 { +1.62/12 62ms } 43. Rd6 { -1.02/12 63ms } 43... Bc6 { +2.10/12 125ms } 44. Rxd7 { -1.21/12 78ms } 44... Bxd7 { +1.98/11 62ms } 45. Kg1 { -1.26/11 125ms } 45... Bc6 { +1.52/11 63ms } 46. Kf1 { -0.94/11 78ms } 46... Bd5 { +1.51/10 141ms } 47. Qc3 { -0.99/13 78ms } 47... Be6 { +2.13/11 110ms } 48. Qb4 { -1.02/10 62ms } 48... Qh1+ { +1.89/11 203ms } 49. Ke2 { -1.18/3 1ms } 49... Qb1 { +2.54/9 63ms } 50. Qd4 { -1.51/8 79ms } 50... b2 { +3.35/9 62ms } 51. Qc3 { -5.12/9 78ms } 51... Qa2 { +11.17/10 63ms } 52. Qc2+ { -10.96/12 109ms } 52... Kg8 { +11.60/14 125ms } 53. f4 { -11.66/12 94ms } 53... b1=Q { +12.75/14 63ms } 54. Qxa2 { -11.97/11 94ms } 54... Qxa2+ { +13.19/13 94ms } 55. Kd3 { -12.39/14 156ms } 0-1
```

### Features
* Can run game matches in parallel.
* Zero interface lags, engine will get its remaining time based on its reported spent time.
* Supports fen/epd and pgn files as a source of opening start positions.
* Can adjudicate games based on winning score.
* Can read engine settings from combat.json file or cutechess engines.json file.

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
