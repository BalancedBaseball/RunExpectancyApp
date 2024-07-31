import pandas as pd

def runner_destinations_to_digits(checkbox_runner: tuple):
    lst_destinations = ['0', '0', '0']
    if "1bstay" in checkbox_runner:
        lst_destinations[0] = '1'
    if "1bto2b" in checkbox_runner:
        lst_destinations[0] = '2'
    if "1bstay" in checkbox_runner and "1bto2b" in checkbox_runner:
        return '', "The runner on first base cannot both stay and attempt to advance to second base!"
    if "2bstay" in checkbox_runner:
        lst_destinations[1] = '2'
    if "1bto2b" in checkbox_runner and "2bstay" in checkbox_runner:
        return '', "The runner on first base cannot attempt to advance to second base if the runner on second base is staying!"
    if "2bto3b" in checkbox_runner:
        lst_destinations[1] = '3'
    if "2bstay" in checkbox_runner and "2bto3b" in checkbox_runner:
        return '', "The runner on second base cannot both stay and attempt to advance to third base!"
    if "3bstay" in checkbox_runner:
        lst_destinations[2] = '3'
    if "2bto3b" in checkbox_runner and "3bstay" in checkbox_runner:
        return '', "The runner on second base cannot attempt to advance to third base if the runner on third base is staying!"
    if "3bscore" in checkbox_runner:
        lst_destinations[2] = '4'
    if "3bstay" in checkbox_runner and "3bscore" in checkbox_runner:
        return '', "The runner on third base cannot both stay and attempt to score!"
    str_destinations = ''.join(lst_destinations)
    return str_destinations, ""

def bases_to_bases_occupied(bases: tuple):
    bases_occupied_lst = ['0', '0', '0']
    if '1b' in bases:
        bases_occupied_lst[0] = '1'
    if '2b' in bases:
        bases_occupied_lst[1] = '1'
    if '3b' in bases:
        bases_occupied_lst[2] = '1'
    bases_occupied = ''.join(bases_occupied_lst)
    return bases_occupied

def check_bases_occupied_and_runner_destinations(bases_occupied, runner_destinations):
    for i in range(3):
        if bases_occupied[i] != '0' and runner_destinations[i] == '0':
            return False
        if bases_occupied[i] == '0' and runner_destinations[i] != '0':
            return False
    return True

def all_runners_stay(runner_destinations):
    for i in range(3):
        if int(runner_destinations[i]) > i + 1:
            return False
    return True

def runner_destinations_to_bases_occupied(runner_destinations: str):
    new_runner_destinations_lst = ['0', '0', '0', '0']
    score = 0
    runner_destinations_lst = list(runner_destinations)
    for runner in runner_destinations_lst:
        if runner != '0' and int(runner) < 4:
            new_runner_destinations_lst[int(runner)] = '1'
        if int(runner) >= 4:
            score += 1
    new_bases_occupied = ''.join(new_runner_destinations_lst)
    return (new_bases_occupied, score)

def lead_moving_runner_and_destination(bases_occupied: str, runner_destinations: str):
    # Example: bases occupied are 0101, runner destinations are 0203
    # This is just the runner on first stealing 2nd
    # and the runner on 3rd is staying put
    bases_occupied_lst = list(bases_occupied)
    runner_destinations_lst = list(runner_destinations)
    for runner in range(1, 5):
        if bases_occupied_lst[4-runner] == '1':
            if int(runner_destinations_lst[-runner]) > 4-runner:
                lead_runner_index = 4 - runner
                lead_runner_destination = runner_destinations_lst[lead_runner_index]
                return (lead_runner_index, lead_runner_destination)
    return (0, '0')

def all_runners_advance_one_base(runner_destinations: str):
    # '0200'
    runner_destinations_lst = list(runner_destinations)
    for runner in range(0, 4):
        destination = runner_destinations_lst[runner]
        if destination != '0':
            new_destination = int(destination) + 1
            runner_destinations_lst[runner] = str(new_destination)
    runner_destinations_new = ''.join(runner_destinations_lst)
    return runner_destinations_new

