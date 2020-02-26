# -*- coding: utf-8 -*-
"""
combat.py

Description:
    Play games between 2 chess engines.

Tested on:
    python 3.7.4
    python-chess v0.30.1
    windows 10
    
"""


import sys
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import time
import random
import chess.pgn
import chess.engine
import logging


# Increase limit to fix RecursionError
sys.setrecursionlimit(10000)  


# Change log level to logging.DEBUG to enable engine logging.
log_level = logging.INFO
log_format = '%(asctime)s - %(levelname)s - tid=%(thread)d - %(message)s'    
logging.basicConfig(filename='log_combat.log', filemode='w', level=log_level,
                    format=log_format)


class Timer():
    def __init__(self, btms, itms):
        """ 
        btms: base time in ms
        itms: inc time in ms
        """
        self.btms = btms
        self.itms = itms
        self.rem_time = btms
        self.tf = False  # tf is time forfeit
        
    def update_time(self, elapse):
        """ 
        elapse: time in ms spent on a search
        """        
        if self.rem_time - int(elapse) < 1:
            logging.warning('Remaining time is below 1ms before adding the increment!')
            self.tf = True
        
        self.rem_time += self.itms - int(elapse)
        logging.info(f'Updated remaining time: {self.rem_time:0.0f}')


class Match():    
    def __init__(self, fen, eng_file1, eng_file2, eng_opt1, eng_opt2,
                 eng_name1, eng_name2, clock, round_num, total_games, gid):
        self.fen = fen
        self.eng_file1 = eng_file1
        self.eng_file2 = eng_file2
        self.eng_opt1 = eng_opt1
        self.eng_opt2 = eng_opt2
        self.eng_name1 = eng_name1
        self.eng_name2 = eng_name2
        self.clock = clock
        self.round_num = round_num  # for pgn header
        self.total_games = total_games
        self.time_forfeit = [False, False]        
        self.eng_name = [eng_name1, eng_name2]
        self.write_time_forfeit_result = True
        self.gid = gid  # game id

    def update_headers(self, game, board, wplayer, bplayer):
        ga = chess.pgn.Game()
        g = ga.from_board(board)
        try:
            game.headers['FEN'] = g.headers['FEN']    
        except:
            pass
        
        if not self.time_forfeit[1] and not self.time_forfeit[0]:
            game.headers['Result'] = g.headers['Result']
            
            if board.is_checkmate():
                game.headers['Termination'] = 'checkmate'
            elif board.is_stalemate():
                game.headers['Termination'] = 'stalemate'
            elif board.is_insufficient_material():
                game.headers['Termination'] = 'insufficient material'
            elif board.can_claim_fifty_moves():
                game.headers['Termination'] = 'fifty moves'            
            elif board.is_repetition(count=3):
                game.headers['Termination'] = 'threefold repetition'
            else:
                game.headers['Termination'] = 'unknown'
        else:
            game.headers['Termination'] = 'time forfeit'
            if self.write_time_forfeit_result:
                if self.time_forfeit[1]:
                    game.headers['Result'] = '0-1'
                else:
                    game.headers['Result'] = '1-0'
            else:
                game.headers['Result'] = '*'
                game.headers['Termination'] = 'unterminated'
        
        game.headers['Round'] = self.round_num
        game.headers['White'] = wplayer
        game.headers['Black'] = bplayer
        
        game.headers['WhiteTimeControl'] = \
            f'{self.clock[1].btms/1000:0.0f}s+{self.clock[1].itms/1000:0.2f}s'
        game.headers['BlackTimeControl'] = \
            f'{self.clock[0].btms/1000:0.0f}s+{self.clock[0].itms/1000:0.2f}s'

        return game
    
    def get_search_info(self, result, info):
        if info == 'score':
            score = None
            try:
                score = result.info[info].relative.score(mate_score=32000)
            except KeyError as e:
                logging.warning(e)
            except Exception:
                logging.exception(f'Exception in getting {info} from search info.')
                logging.debug(result)
                
            return score
        
        elif info == 'depth':
            depth = None
            try:
                depth = result.info[info]
            except KeyError as e:
                logging.warning(e)
            except Exception:
                logging.exception(f'Exception in getting {info} from search info.')
                logging.debug(result)
                
            return depth
        
        elif info == 'time':
            time = None
            try:
                time = result.info[info] * 1000
            except KeyError as e:
                logging.warning(e)
            except Exception:
                logging.exception(f'Exception in getting {info} from search info.')
                logging.debug(result)
                
            return time
        
        elif info == 'nodes':
            nodes = None
            try:
                nodes = result.info[info]
            except KeyError as e:
                logging.warning(e)
            except Exception:
                logging.exception(f'Exception in getting {info} from search info.')
                logging.debug(result)
                
            return nodes
        
        return None
    
    def start_match(self):        
        eng = [chess.engine.SimpleEngine.popen_uci(self.eng_file1),
                chess.engine.SimpleEngine.popen_uci(self.eng_file2)]
        
        # Set options
        for k, v in self.eng_opt1.items():
            eng[0].configure({k: v})
        for k, v in self.eng_opt2.items():
            eng[1].configure({k: v})        
        
        game = chess.pgn.Game()
        node = game
        
        board = chess.Board(self.fen)
        
        logging.info(f'Starting game {self.gid} of {self.total_games}, round: {self.round_num}, ({self.eng_name2} vs {self.eng_name1})')
        print(f'Starting game {self.gid} / {self.total_games}, round: {self.round_num}, ({self.eng_name2} vs {self.eng_name1})')
        
        # First engine with index 0 will handle the black side.
        self.clock[1].rem_time = self.clock[1].btms
        self.clock[0].rem_time = self.clock[0].btms
        
        # Play the game, till its over by python-chess
        # while not board.is_game_over(claim_draw=True): 
        while not board.is_game_over():          
            t1 = time.perf_counter_ns()
            
            # Let engine search for the best move of the given board.
            result = eng[board.turn].play(board, chess.engine.Limit(
                white_clock=self.clock[1].rem_time/1000,
                black_clock=self.clock[0].rem_time/1000,
                white_inc=self.clock[1].itms/1000,
                black_inc=self.clock[0].itms/1000),
                info=chess.engine.INFO_SCORE)
            
            # Get score, depth and time for move comments.
            score_cp = self.get_search_info(result, 'score')
            depth = self.get_search_info(result, 'depth')
            time_ms = self.get_search_info(result, 'time')
            
            if time_ms is None:
                time_ms = (time.perf_counter_ns() - t1)/1000/1000  # in ms
            time_ms = max(1, time_ms)  # Set a minimum of 1ms
                
            self.clock[board.turn].update_time(time_ms)
            self.time_forfeit[board.turn] = self.clock[board.turn].tf
            
            # Save move and comment                
            node = node.add_variation(result.move)
            if score_cp is not None and depth is not None and time_ms is not None:
                node.comment = f'{score_cp/100:+0.2f}/{depth} {time_ms:0.0f}ms' 
                
            # Stop the game if time limit is exceeded.
            if self.clock[board.turn].tf:
                logging.warning(f'round: {self.round_num}, {"white" if not board.turn else "black"} loses on time!')
                print(f'round: {self.round_num}, {"white" if not board.turn else "black"} loses on time!')
                break
                
            # Update the board with the move for next player
            board.push(result.move)            
        
        eng[0].quit()
        eng[1].quit()
        
        game = self.update_headers(game, board, self.eng_name2, self.eng_name1)
        
        return [game, self.gid, self.round_num, self.time_forfeit]
    
    
