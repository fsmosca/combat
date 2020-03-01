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
from pathlib import Path  # Python 3.4
import time
from datetime import datetime
import random
import collections
import argparse
import json
import chess.pgn
import chess.engine
import logging


APP_NAME = 'combat'
APP_VERSION = 'v1.12'


# Increase limit to fix RecursionError
sys.setrecursionlimit(10000)  


# Change log level to logging.DEBUG to enable engine logging by python-chess.
# Change log level to logging.info to see combat logging.
# Set log level to logging.CRITICAL to only get critical logging.
log_level = logging.CRITICAL
log_format = '%(asctime)s - %(levelname)5s - %(message)s'    
logging.basicConfig(filename='combat_logging.log', filemode='w', level=log_level, format=log_format)


# Formated help Messages for parser
engine_config_help ='''This is used to define the file where
engine configurations are located. You may use included file combat.json
or you can use engines.json from cutechess.
example:
--engine-config-file combat.json
or using the engines.json from cutechess
--engine-config-file "d:/chess/cutechess/engines.json"'''

engine_help ='''This option is used to define the engines
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
      engine1 will play as white and engine2 will play as black'''

opening_help ='''Opening file is used by engine to start the game. You
may use pgn or epd or fen formats.
example:
--opening file=start.pgn random=true
or with file path
--opening file="d:/chess/opening_start.pgn" random=true
or with epd file
--opening file="d:/chess/opening.epd" random=true
or to not use random
--opening file="d:/chess/opening.epd" random=false'''

parallel_help ='''Option to run game matches in parallel
example:
--parallel 1
default is 1, but if your cpu has more than 1 cores or threads
lets say 8, you may use
--parallel 7'''
win_adjudication_help ='''Option to stop the game when one side is
already ahead on score. Both engines would agree that one side
is winning and the other side is lossing.
example:
--win-adjudication score=700 count=4
where:
    score: engine score in cp
    count: number of times the score is recorded'''
        

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


