# Zach Manson 20200707
# A Python clone of cits1001 project1

class VotingPaper():

    def __init__(self, s):
        '''
        Constructor, s is a possibly empty sequence of integers seperated by 
        commas. E.g. "1,22,-13,456", marks is set to [1,22,-13,456]
        '''
        self.marks = []
        if s != "":
            self.marks = list( map(int, s.split(",")) )

    def is_correct_length(self, no_of_candidates):
        return len(self.marks) == no_of_candidates

    def is_legal_total(self, total):
        mark_sum = 0
        for mark in self.marks:
            mark_sum += mark
        
        return total >= mark_sum

    def any_negative_marks(self):
        for mark in self.marks:
            if mark < 0:
                return True

        return False

    def is_formal(self, no_of_candidates):
        return (self.is_correct_length(no_of_candidates)
                and self.is_legal_total(no_of_candidates)
                and not self.any_negative_marks())
    
    def update_vote_counts(self, candidates):
        for i in range(len(candidates)):
            candidates[i].no_of_votes += self.marks[i]

    def highest_vote(self):
        max_value = sorted(self.marks)[-1]

        indices = [ i for i in range(len(self.marks)) if self.marks[i] == max_value]

        return indices

    def update_win_counts(self, candidates):
        win_indices = self.highest_vote()
        win_count_increase = 1.0/len(win_indices)
        
        for index in win_indices:
            candidates[index].no_of_wins += win_count_increase

class Candidate():
    
    def __init__(self, cname):
        self.name = cname
        self.no_of_votes = 0
        self.no_of_wins = 0.0

    def __repr__(self):
        return self.name

    def get_standing(self):
        standing = f"{self.name} got {self.no_of_votes} votes and {self.no_of_wins} wins."
        return standing

class Election():
    
    def __init__(self, filename):
        self.candidates = []
        self.papers = []
        self.lines = open(filename, 'r').read().split("\n")

    def process_file(self):
        
        still_new_candidates = True

        for line in self.lines:
            if line == "" and still_new_candidates:
                still_new_candidates = False
            elif still_new_candidates:
                self.candidates.append( Candidate(line) )
            elif not still_new_candidates:
                self.papers.append( VotingPaper(line) )
    
    def conduct_count(self):
        informal_vote_total = 0
        for paper in self.papers:
            if paper.is_formal(len(self.candidates)):
                paper.update_vote_counts(self.candidates)
                paper.update_win_counts(self.candidates)
            else:
                informal_vote_total += 1
        return informal_vote_total

    def get_standings(self):
        standings = ""
        for candidate in self.candidates:
            standings += candidate.get_standing() + "\n"
        print(standings)
        return standings

    def get_winner(self):
        candidates_with_max_votes = []
        max_votes_so_far = 0

        for candidate in self.candidates:
            if candidate.no_of_votes > max_votes_so_far:
                candidates_with_max_votes = [candidate]
            elif candidate.no_of_votes == max_votes_so_far:
                candidates_with_max_votes.append(candidate)

        winner = no_of_candidates
        if len(candidates_with_max_votes) > 1:
            max_wins_so_far = 0.0
            for candidate in candidates_with_max_votes:
                if candidate.no_of_wins > max_wins_so_far:
                    winner = candidate
                    max_wins_so_far = candidate.no_of_wins
        elif len(candidates_with_max_votes) == 1:
            winner = candidates_with_max_votes[0]
        
        return winner