def update_score(g, n1, n2, s1, s2, d1, d2):
    """ 
    n1, n2 are engine names
    s1, s2 are scores
    d1, d2 are number of draws
    """
    res = g.headers['Result']
    wp = g.headers['White']
    bp = g.headers['Black']
    
    if res == '1-0':
        if wp == n1:
            s1 += 1
        elif wp == n2:
            s2 += 1
    elif res == '0-1':
        if bp == n1:
            s1 += 1
        elif bp == n2:
            s2 += 1
    elif res == '1/2-1/2':
        s1 += 0.5
        s2 += 0.5
        d1 += 1
        d2 += 1
        
    return s1, s2, d1, d2


def get_fen_list(fn, mr, randomize_fen=False):
    """ 
    Read fen file and return fen list.
    """
    fens = []
    pos = 0
    
    with open(fn) as h:
        for lines in h:
            pos += 1
            fen = lines.strip()
            fens.append(fen)
            if pos >= mr:
                break
            
    if randomize_fen:
        random.shuffle(fens)

    return fens


def print_match_conditions(max_round, reverse_start_side, opening_file,
                           randomize_fen, parallel, base_time_ms, inc_time_ms):
    print(f'rounds        : {max_round}')
    print(f'revese side   : {reverse_start_side}')
    print(f'total games   : {max_round*2 if reverse_start_side else max_round}')
    print(f'opening file  : {opening_file}')
    print(f'randomize fen : {randomize_fen}')        
    print(f'base time(ms) : {base_time_ms}')
    print(f'inc time(ms)  : {inc_time_ms}')
    print(f'parallel      : {parallel}\n')
    
    