class Match():    
    def __init__(self, start_game, eng_files, eng_opts, eng_names, clock,
                 round_num, total_games, game_id, adjudication=False,
                 win_score_cp=700, win_score_count=4):
        self.start_game = start_game
        self.eng_files = eng_files
        self.eng_opts = eng_opts
        self.eng_names = eng_names
        self.clock = clock
        self.round_num = round_num  # for pgn header
        self.total_games = total_games
        self.time_forfeit = [False, False]
        self.write_time_forfeit_result = True
        self.game_id = game_id
        self.adjudication = adjudication
        self.win_score_cp = win_score_cp
        self.win_score_count = win_score_count

    def update_headers(self, game, board, wplayer, bplayer, score_adjudication, elapse):
        ga = chess.pgn.Game()
        g = ga.from_board(board)
        
        game.headers['Event'] = 'Computer games'
        game.headers['Site'] = 'Combat'
        game.headers['Date'] = datetime.today().strftime('%Y.%m.%d')
        
        try:
            game.headers['FEN'] = g.headers['FEN']    
        except:
            pass
        
        if self.time_forfeit[1] or self.time_forfeit[0]:
            game.headers['Termination'] = 'time forfeit'
            
            if self.write_time_forfeit_result:
                if self.time_forfeit[1]:
                    game.headers['Result'] = '0-1'
                else:
                    game.headers['Result'] = '1-0'
            else:
                game.headers['Result'] = '*'
                game.headers['Termination'] = 'unterminated'
        
        # Win score adjudication
        elif score_adjudication[0] or score_adjudication[1]:
            adj_value = 'adjudication: good score for white' if score_adjudication[1] else 'adjudication: good score for black'
            game.headers['Termination'] = adj_value
            
            game.headers['Result'] = '1-0' if score_adjudication[1] else '0-1'            
        
        else:
            game.headers['Result'] = g.headers['Result']
            
            if board.is_checkmate():
                game.headers['Termination'] = 'checkmate'
                
            elif board.is_stalemate():
                game.headers['Termination'] = 'stalemate'
                
            elif board.is_insufficient_material():
                game.headers['Termination'] = 'insufficient mating material'
                
            elif board.can_claim_fifty_moves():
                game.headers['Termination'] = 'fifty-move draw rule' 
                
            elif board.is_repetition(count=3):
                game.headers['Termination'] = 'threefold repetition'
                
            else:
                # Todo: Check the game if this is triggered, not encountered so far.
                game.headers['Termination'] = 'unknown'
        
        game.headers['Round'] = self.round_num
        game.headers['White'] = wplayer
        game.headers['Black'] = bplayer
        
        game.headers['WhiteTimeControl'] = \
            f'{get_time_h_mm_ss_ms(self.clock[1].btms*1000000)} + {get_time_h_mm_ss_ms(self.clock[1].itms*1000000, True)}'
        game.headers['BlackTimeControl'] = \
            f'{get_time_h_mm_ss_ms(self.clock[0].btms*1000000)} + {get_time_h_mm_ss_ms(self.clock[0].itms*1000000, True)}'
            
        game.headers['GameDuration'] = get_time_h_mm_ss_ms(elapse)

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
    
    def win_score_adjudication(self, wscores, bscores):
        """
        Adjudicate game by score, scores of one side should be successively
        winning and the scores of other side are successively losing.
        
        wscores: a list of white scores
        bscores: a list of black scores
        
        Return: 
            [True, False] if game is good for black
            [False, True] if game is good for white
            [False, False] if game is not to be adjudicated
        """
        n = self.win_score_count  # Default 4
        w = self.win_score_cp  # Default 700
        ret = [False, False]  # [Black, white]
        
        if len(wscores) < n or len(bscores) < n:
            return ret
        
        # (1) White wins
        w_good_cnt, b_bad_cnt = 0, 0
        for s in wscores[-n:]:  # Check the last n scores
            if s >= w:
                w_good_cnt += 1
                
        for s in bscores[-n:]:
            if s <= -w:
                b_bad_cnt += 1
                
        if w_good_cnt >= n and b_bad_cnt >= n:
            return [False, True]
        
        # (2) Black wins
        w_bad_cnt, b_good_cnt = 0, 0
        for s in bscores[-n:]:
            if s >= w:
                b_good_cnt += 1
                
        for s in wscores[-n:]:
            if s <= -w:
                w_bad_cnt += 1
                
        if b_good_cnt >= n and w_bad_cnt >= n:
            return [True, False]
        
        return ret
    
    def start_match(self):
        # Save score info per move from both engines for score adjudications
        eng_score = {0: [], 1: []}
        score_adjudication = [False, False]
        
        eng = [chess.engine.SimpleEngine.popen_uci(self.eng_files[0]),
                chess.engine.SimpleEngine.popen_uci(self.eng_files[1])]
        
        # Set options
        for k, v in self.eng_opts[0].items():
            eng[0].configure({k: v})
        for k, v in self.eng_opts[1].items():
            eng[1].configure({k: v})           
        
        # Create a board which will be played by engines.
        end_node = self.start_game.end()
        end_board = end_node.board()
        board = end_board.copy()
        
        # Create a game for annotated game output.
        game = chess.pgn.Game()
        game = game.from_board(end_board)
        node = game.end()
        
        logging.info(f'Starting, game: {self.game_id} of {self.total_games}, round: {self.round_num}, players: {self.eng_names[1]} vs {self.eng_names[0]}')
        print(f'Starting, game: {self.game_id} / {self.total_games}, round: {self.round_num}, players: {self.eng_names[1]} vs {self.eng_names[0]}')
        
        # First engine with index 0 will handle the black side.
        self.clock[1].rem_time = self.clock[1].btms
        self.clock[0].rem_time = self.clock[0].btms
        
        game_start = time.perf_counter_ns()
        
        # Play the game, till its over by python-chess
        while not board.is_game_over():
            # Get init time in case the engine does not send its time info.
            t1 = time.perf_counter_ns()
            
            # Let engine search for the best move of the given board.
            result = eng[board.turn].play(board, chess.engine.Limit(
                white_clock=self.clock[1].rem_time/1000,
                black_clock=self.clock[0].rem_time/1000,
                white_inc=self.clock[1].itms/1000,
                black_inc=self.clock[0].itms/1000),
                info=chess.engine.INFO_SCORE)
            
            # Get score, depth and time for move comments in pgn output.
            score_cp = self.get_search_info(result, 'score')
            depth = self.get_search_info(result, 'depth')
            time_ms = self.get_search_info(result, 'time')
            
            # Save score for game adjudication based on engine score
            eng_score[board.turn].append(0 if score_cp is None else score_cp)
            
            # If engine does not give time spent, calculate elapse time manually.
            if time_ms is None:
                time_ms = (time.perf_counter_ns() - t1)//1000//1000  # from nano to ms
            time_ms = max(1, time_ms)  # If engine sent time below 1, use a minimum of 1ms
                
            # Update time and determine if engine exceeds allocated time.
            self.clock[board.turn].update_time(time_ms)
            self.time_forfeit[board.turn] = self.clock[board.turn].tf
            
            # Save move and comment in pgn output file.               
            node = node.add_variation(result.move)
            if score_cp is not None and depth is not None and time_ms is not None:
                node.comment = f'{score_cp/100:+0.2f}/{depth} {time_ms:0.0f}ms'

            # Stop the game if time limit is exceeded.
            if self.clock[board.turn].tf:
                logging.warning(f'round: {self.round_num}, infraction: {"white" if board.turn else "black"} loses on time!')
                print(f'round: {self.round_num}, infraction: {"white" if board.turn else "black"} loses on time!')
                break
                
            # Update the board with the move for next player
            board.push(result.move) 
            
            # Stop game by score adjudication
            if self.adjudication:
                score_adjudication = self.win_score_adjudication(
                    eng_score[chess.WHITE], eng_score[chess.BLACK])
            
            if score_adjudication[0] or score_adjudication[1]:
                break                    
        
        eng[0].quit()
        eng[1].quit()
        
        elapse = time.perf_counter_ns() - game_start        
        game = self.update_headers(game, board, self.eng_names[1],
                                   self.eng_names[0], score_adjudication,
                                   elapse)
        
        return [game, self.game_id, self.round_num, elapse]