def evaluate_play_RE(play: str, runner_destinations: str, year: int,
                 gametypes: str, bases_occupied: str, outs: str,
                 bunt_hit: bool, failed_bunt: bool, one_base_error: bool #, two_base_error: bool
                 ):
    
    # Read in appropriate RE24 table
    df = pd.read_csv(f'RE24_{year}_{gametypes}.csv').set_index('Bases')
    
    # For now, the batter is not assumed to be a runner until a bunt for hit or error happens
    runner_destinations_lst = list(runner_destinations)
    runner_destinations_lst.insert(0, '0')
    runner_destinations = ''.join(runner_destinations_lst)
    bases_occupied_lst = list(bases_occupied)
    bases_occupied_lst.insert(0, '0')
    bases_occupied = ''.join(bases_occupied_lst)
    
    # Establish starting run expectancy
    starting_RE = df.loc[int(bases_occupied[1:4]), outs]
    starting_runs_scored = 0
    
    # Translating the runner destinations to desired format
    desired_bases_occupied, desired_runs_scored = runner_destinations_to_bases_occupied(runner_destinations)
    
    # Compute desired run expectancy        
    if play == 'steal':
        bunt_hit = False
        desired_outs = outs
        desired_RE = df.loc[int(desired_bases_occupied[1:4]), desired_outs]
    if play == 'bunt':
        desired_outs = int(outs) + 1
        desired_outs = str(desired_outs)
        if int(desired_outs) >= 3:
            desired_RE = 0
            desired_runs_scored = 0
        else:
            desired_RE = df.loc[int(desired_bases_occupied[1:4]), desired_outs]
    
    # Compute bunt for hit run expectancy
    if play == 'bunt' and bunt_hit:
        runner_destinations_lst = list(runner_destinations)
        runner_destinations_lst[0] = '1'
        bunt_for_hit_runner_destinations = ''.join(runner_destinations_lst)
        bunt_for_hit_bases_occupied, bunt_for_hit_runs_scored = runner_destinations_to_bases_occupied(bunt_for_hit_runner_destinations)
        bunt_for_hit_outs = outs
        bunt_for_hit_RE = df.loc[int(bunt_for_hit_bases_occupied[1:4]), bunt_for_hit_outs]
    else:
        bunt_for_hit_RE = 0
        bunt_for_hit_runs_scored = 0
        
    # Compute failed bunt run expectancy
    if play == 'bunt' and failed_bunt:
        failed_bunt_bases_occupied = bases_occupied
        failed_bunt_runs_scored = 0
        failed_bunt_outs = str(int(outs) + 1)
        if int(failed_bunt_outs) >= 3:
            failed_bunt_RE = 0
            failed_bunt_runs_scored = 0
        else:
            failed_bunt_RE = df.loc[int(failed_bunt_bases_occupied[1:4]), failed_bunt_outs]
    else:
        failed_bunt_RE = 0
        failed_bunt_runs_scored = 0
        
    # Compute risked run expectancy
    if play == 'bunt':
        risked_runner_destinations_lst = list(runner_destinations)
        risked_runner_destinations_lst[0] = '1'
        risked_runner_destinations = ''.join(risked_runner_destinations_lst)
        risked_bases_occupied_lst = list(bases_occupied)
        risked_bases_occupied_lst[0] = '1'
        risked_bases_occupied = ''.join(risked_bases_occupied_lst)
    else:
        risked_runner_destinations = runner_destinations
        risked_bases_occupied = bases_occupied
    lead_runner_index, lead_runner_destination = lead_moving_runner_and_destination(risked_bases_occupied, risked_runner_destinations)
    risked_runner_destinations_lst = list(risked_runner_destinations)
    risked_runner_destinations_lst[lead_runner_index] = '0'
    risked_runner_destinations = ''.join(risked_runner_destinations_lst)
    risked_bases_occupied, risked_runs_scored = runner_destinations_to_bases_occupied(risked_runner_destinations)
    risked_outs = str(int(outs) + 1)
    if int(risked_outs) >= 3:
        risked_RE = 0
        risked_runs_scored = 0
    else:
        risked_RE = df.loc[int(risked_bases_occupied[1:4]), risked_outs]
        
    # Compute one-base error expectancy
    if one_base_error:
        if play == 'bunt':
            one_base_error_runner_destinations_lst = list(runner_destinations)
            one_base_error_runner_destinations_lst[0] = '1'
            one_base_error_runner_destinations = ''.join(one_base_error_runner_destinations_lst)
        if play == 'steal':
            one_base_error_runner_destinations = runner_destinations
        one_base_error_runner_destinations = all_runners_advance_one_base(one_base_error_runner_destinations)
        one_base_error_bases_occupied, one_base_error_runs_scored = runner_destinations_to_bases_occupied(one_base_error_runner_destinations)
        one_base_error_outs = outs
        one_base_error_RE = df.loc[int(one_base_error_bases_occupied[1:4]), one_base_error_outs]
    else:
        one_base_error_RE = 0
        one_base_error_runs_scored = 0
        
    return (starting_RE, starting_runs_scored,
            desired_RE, desired_runs_scored,
            risked_RE, risked_runs_scored,
            bunt_for_hit_RE, bunt_for_hit_runs_scored,
            failed_bunt_RE, failed_bunt_runs_scored,
            one_base_error_RE, one_base_error_runs_scored)

