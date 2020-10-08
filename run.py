from astropy.table import Table
from great_deluge import *
from brute_force import *
from hillclimbing import *
from random import shuffle, seed


if __name__ == '__main__':
    # Get the initial schedule.
    initial_sched_table = Table.read('plantab.fits')
    obs_ids = [row['obs_id'] for row in initial_sched_table]
    obs_starts = [row['i_start']-1 for row in initial_sched_table]
    obs_ends = [row['i_end']-1 for row in initial_sched_table]

    packed_ids = []
    packed_starts = {}
    packed_ends = {}

    current_time = 0
    obs_idx = 0
    gaps = 0

    while obs_idx < len(obs_ids):
        # Iterate over the observations.
        # Check to see if the current position on the timeline is the position of the scheduled observation.
        # If it is, add the observation.
        # If it isn't, add a block.
        # Iterate over the time to make sure that they are packed.
        # If not, enter gaps into holes.
        if current_time < obs_starts[obs_idx]:
            obs_id = f"Gap-{gaps}"
            gaps += 1
            packed_ids.append(obs_id)
            packed_starts[obs_id] = current_time
            end_time = obs_starts[obs_idx]-1 if obs_idx < len(obs_ids) else 172
            packed_ends[obs_id] = end_time

            current_time = end_time + 1

        else:
            obs_id = obs_ids[obs_idx]
            packed_ids.append(obs_id)
            packed_starts[obs_id] = obs_starts[obs_idx]
            packed_ends[obs_id] = obs_ends[obs_idx]
            current_time = obs_ends[obs_idx] + 1
            obs_idx += 1

        if obs_idx > len(obs_ids) or current_time >= 172:
            break

    obstab = Table.read('obstab.fits')

    # Get the scoring function for all 173 positions.
    targtab = Table.read('targtab_metvisha.fits')
    wha = {obs_idx : row['wha'] for row in targtab for obs_idx in obs_ids if row['id'] == obs_idx}

    # Create the observations.
    # sorted(print(packed_ids))
    empty_score = [0] * 172

    observations = [Observation(id,
                                packed_ends[id] - packed_starts[id] + 1,
                                wha.get(id, empty_score))
                    for id in packed_ids]

    # This is to show the possible correction of a bad schedule.
    #shuffle(observations)

    print('\n*** DEFAULT_SCHEDULE ***')
    scheduler = Schedule(observations)
    print([obs.name for obs in scheduler.schedule])
    score_def = scheduler.evaluate()
    print(score_def)

    print('\n*** HILL CLIMBING ***')
    scheduler = hillclimbing(Schedule(observations))
    print([obs.name for obs in scheduler.schedule])
    score_hc = scheduler.evaluate()
    print(score_hc)

    print('\n*** GREAT DELUGE ***')
    scheduler = deluge_solver(Schedule(observations))
    print([obs.name for obs in scheduler.schedule])
    score_gd = scheduler.evaluate()
    print(score_gd)

    print('\n*** BRUTE FORCE ***')
    scheduler = brute_force_search(Schedule(observations))
    print([obs.name for obs in scheduler.schedule])
    score_bf = scheduler.evaluate()
    print(score_bf)

    assert(score_bf >= max(score_def, score_hc, score_gd))
    min_score = min(score_def, score_hc, score_gd, score_bf)
    max_score = max(score_def, score_hc, score_gd, score_bf)
    print(f"Improvement of: {max_score} - {min_score} = {max_score - min_score}")