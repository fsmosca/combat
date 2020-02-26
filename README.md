# Combat
A python script to run engine vs engine game matches.

### Requirements
* Python 3.7.x or later
* Python-chess

### Guide
Edit the source combat.py to define engine locations, options and names.
```
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
    randomize_fen = True
    reverse_start_side = True
    max_round = 50
    parallel = 6  # No. of game matches to run in parallel
    
    # Time control
    base_time_ms = 5000
    inc_time_ms = 50
    
    # Adjust time odds, should be 1 or more
    bt_time_odds = [1, 1]  # bt is base time
    it_time_odds = [1, 1]  # it is increment time
```

### Features
* Can run game matches in parallel.
* Zero interface lags, engine will get its remaining time based on its reported spent time.

### Limitations
* Can only run engine vs engine match.
* No command line support to set engines and other settings. The source has to be modified.
* PGN format for opening start positions is not supported, only epd file.
* Only uci engines are supported.

### Testing
Tested to run on the following conditions:
* Windows 10
* Python 3.7
* Python-chess v0.30.1

### Credits
* Python-chess  
https://github.com/niklasf/python-chess