def make_decision_RE_and_explain(play: str, REandRuns: tuple, bunt_probability: int, steal_probability: int,
                                bunt_for_hit_probability: int, failed_bunt_probability: int,
                                 one_base_error_probability: int):
    
    starting_RE, starting_runs_scored, desired_RE, desired_runs_scored, risked_RE, risked_runs_scored, bunt_for_hit_RE, bunt_for_hit_runs_scored, failed_bunt_RE, failed_bunt_runs_scored, one_base_error_RE, one_base_error_runs_scored = REandRuns
    starting_effective_RE = starting_RE + starting_runs_scored
    desired_effective_RE = desired_RE + desired_runs_scored
    risked_effective_RE = risked_RE + risked_runs_scored
    bunt_for_hit_effective_RE = bunt_for_hit_RE + bunt_for_hit_runs_scored
    failed_bunt_effective_RE = failed_bunt_RE + failed_bunt_runs_scored
    one_base_error_effective_RE = one_base_error_RE + one_base_error_runs_scored
    
    if play == 'steal':
        alt_effective_RE = (desired_effective_RE * steal_probability * 0.01) + (one_base_error_effective_RE * one_base_error_probability * 0.01) + (risked_effective_RE * (1 - ((one_base_error_probability * 0.01) + (steal_probability * 0.01))))
        
        if starting_effective_RE > alt_effective_RE:
            decision = 'Stay'
            explanation1 = f'Given the bases occupied and outs recorded combination you have entered, it makes sense for the runner(s) to stay where they are. This bases-outs combination already has a starting run expectancy of {round(starting_RE, 2)}. Calling for a steal play could get you into a better position to score with a run expectancy of {round(desired_RE, 2)}'
            if desired_runs_scored > 0:
                explanation1 = explanation1 + (f' with {desired_runs_scored} run(s) scored. ')
            else:
                explanation1 = explanation1 + '. '
            explanation2 = f'If the catcher is able to throw out the lead runner, you risk reducing your run expectancy down to {round(risked_RE, 2)}'
            if risked_RE == 0:
                explanation2 = explanation2 + ' because 3 outs would end the inning. '
            else:
                explanation2 = explanation2 + '. '
            if one_base_error_probability > 0:
                explanation2 = explanation2 + f'In a scenario where the defense surrenders a one-base error, you could potentially increase run expectancy to {round(one_base_error_RE, 2)}'
                if one_base_error_runs_scored > 0:
                    explanation2 = explanation2 + f' with {one_base_error_runs_scored} run(s) scored. '
                else:
                    explanation2 = explanation2 + '. '
            explanation3 = f'Ultimately, even with a successful steal probability of {steal_probability}% and a one-base error probability of {one_base_error_probability}%, the aggregate run expectancy of stealing given these odds is {round(alt_effective_RE, 2)} compared to a starting run expectancy of {round(starting_RE, 2)}, so it would not be worth it to try to steal in this scenario.'
            explanation = [explanation1, explanation2, explanation3]
            explanation = ''.join(explanation)
            
        if starting_effective_RE < alt_effective_RE:
            decision = 'Go'
            explanation1 = f'Given the bases occupied and outs recorded combination you have entered, it makes sense for the runner(s) to go for a steal. This bases-outs combination has a starting run expectancy of {round(starting_RE, 2)}. Calling for a steal play could get you into a better position to score with a run expectancy of {round(desired_RE, 2)}'
            if desired_runs_scored > 0:
                explanation1 = explanation1 + (f' with {desired_runs_scored} run(s) scored. ')
            else:
                explanation1 = explanation1 + '. '
            explanation2 = f'If the catcher is able to throw out the lead runner, you risk reducing your run expectancy down to {round(risked_RE, 2)}' 
            if risked_RE == 0:
                explanation2 = explanation2 + ' because 3 outs would end the inning. '
            else:
                explanation2 = explanation2 + '. '
            if one_base_error_probability > 0:
                explanation2 = explanation2 + f'In a scenario where the defense surrenders a one-base error, you could potentially increase run expectancy to {round(one_base_error_RE, 2)}'
                if one_base_error_runs_scored > 0:
                    explanation2 = explanation2 + f' with {one_base_error_runs_scored} run(s) scored. '
                else:
                    explanation2 = explanation2 + '. '
            explanation3 = f'Ultimately, with a successful steal probability of {steal_probability}% and a one-base error probability of {one_base_error_probability}%, the aggregate run expectancy of stealing given these odds is {round(alt_effective_RE, 2)} compared to a starting run expectancy of {round(starting_RE, 2)}, so it would be worth it to try to steal in this scenario.'
            explanation = [explanation1, explanation2, explanation3]
            explanation = ''.join(explanation)
            
    if play == 'bunt':
        alt_effective_RE = (desired_effective_RE * bunt_probability * 0.01) + (one_base_error_effective_RE * one_base_error_probability * 0.01) + (bunt_for_hit_effective_RE * bunt_for_hit_probability * 0.01) + (failed_bunt_effective_RE * failed_bunt_probability * 0.01) + (risked_effective_RE * (1 - ((one_base_error_probability * 0.01) + (bunt_probability * 0.01) + (bunt_for_hit_probability * 0.01) + (failed_bunt_probability * 0.01))))
        if starting_effective_RE > alt_effective_RE:
            decision = 'Swing Away'
            explanation1 = f'Given the bases occupied and outs recorded combination you have entered, it makes sense for the batter to swing away. This bases-outs combination already has a starting run expectancy of {round(starting_RE, 2)}. Calling for a bunt play'
            if desired_effective_RE > starting_effective_RE:
                explanation1 = explanation1 + (f', only if successful, would increase run expectancy to {round(desired_RE, 2)}')
            else:
                explanation1 = explanation1 + (f', even if successful, would still lower run expectancy to {round(desired_RE, 2)}')
                if desired_RE == 0:
                    explanation1 = explanation1 + ' because 3 outs would end the inning. '
                elif desired_runs_scored > 0:
                    explanation1 = explanation1 + (f' with {desired_runs_scored} run(s) scored. ')
                else:
                    explanation1 = explanation1 + ('. ')
            explanation2 = f'If the fielders are able to throw out the lead runner, you risk reducing your run expectancy down to {round(risked_RE, 2)}.'
            if risked_RE == 0:
                explanation2 = explanation2 + ' because 3 outs would end the inning. '
            else:
                explanation2 = explanation2 + '. '
            if one_base_error_probability > 0:
                explanation2 = explanation2 + f' In a scenario where the defense surrenders a one-base error, you could potentially increase run expectancy to {round(one_base_error_RE, 2)}'
                if one_base_error_runs_scored > 0:
                    explanation2 = explanation2 + f' with {one_base_error_runs_scored} run(s) scored. '
                else:
                    explanation2 = explanation2 + '. '
            if bunt_for_hit_probability > 0:
                explanation3 = f'There is also the {bunt_for_hit_probability}% chance that the bunt goes for a hit, and that would increase run expectancy to {round(bunt_for_hit_RE, 2)}'
                if bunt_for_hit_runs_scored > 0:
                    explanation3 = explanation3 + f' with {bunt_for_hit_runs_scored} run(s) scored. '
                else:
                    explanation3 = explanation3 + '. '
            else:
                explanation3 = ''
            explanation4 = f'If the batter fails to execute the bunt and no runners can advance, the run expectancy drops to {round(failed_bunt_RE, 2)}'
            if failed_bunt_RE == 0:
                explanation4 = explanation4 + ' because 3 outs would end the inning. '
            else:
                explanation4 = explanation4 + '. '
            explanation5 = f'Ultimately, even with a successful bunt probability of {bunt_probability}%, a probability of bunting for a hit of {bunt_for_hit_probability}%, a failed bunt probability of {failed_bunt_probability}%, and a one-base error probability of {one_base_error_probability}%, the aggregate run expectancy of attempting to bunt given these odds is {round(alt_effective_RE, 2)} compared to a starting run expectancy of {round(starting_RE, 2)}, so it would not be worth it to try to bunt in this scenario.'
            explanation = [explanation1, explanation2, explanation3, explanation4, explanation5]
            explanation = ''.join(explanation)
            
        if starting_effective_RE < alt_effective_RE:
            decision = 'Bunt'
            explanation1 = f'Given the bases occupied and outs recorded combination you have entered, it makes sense for the batter to attempt a bunt. This bases-outs combination already has a starting run expectancy of {round(starting_RE, 2)}. Calling for a bunt play'
            if desired_effective_RE > starting_effective_RE:
                explanation1 = explanation1 + (f', if successful, would increase run expectancy to {round(desired_RE, 2)}')
            else:
                explanation1 = explanation1 + (f', even if successful, would still lower run expectancy to {round(desired_RE, 2)}')
                if desired_RE == 0:
                    explanation1 = explanation1 + ' because 3 outs would end the inning. '
                elif desired_runs_scored > 0:
                    explanation1 = explanation1 + (f' with {desired_runs_scored} run(s) scored. ')
                else:
                    explanation1 = explanation1 + ('. ')
            explanation2 = f'If the fielders are able to throw out the lead runner, you risk reducing your run expectancy down to {round(risked_RE, 2)}'
            if risked_RE == 0:
                explanation2 = explanation2 + ' because 3 outs would end the inning. '
            else:
                explanation2 = explanation2 + '. '
            if one_base_error_probability > 0:
                explanation2 = explanation2 + f'In a scenario where the defense surrenders a one-base error, you could potentially increase run expectancy to {round(one_base_error_RE, 2)}'
                if one_base_error_runs_scored > 0:
                    explanation2 = explanation2 + f' with {one_base_error_runs_scored} run(s) scored. '
                else:
                    explanation2 = explanation2 + '. '
            if bunt_for_hit_probability > 0:
                explanation3 = f'There is also the {bunt_for_hit_probability}% chance that the bunt goes for a hit, and that would increase run expectancy to {round(bunt_for_hit_RE, 2)}'
                if bunt_for_hit_runs_scored > 0:
                    explanation3 = explanation3 + f' with {bunt_for_hit_runs_scored} run(s) scored. '
                else:
                    explanation3 = explanation3 + '. '
            else:
                explanation3 = ''
            explanation4 = f'If the batter fails to execute the bunt and no runners can advance, the run expectancy drops to {round(failed_bunt_RE, 2)}'
            if failed_bunt_RE == 0:
                explanation4 = explanation4 + ' because 3 outs would end the inning. '
            else:
                explanation4 = explanation4 + '. '
            explanation5 = f'Ultimately, even with a successful bunt probability of {bunt_probability}%, a probability of bunting for a hit of {bunt_for_hit_probability}%, a failed bunt probability of {failed_bunt_probability}%, and a one-base error probability of {one_base_error_probability}%, and a one-base error probability of {one_base_error_probability}%, the aggregate run expectancy of attempting to bunt given these odds is {round(alt_effective_RE, 2)} compared to a starting run expectancy of {round(starting_RE, 2)}, so it would be worth it to try to bunt in this scenario.'
            explanation = [explanation1, explanation2, explanation3, explanation4]
            explanation = ''.join(explanation)
    return (decision, starting_effective_RE, alt_effective_RE, explanation)