def get_time_h_mm_ss_ms(time_ns, mmssms = False):
        """
        Converts time delta to hh:mm:ss:ms format.
        
        time_ns: time delta in nanoseconds
        return: time in h:m:s:ms format
        """
        time_ms = time_ns//1000000
        s, ms = divmod(time_ms, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)

        if mmssms:
            return '{:02d}m:{:02d}s:{:03d}ms'.format(m, s, ms)
        return '{:01d}h:{:02d}m:{:02d}s:{:03d}ms'.format(h, m, s, ms)
    
    
def print_result_table(scores, num_res):
    tname = [None, None]
    tname[0] = list(scores.keys())[0]
    tname[1] = list(scores.keys())[1]
    
    name_len = max(8, max(len(tname[0]), len(tname[1])))
    
    # Result table header
    print('\n%-*s %9s %9s %7s %7s %4s' % (
        name_len, 'name', 'score', 'games', 'score%', 'Draw%', 'tf'))
    
    # Table data
    for i in range(len(tname)):
        print('%-*s %9.1f %9d %7.1f %7.1f %4d' % (
            name_len,
            tname[i],
            scores[tname[i]]['score'],
            num_res,
            100*scores[tname[i]]['score']/num_res,
            100*scores[tname[i]]['draws']/num_res,
            scores[tname[i]]['tf']))
    print()
    