def main():    
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
    
    bt1 = base_time_ms/max(1, bt_time_odds[0])
    bt2 = base_time_ms/max(1, bt_time_odds[1])
    
    it1 = inc_time_ms/max(1, it_time_odds[0])
    it2 = inc_time_ms/max(1, it_time_odds[1])
    
    # Set each engine clocks
    clock = [Timer(bt1, it1), Timer(bt2, it2)]
    
    print_match_conditions(max_round, reverse_start_side, opening_file,
                           randomize_fen, parallel, base_time_ms, inc_time_ms)
    
    # Init vars, s for score, d for draw, tf for time forfeit
    s1, s2, d1, d2, tf1, tf2 = 0, 0, 0, 0, 0, 0
    analysis = []
    round_num = 0
    num_res = 0
    
    # Save opening positions to a list
    fens = get_fen_list(opening_file, max_round, randomize_fen)
    total_games = len(fens) * 2 if reverse_start_side else 1
    
    # Run game matches in parallel
    with ProcessPoolExecutor(max_workers=parallel) as executor:
        game_id = 0
        for fen in fens:
            game_id += 1
            round_num += 1
            sub_round = 0.1
            g = Match(
                fen, eng_file1, eng_file2, eng_opt1, eng_opt2, eng_name1,
                eng_name2, clock,
                round_num + sub_round if reverse_start_side else round_num,
                total_games, game_id)
            job = executor.submit(g.start_match)            
            analysis.append(job)
            
            if reverse_start_side:
                game_id += 1
                sub_round += 0.1
                swap_clock = [clock[1], clock[0]]
                g = Match(
                    fen, eng_file2, eng_file1, eng_opt2, eng_opt1, eng_name2,
                    eng_name1, swap_clock,
                    round_num + sub_round if reverse_start_side else round_num,
                    total_games, game_id)
                job = executor.submit(g.start_match)            
                analysis.append(job)
            
        for future in concurrent.futures.as_completed(analysis):
            try:
                game = future.result()[0]
                game_num = future.result()[1]
                round_number = future.result()[2]
                tf = future.result()[3]
                
                num_res += 1                
                tf1 += tf[0]
                tf2 += tf[1]
                
                wp = game.headers['White']
                bp = game.headers['Black']
                res = game.headers['Result']
                termi = game.headers['Termination']
                
                # Save games to a file
                print(game, file=open(outpgn, 'a'), end='\n\n')
                
                s1, s2, d1, d2 = update_score(
                    game, eng_name1, eng_name2, s1, s2, d1, d2)
                
                logging.info(f'Done game {game_num}, round: {round_number}, ({wp} vs {bp}): {res} ({termi})')
                print(f'Done game {game_num}, round: {round_number}, ({wp} vs {bp}): {res} ({termi})')
                
                # Print result table.                
                # Get max length of names for print formatting.
                name_len = max(8, max(len(eng_name2), len(eng_name1)))
                
                print('\n%-*s %9s %9s %7s %7s %4s' % (
                    name_len, 'name', 'score', 'games', 'score%', 'Draw%',
                    'tf'))
                print('%-*s %9.1f %9d %7.1f %7.1f %4d' % (
                    name_len, eng_name1, s1, num_res, 100*s1/num_res,
                    100*d1/num_res, tf1))
                print('%-*s %9.1f %9d %7.1f %7.1f %4d\n' % (
                    name_len, eng_name2, s2, num_res, 100*s2/num_res,
                    100*d2/num_res, tf2))
                
            except Exception:
                logging.exception('Exception in completed analysis.')
    
    logging.shutdown()
    

if __name__ == '__main__':
    main()
    