def evaluate_play_RP(play: str, runner_destinations: str, year: int,
                 gametypes: str, bases_occupied: str, outs: str,
                 bunt_hit: bool, failed_bunt: bool, one_base_error: bool #, two_base_error: bool
                 ):
    
    # Read in appropriate RE24 table
    df = pd.read_csv(f'RP24_{year}_{gametypes}.csv').set_index('Bases')
    
    # For now, the batter is not assumed to be a runner until a bunt for hit or error happens
    runner_destinations_lst = list(runner_destinations)
    runner_destinations_lst.insert(0, '0')
    runner_destinations = ''.join(runner_destinations_lst)
    bases_occupied_lst = list(bases_occupied)
    bases_occupied_lst.insert(0, '0')
    bases_occupied = ''.join(bases_occupied_lst)
    
    # Establish starting run probability
    starting_RP = df.loc[int(bases_occupied[1:4]), outs]
    starting_runs_scored = 0
    
    # Translating the runner destinations to desired format
    desired_bases_occupied, desired_runs_scored = runner_destinations_to_bases_occupied(runner_destinations)
    
    # Compute desired run probability        
    if play == 'steal':
        bunt_hit = False
        desired_outs = outs
        desired_RP = df.loc[int(desired_bases_occupied[1:4]), desired_outs]
    if play == 'bunt':
        desired_outs = int(outs) + 1
        desired_outs = str(desired_outs)
        if int(desired_outs) >= 3:
            desired_RP = 0
            desired_runs_scored = 0
        else:
            desired_RP = df.loc[int(desired_bases_occupied[1:4]), desired_outs]
    
    # Compute bunt for hit run probability
    if play == 'bunt' and bunt_hit:
        runner_destinations_lst = list(runner_destinations)
        runner_destinations_lst[0] = '1'
        bunt_for_hit_runner_destinations = ''.join(runner_destinations_lst)
        bunt_for_hit_bases_occupied, bunt_for_hit_runs_scored = runner_destinations_to_bases_occupied(bunt_for_hit_runner_destinations)
        bunt_for_hit_outs = outs
        bunt_for_hit_RP = df.loc[int(bunt_for_hit_bases_occupied[1:4]), bunt_for_hit_outs]
    else:
        bunt_for_hit_RP = 0
        bunt_for_hit_runs_scored = 0
        
    # Compute failed bunt run probability
    if play == 'bunt' and failed_bunt:
        failed_bunt_bases_occupied = bases_occupied
        failed_bunt_runs_scored = 0
        failed_bunt_outs = str(int(outs) + 1)
        if int(failed_bunt_outs) >= 3:
            failed_bunt_RP = 0
            failed_bunt_runs_scored = 0
        else:
            failed_bunt_RP = df.loc[int(failed_bunt_bases_occupied[1:4]), failed_bunt_outs]
    else:
        failed_bunt_RP = 0
        failed_bunt_runs_scored = 0
        
    # Compute risked run probability
    if play == 'bunt':
        risked_runner_destinations_lst = list(runner_destinations)
        risked_runner_destinations_lst[0] = '1'
        risked_runner_destinations = ''.join(risked_runner_destinations_lst)
        risked_bases_occupied_lst = list(bases_occupied)
        risked_bases_occupied_lst[0] = '1'
        risked_bases_occupied = ''.join(risked_bases_occupied_lst)
    else:
        risked_runner_destinations = runner_destinations
        risked_bases_occupied = bases_occupied
    lead_runner_index, lead_runner_destination = lead_moving_runner_and_destination(risked_bases_occupied, risked_runner_destinations)
    risked_runner_destinations_lst = list(risked_runner_destinations)
    risked_runner_destinations_lst[lead_runner_index] = '0'
    risked_runner_destinations = ''.join(risked_runner_destinations_lst)
    risked_bases_occupied, risked_runs_scored = runner_destinations_to_bases_occupied(risked_runner_destinations)
    risked_outs = str(int(outs) + 1)
    if int(risked_outs) >= 3:
        risked_RP = 0
        risked_runs_scored = 0
    else:
        risked_RP = df.loc[int(risked_bases_occupied[1:4]), risked_outs]
        
    # Compute one-base error probability
    if one_base_error:
        if play == 'bunt':
            one_base_error_runner_destinations_lst = list(runner_destinations)
            one_base_error_runner_destinations_lst[0] = '1'
            one_base_error_runner_destinations = ''.join(one_base_error_runner_destinations_lst)
        if play == 'steal':
            one_base_error_runner_destinations = runner_destinations
        one_base_error_runner_destinations = all_runners_advance_one_base(one_base_error_runner_destinations)
        one_base_error_bases_occupied, one_base_error_runs_scored = runner_destinations_to_bases_occupied(one_base_error_runner_destinations)
        one_base_error_outs = outs
        one_base_error_RP = df.loc[int(one_base_error_bases_occupied[1:4]), one_base_error_outs]
    else:
        one_base_error_RP = 0
        one_base_error_runs_scored = 0
        
    return (starting_RP, starting_runs_scored,
            desired_RP, desired_runs_scored,
            risked_RP, risked_runs_scored,
            bunt_for_hit_RP, bunt_for_hit_runs_scored,
            failed_bunt_RP, failed_bunt_runs_scored,
            one_base_error_RP, one_base_error_runs_scored)

