def extract_workout_types(workouts):
    workout_types: str = []
    
    for i in range(0, len(workouts)):
        if workouts.loc[i] not in workout_types:
            workout_types.append(workouts.loc[i])
        
    return workout_types

def count_workouts(workouts, types):
    type_and_times_dict = dict()
    
    for workout in types:
        type_and_times_dict.update({workout : 0})
        
    for i in range(0, len(workouts)):
        n_occurence = type_and_times_dict[workouts.loc[i]] 
        n_occurence += 1
        type_and_times_dict.update({workouts.loc[i] : n_occurence})
    return type_and_times_dict


def filter_from_date(workouts, yearfrom):
    for i in range(0, len(workouts)):
        if yearfrom in str(df["date"].values[i]):
            workouts = workouts.loc[i:]
            workouts = workouts.reset_index(drop = True)
            return workouts