def update_score(g, scores):
    """ 
    scores = {names[0]: {'score': 0, 'draws': 0, 'tf': 0},
              names[1]: {'score': 0, 'draws': 0, 'tf': 0}}
    """
    res = g.headers['Result']
    wp = g.headers['White']
    bp = g.headers['Black']
    termi = g.headers['Termination']
    
    n1 = list(scores.keys())[0]
    n2 = list(scores.keys())[1]
    s1 = scores[n1]['score']
    s2 = scores[n2]['score']
    d1 = scores[n1]['draws']
    d2 = scores[n2]['draws']
    tf1 = scores[n1]['tf']
    tf2 = scores[n2]['tf']
    
    if res == '1-0':        
        if wp == n1:
            s1 += 1
            if termi == 'time forfeit':
                tf2 += 1
        elif wp == n2:
            s2 += 1
            if termi == 'time forfeit':
                tf1 += 1
    elif res == '0-1':
        if bp == n1:
            s1 += 1
            if termi == 'time forfeit':
                tf2 += 1
        elif bp == n2:
            s2 += 1
            if termi == 'time forfeit':
                tf1 += 1
    elif res == '1/2-1/2':
        s1 += 0.5
        s2 += 0.5
        d1 += 1
        d2 += 1
        
    scores = {n1: {'score': s1, 'draws': d1, 'tf': tf1},
              n2: {'score': s2, 'draws': d2, 'tf': tf2}}
        
    return scores


def get_game_list(fn, max_round=500, randomize_pos=False):
    """ 
    Converts fn file into python-chess game objects.
    
    fn: can be a fen or an epd or a pgn file
    Return: a list of games
    """
    t1 = time.perf_counter_ns()
    
    games = []
    
    fn_filename = Path(fn).name
    file_suffix = Path(fn).suffix
    
    logging.info(f'Preparing start opening from {fn_filename} ...')
    print(f'Preparing start opening from {fn_filename} ...')
    
    if file_suffix not in ['.pgn', '.fen', '.epd']:
        raise  Exception(f'File {fn} has no extension!, accepted file ext: .pgn, .fen, .epd')
    
    if file_suffix == '.pgn':
        with open(fn) as pgn:
            while True:
                game = chess.pgn.read_game(pgn)
                if game is None:
                    break
                games.append(game)
                if len(games) >= max_round:
                    break
    else:
        with open(fn) as pos:
            for lines in pos:
                line = lines.strip()
                board = chess.Board(line)
                game = chess.pgn.Game()
                game = game.from_board(board)
                games.append(game)
                if len(games) >= max_round:
                    break
                
    if randomize_pos:
        random.shuffle(games)
        
    elapse = time.perf_counter_ns() - t1
    
    if len(games) < max_round:
        logging.warning(f'Number of positions in the file {len(games)} are below max_round {max_round}!')
        print(f'Number of positions in the file {len(games)} are below max_round {max_round}!')
    
    logging.info(f'status: done, games prepared: {len(games)}, elapse: {get_time_h_mm_ss_ms(elapse)}\n')
    print(f'status: done, games prepared: {len(games)}, elapse: {get_time_h_mm_ss_ms(elapse)}\n')
        
    return games


def print_match_conditions(max_round, reverse_start_side, opening_file,
                           randomize_pos, parallel, base_time_ms, inc_time_ms,
                           adjudication, win_score_cp, win_score_count):
    print(f'rounds           : {max_round}')
    print(f'reverse side     : {reverse_start_side}')
    print(f'total games      : {max_round*2 if reverse_start_side else max_round}')
    print(f'opening file     : {opening_file}')
    print(f'randomize fen    : {randomize_pos}')        
    print(f'base time(ms)    : {base_time_ms}')
    print(f'inc time(ms)     : {inc_time_ms}')    
    print(f'win adjudication : {adjudication}')
    print(f'win score cp     : {win_score_cp}')
    print(f'win score count  : {win_score_count}')
    print(f'parallel         : {parallel}\n')
    
    
def get_engine_data(fn, ename):
    """
    Read engine json file to get options etc. of ename.
    
    fn: engine json file
    ename: engine config name to search
    return: eng path and file and its options that are not default
    """
    path_file = None
    opt = {}
    
    with open(fn) as json_file:
        data = json.load(json_file)
        
    for p in data:
        command = p['command']
        work_dir = p['workingDirectory']
        name = p['name']
        
        if name != ename:
            continue
        
        path_file = Path(work_dir, command).as_posix()
        
        for k, v in p.items():
            if k == 'options':
                for o in v:
                    # d = {'name': 'Ponder', 'default': False, 'value': False, 'type': 'check'}
                    opt_name = o['name']
                    
                    try:
                        opt_default = o['default']
                    except KeyError:
                        continue
                    except Exception:
                        logging.exception('Error in getting default option value!')
                        continue
                        
                    opt_value = o['value']
                    if opt_default != opt_value:
                        opt.update({opt_name: opt_value})
        
        return path_file, opt
    