def make_decision_RP_and_explain(play: str, RPandRuns: tuple, bunt_probability: int, steal_probability: int,
                                bunt_for_hit_probability: int, failed_bunt_probability: int,
                                 one_base_error_probability: int):
   
    starting_RP, starting_runs_scored, desired_RP, desired_runs_scored, risked_RP, risked_runs_scored, bunt_for_hit_RP, bunt_for_hit_runs_scored, failed_bunt_RP, failed_bunt_runs_scored, one_base_error_RP, one_base_error_runs_scored = RPandRuns
    
    if starting_runs_scored > 0:
        starting_RP = 1
        starting_effective_RP = 1
    else:
        starting_effective_RP = starting_RP + starting_runs_scored
        
    if desired_runs_scored > 0:
        desired_RP = 1
        desired_effective_RP = 1
    else:
        desired_effective_RP = desired_RP + desired_runs_scored
    
    if risked_runs_scored > 0:
        risked_RP = 1
        risked_effective_RP = 1
    else:
        risked_effective_RP = risked_RP + risked_runs_scored
    
    if bunt_for_hit_runs_scored > 0:
        bunt_for_hit_RP = 1
        bunt_for_hit_effective_RP = 1
    else:
        bunt_for_hit_effective_RP = bunt_for_hit_RP + bunt_for_hit_runs_scored

    if failed_bunt_runs_scored > 0:
        failed_bunt_RP = 1
        failed_bunt_effective_RP = 1
    else:
        failed_bunt_effective_RP = failed_bunt_RP + failed_bunt_runs_scored
    
    if one_base_error_runs_scored > 0:
        one_base_error_RP = 1
        one_base_error_effective_RP = 1
    else:
        one_base_error_effective_RP = one_base_error_RP + one_base_error_runs_scored
   
    if play == 'steal':
        alt_effective_RP = (desired_effective_RP * steal_probability * 0.01) + (one_base_error_effective_RP * one_base_error_probability * 0.01) + (risked_effective_RP * (1 - ((one_base_error_probability * 0.01) + (steal_probability * 0.01))))
       
        if starting_effective_RP > alt_effective_RP:
            decision = 'Stay'
            explanation1 = f'Given the bases occupied and outs recorded combination you have entered, it makes sense for the runner(s) to stay where they are. This bases-outs combination already has a starting run probability of {round(starting_RP * 100, 2)}%. Calling for a steal play'
            if desired_runs_scored > 0:
                explanation1 = explanation1 + (', if successful, scores a run and has run probability of 100%.')
            else:
                explanation1 = explanation1 + f' could get you into a better position to score with a run probability of {round(desired_RP * 100, 2)}%. '
            explanation2 = f'If the catcher is able to throw out the lead runner, you risk reducing your run probability down to {round(risked_RP * 100, 2)}%'
            if risked_RP == 0:
                explanation2 = explanation2 + ' because 3 outs would end the inning. '
            else:
                explanation2 = explanation2 + '. '
            if one_base_error_probability > 0:
                explanation2 = explanation2 + 'In a scenario where the defense surrenders a one-base error, you '
                if one_base_error_runs_scored > 0:
                    explanation2 = explanation2 + ' score one or more runs and have run probability of 100%. '
                else:
                    explanation2 = explanation2 + f'could potentially increase run probability to {round(one_base_error_RP * 100, 2)}%. '
            explanation3 = f'Ultimately, even with a successful steal probability of {steal_probability}% and a one-base error probability of {one_base_error_probability}%, the aggregate run probability of stealing given these odds is {round(alt_effective_RP * 100, 2)}% compared to a starting run probability of {round(starting_RP * 100, 2)}%, so it would not be worth it to try to steal in this scenario.'
            explanation = [explanation1, explanation2, explanation3]
            explanation = ''.join(explanation)
           
        if starting_effective_RP < alt_effective_RP:
            decision = 'Go'
            explanation1 = f'Given the bases occupied and outs recorded combination you have entered, it makes sense for the runner(s) to go for a steal. This bases-outs combination has a starting run probability of {round(starting_RP * 100, 2)}%. Calling for a steal play'
            if desired_runs_scored > 0:
                explanation1 = explanation1 + (', if successful, scores a run and has run probability of 100%.')
            else:
                explanation1 = explanation1 + f' could get you into a better position to score with a run probability of {round(desired_RP * 100, 2)}%. '
            explanation2 = f'If the catcher is able to throw out the lead runner, you risk reducing your run probability down to {round(risked_RP * 100, 2)}%'
            if risked_RP == 0:
                explanation2 = explanation2 + ' because 3 outs would end the inning. '
            else:
                explanation2 = explanation2 + '. '
            if one_base_error_probability > 0:
                explanation2 = explanation2 + 'In a scenario where the defense surrenders a one-base error, you '
                if one_base_error_runs_scored > 0:
                    explanation2 = explanation2 + ' score one or more runs and have run probability of 100%. '
                else:
                    explanation2 = explanation2 + f'could potentially increase run probability to {round(one_base_error_RP * 100, 2)}%. '
            explanation3 = f'Ultimately, with a successful steal probability of {steal_probability}% and a one-base error probability of {one_base_error_probability}%, the aggregate run probability of stealing given these odds is {round(alt_effective_RP * 100, 2)}% compared to a starting run probability of {round(starting_RP * 100, 2)}%, so it would be worth it to try to steal in this scenario.'
            explanation = [explanation1, explanation2, explanation3]
            explanation = ''.join(explanation)
           
    if play == 'bunt':
        alt_effective_RP = (desired_effective_RP * bunt_probability * 0.01) + (one_base_error_effective_RP * one_base_error_probability * 0.01) + (bunt_for_hit_effective_RP * bunt_for_hit_probability * 0.01) + (failed_bunt_effective_RP * failed_bunt_probability * 0.01) + (risked_effective_RP * (1 - ((one_base_error_probability * 0.01) + (bunt_probability * 0.01) + (bunt_for_hit_probability * 0.01) + (failed_bunt_probability * 0.01))))
        if starting_effective_RP > alt_effective_RP:
            decision = 'Swing Away'
            explanation1 = f'Given the bases occupied and outs recorded combination you have entered, it makes sense for the batter to swing away. This bases-outs combination already has a starting run probability of {round(starting_RP * 100, 2)}%. Calling for a bunt play'
            if desired_runs_scored > 0:
                explanation1 = explanation1 + (', if successful, scores a run and has run probability of 100%. ')
            else:
                if desired_effective_RP > starting_effective_RP:
                    explanation1 = explanation1 + (f', only if successful, would increase run probability to {round(desired_RP * 100, 2)}%')
                else:
                    explanation1 = explanation1 + (f', even if successful, would still lower run probability to {round(desired_RP * 100, 2)}%')
                if desired_RP == 0:
                    explanation1 = explanation1 + ' because 3 outs would end the inning. '
                else:
                    explanation1 = explanation1 + ('. ')
            
            explanation2 = f'If the fielders are able to throw out the lead runner, you risk reducing your run probability down to {round(risked_RP * 100, 2)}%'
            if risked_RP == 0:
                explanation2 = explanation2 + ' because 3 outs would end the inning. '
            else:
                explanation2 = explanation2 + '. '
            if one_base_error_probability > 0:
                explanation2 = explanation2 + 'In a scenario where the defense surrenders a one-base error, you '
                if one_base_error_runs_scored > 0:
                    explanation2 = explanation2 + ' score one or more runs with run probability of 100%. '
                else:
                    explanation2 = explanation2 + f'could potentially increase run probability to {round(one_base_error_RP * 100, 2)}%. '
            
            if bunt_for_hit_probability > 0:
                explanation3 = f'There is also the {bunt_for_hit_probability}% chance that the bunt goes for a hit, and that would'
                if bunt_for_hit_runs_scored > 0:
                    explanation3 = explanation3 + ' score one or more runs with run probability of 100%. '
                else:
                    explanation3 = explanation3 + f' increase run probability to {round(bunt_for_hit_RP * 100, 2)}%. '
            else:
                explanation3 = ''
            
            if failed_bunt_probability > 0:
                explanation4 = f'If the batter fails to execute the bunt and no runners can advance, the run probability drops to {round(failed_bunt_RP * 100, 2)}%'
                if failed_bunt_RP == 0:
                    explanation4 = explanation4 + ' because 3 outs would end the inning. '
                else:
                    explanation4 = explanation4 + '. '
            else:
                explanation4 = ''
            
            explanation5 = f'Ultimately, even with a successful bunt probability of {bunt_probability}%, a probability of bunting for a hit of {bunt_for_hit_probability}%, a failed bunt probability of {failed_bunt_probability}%, and a one-base error probability of {one_base_error_probability}%, the aggregate run probability of attempting to bunt given these odds is {round(alt_effective_RP * 100, 2)}% compared to a starting run probability of {round(starting_RP * 100, 2)}%, so it would not be worth it to try to bunt in this scenario.'
            
            explanation = [explanation1, explanation2, explanation3, explanation4, explanation5]
            explanation = ''.join(explanation)
           
        if starting_effective_RP < alt_effective_RP:
            decision = 'Bunt'
            explanation1 = f'Given the bases occupied and outs recorded combination you have entered, it makes sense for the batter to attempt the bunt. This bases-outs combination already has a starting run probability of {round(starting_RP * 100, 2)}%. Calling for a bunt play'
            if desired_runs_scored > 0:
                explanation1 = explanation1 + (', if successful, scores a run and has run probability of 100%. ')
            else:
                if desired_effective_RP > starting_effective_RP:
                    explanation1 = explanation1 + (f', only if successful, would increase run probability to {round(desired_RP * 100, 2)}%')
                else:
                    explanation1 = explanation1 + (f', even if successful, would still lower run probability to {round(desired_RP * 100, 2)}%')
                if desired_RP == 0:
                    explanation1 = explanation1 + ' because 3 outs would end the inning. '
                else:
                    explanation1 = explanation1 + ('. ')
                    
            explanation2 = f'If the fielders are able to throw out the lead runner, you risk reducing your run probability down to {round(risked_RP * 100, 2)}%'
            if risked_RP == 0:
                explanation2 = explanation2 + ' because 3 outs would end the inning. '
            else:
                explanation2 = explanation2 + '. '
            if one_base_error_probability > 0:
                explanation2 = explanation2 + 'In a scenario where the defense surrenders a one-base error, you '
                if one_base_error_runs_scored > 0:
                    explanation2 = explanation2 + ' score one or more runs with run probability of 100%. '
                else:
                    explanation2 = explanation2 + f'could potentially increase run probability to {round(one_base_error_RP * 100, 2)}%. '

            if bunt_for_hit_probability > 0:
                explanation3 = f'There is also the {bunt_for_hit_probability}% chance that the bunt goes for a hit, and that would'
                if bunt_for_hit_runs_scored > 0:
                    explanation3 = explanation3 + ' score one or more runs with run probability of 100%. '
                else:
                    explanation3 = explanation3 + f' increase run probability to {round(bunt_for_hit_RP * 100, 2)}%. '
            else:
                explanation3 = ''
                
            if failed_bunt_probability > 0:
                explanation4 = f'If the batter fails to execute the bunt and no runners can advance, the run probability drops to {round(failed_bunt_RP * 100, 2)}%'
                if failed_bunt_RP == 0:
                    explanation4 = explanation4 + ' because 3 outs would end the inning. '
                else:
                    explanation4 = explanation4 + '. '
            else:
                explanation4 = ''
            
            explanation5 = f'Ultimately, with a successful bunt probability of {bunt_probability}%, a probability of bunting for a hit of {bunt_for_hit_probability}%, a failed bunt probability of {failed_bunt_probability}%, and a one-base error probability of {one_base_error_probability}%, the aggregate run probability of attempting to bunt given these odds is {round(alt_effective_RP * 100, 2)}% compared to a starting run probability of {round(starting_RP * 100, 2)}%, so it would be worth it to try to bunt in this scenario.'
            
            explanation = [explanation1, explanation2, explanation3, explanation4, explanation5]
            explanation = ''.join(explanation)
            
    return (decision, starting_effective_RP * 100, alt_effective_RP * 100, explanation)