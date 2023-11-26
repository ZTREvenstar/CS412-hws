from typing import List


def read_sequences(path):
    seqs = {}
    with open(path, 'r') as file:
        for line in file:
            record = line.strip().split(', ')
            if len(record) == 2:
                idx, s = record
                seqs[idx] = s
    return seqs


def preprocess(database):
    """preprocess the input raw string"""
    for k, string in database.items():
        database[k] = string[1:-1]


class SingletonRecord:
    """The data structure to store necessary info for singletons"""
    def __init__(self, char):
        self.char = char
        self.freq = 0
        # following to should have same length, record their occurrence in a certain projected_DB
        self.record_idx = []
        self.record_offset = []  # the index of the first char in that string

    def update(self, line_idx, offset):
        """will be called once first meet that char in a seq"""
        self.freq += 1
        self.record_idx.append(line_idx)
        self.record_offset.append(offset)


def count_singleton(projected_DB: List[str], minsup) -> dict:
    # count occurrence in nums of records for each single char in [a-z].
    # No need to worry about (_"x") patterns.

    # construct 26 SingletonRecord Objs
    singletons = {chr(i): SingletonRecord(chr(i)) for i in range(97, 123)}

    # traverse the database: find all frequent singletons and their occurrence in DB.
    for i, line in enumerate(projected_DB):
        existed = set()
        for offset, c in enumerate(line):
            if c in existed:
                continue
            # first meet a char in that seq
            singletons[c].update(line_idx=i, offset=offset)
            existed.add(c)

    # finally, only keep those frequent singletons to return
    freq_singletons = {c: s_obj for c, s_obj in singletons.items() if s_obj.freq >= minsup}

    return freq_singletons


def dfsProcess(database: List[str], S, minsup, ANS_dict: dict):
    """
    param:
    database: the projected database
    S: the previous expanded string. S + freq_char will be added to ANS.
    ANS_dict: a reference to a global buffer that storing answers
    """
    if not database:
        return

    # mine freq patterns
    freq_singletons = count_singleton(database, minsup)
    if not freq_singletons:  # break the recursion
        return

    # for each frequent pattern in this DB:
    for c, s_obj in freq_singletons.items():
        # 1. register new-discovered frequent patterns to ANS
        ANS_dict[S+c] = s_obj.freq
        # 2. prepare the corresponding projected_DB
        projected_DB = [database[idx][offset+1:] for idx, offset in zip(s_obj.record_idx, s_obj.record_offset)]
        # 3. call next level dfs
        dfsProcess(projected_DB, S+c, minsup, ANS_dict)


def ord_prefixspan(filename, minsup):
    freq_sequences = {}  # default initialization
    Database = read_sequences(filename)
    preprocess(Database)

    # freq_singletons = count_singleton(list(Database.values()), minsup)
    # for obj in freq_singletons.values():
    #     print(obj.__dict__)

    dfsProcess(list(Database.values()), "", minsup, freq_sequences)

    return freq_sequences


# JUST for TESTING
if __name__ == "__main__":
    filename, minsup = './a5_sample_input.txt', 2
    print(ord_prefixspan(filename, minsup))