def read_engine_option(engine_option_value):
    players = {}
    
    if len(engine_option_value) == 0:
        return players, None, None
    
    for i, e in enumerate(engine_option_value):
        name, base_time_ms, inc_time_ms = None, None, None
        for v in e:
            par_name = v.split('=')[0]
            par_value = v.split('=')[1]
            if par_name == 'config-name':
                name = par_value
            elif par_name == 'tc':
                tc_val = par_value
                base_time_ms = int(tc_val.split('+')[0])
                try:
                    inc_time_ms = int(tc_val.split('+')[1])
                except IndexError:
                    raise Exception('Time increment is missing!')
                
        d = {i: {'name': name, 'base': base_time_ms, 'inc': inc_time_ms}}
        players.update(d)
        
    players = collections.OrderedDict(sorted(players.items()))
    
    return players, base_time_ms, inc_time_ms

    
def main():   
    print(f'{APP_NAME} {APP_VERSION}')
    
    # Variable that is not available yet in command line options
    max_games_per_round = 2  # For each round, there is only 1 opening.
    
    parser = argparse.ArgumentParser(
        prog='%s' % (APP_NAME),
        description='Run engine vs engine match',
        epilog='%(prog)s' + ' %s' % APP_VERSION,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--engine-config-file', required=True,
                        help=engine_config_help)
    parser.add_argument('--engine', nargs='*', action='append', required=True,
                        help=engine_help)
    parser.add_argument('--opening', nargs='*', required=True, help=opening_help)
    parser.add_argument('--round', default=500, type=int,
                        help='number of games to play, twice if reverse is true')
    parser.add_argument('--reverse', action='store_true',
                        help='A flag when when set, changes start side, to play a position.')
    parser.add_argument('--parallel', default=1, type=int, required=False,
                        help=parallel_help)
    parser.add_argument('--win-adjudication', nargs='*', required=False,
                        help=win_adjudication_help)
    parser.add_argument('--output', default='output_games.pgn',
                        help='Save output games, default=output_games.pgn')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + APP_VERSION)
    
    args = parser.parse_args()
    outpgn = args.output
    parallel = args.parallel  
    max_round = args.round
    reverse_start_side = args.reverse
    
    clock = []  # clock[Timer(), Timer()] index 0 is for black
    
    # --engine-config-file combat.json
    engine_json = args.engine_config_file
    
    # --engine config-name="E1" tc=1000+100 --engine config-name="E2" ...
    # players is a dict {0: {'name': None, 'base': None, 'inc': None}, 1: {} ...}
    players, base_time_ms, inc_time_ms = read_engine_option(args.engine)
    names = [players[0]['name'], players[1]['name']]
        
    # Update clock
    for _, v in players.items():
        clock.append(Timer(v['base'], v['inc']))
    
    # Stop the script if engine config name is not defined
    if names[0] is None or names[1] is None:
        raise Exception('Engine config name was not defined! Use config-name=engine_name')

    # Stop the script if engine clock is not defined
    for i in range(len(names)):
        if players[i]['base'] is None or players[i]['inc'] is None:
            raise Exception(f'{"Black" if i == 0 else "White"} TC was not defined! Use tc=base_time_ms+inc_time_ms')
    
    # --opening file=start.pgn random=False
    opening_file, randomize_pos = None, False
    for v in args.opening:
        value = v.split('=')
        if value[0] == 'file':
            opening_file = value[1]
        elif value[0] == 'random':
            randomize_pos = True if value[1] == 'true' else False
            
    # --win-adjudication score=700 count=4
    win_adj, win_score_cp, win_score_count = False, 700, 4
    if args.win_adjudication is not None:
        win_adj = True
        for v in args.win_adjudication:
            value = v.split('=')
            if value[0] == 'score':
                win_score_cp = int(value[1])
            elif value[0] == 'count':
                win_score_count = int(value[1])
    
    # Get eng file and options from engine json file
    eng_files, eng_opts = [None] * len(names), [None] * len(names)
    for i in range(len(names)):
        try:
            eng_files[i], eng_opts[i] = get_engine_data(engine_json, names[i])
        except TypeError:
            raise Exception(f'engine {i+1} name cannot be found in engine config file!')
        except Exception:
            logging.exception('Exception occurs in getting engine data from engine config file!')
            raise Exception('Exception occurs in getting engine data!')
    
    names = [players[0]['name'], players[1]['name']]
    
    # Init vars for game matches and results
    scores = {names[0]: {'score': 0, 'draws': 0, 'tf': 0},
              names[1]: {'score': 0, 'draws': 0, 'tf': 0}}
    analysis, round_num, num_res = [], 0, 0
    
    time_start = time.perf_counter_ns()
    
    games = get_game_list(opening_file, max_round, randomize_pos)    
    total_games = len(games) * 2 if reverse_start_side else len(games)
    
    print_match_conditions(len(games), reverse_start_side, opening_file,
                           randomize_pos, parallel, base_time_ms, inc_time_ms,
                           win_adj, win_score_cp, win_score_count)
    
    # Run game matches in parallel
    if parallel < 1:
        print(f'Warning, parallel is only {parallel}!, now it set at 1.')
        parallel = 1

    with ProcessPoolExecutor(max_workers=parallel) as executor:
        game_id, round_num = 0, 0
        
        # Submit engine matches as job
        for game in games:            
            round_num += 1
            sub_round, games_per_round_cnt, m, n = 0.0, 0, 0, 1
            
            while True:
                game_id += 1
                sub_round += 0.1
                
                g = Match(
                    game,
                    [eng_files[m], eng_files[n]],
                    [eng_opts[m], eng_opts[n]],
                    [names[m], names[n]],
                    [clock[m], clock[n]],
                    round_num + sub_round if reverse_start_side else round_num,
                    total_games, game_id,
                    win_adj, win_score_cp, win_score_count)
                
                job = executor.submit(g.start_match)
                analysis.append(job)
                games_per_round_cnt += 1
                
                if not reverse_start_side:
                    break
                
                if games_per_round_cnt >= max_games_per_round:
                    break
                
                m, n = n, m  # Reverse the side
            
        # Process every game results
        for future in concurrent.futures.as_completed(analysis):
            try:
                game_output = future.result()[0]
                game_num = future.result()[1]
                round_number = future.result()[2]
                game_elapse = future.result()[3]  # nanoseconds
                
                num_res += 1
                
                wp = game_output.headers['White']
                bp = game_output.headers['Black']
                res = game_output.headers['Result']
                try:
                    termi = game_output.headers['Termination']
                except KeyError:
                    termi = 'normal'
                except Exception:
                    logging.exception('Error in getting termination header value!')
                    termi = 'unknown'
                
                # Save games to a file
                print(game_output, file=open(outpgn, 'a'), end='\n\n')
                
                scores = update_score(game_output, scores)
                
                logging.info(f'Done, game: {game_num}, round: {round_number}, ({wp} vs {bp}): {res} ({termi})')
                print(f'Done, game: {game_num}, round: {round_number}, elapse: {get_time_h_mm_ss_ms(game_elapse)}')
                print(f'players: {wp} vs {bp}')
                print(f'result: {res} ({termi})')
                
                print_result_table(scores, num_res)

            except Exception:
                logging.exception('Exception in completed analysis.')
    
    elapse = time.perf_counter_ns() - time_start  # time delta in nanoseconds
    logging.info(f'Match: done, elapse: {get_time_h_mm_ss_ms(elapse)}')
    print(f'Match: done, elapse: {get_time_h_mm_ss_ms(elapse)}')
    
    logging.shutdown()
    

if __name__ == '__main__':
    main()
    