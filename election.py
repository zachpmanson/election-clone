#!/usr/bin/python3
# Zach Manson 20200707
# A Python clone of cits1001 project1

from sys import argv


class VotingPaper:
    def __init__(self, s):
        """
        Constructor, s is a possibly empty sequence of integers seperated by
        commas. E.g. "1,22,-13,456", marks is set to [1,22,-13,456]
        """
        self.marks = [] if s == "" else list(map(int, s.split(",")))

    def is_correct_length(self, no_of_candidates):
        return len(self.marks) == no_of_candidates

    def is_legal_total(self, total):
        return total >= sum(self.marks)

    def any_negative_marks(self):
        return any(mark < 0 for mark in self.marks)

    def is_formal(self, no_of_candidates):
        return (
            self.is_correct_length(no_of_candidates)
            and self.is_legal_total(no_of_candidates)
            and not self.any_negative_marks()
        )

    def update_vote_counts(self, candidates):
        for i, candidate in enumerate(candidates):
            candidate.no_of_votes += self.marks[i]

    def highest_vote(self):
        max_value = max(self.marks)
        return [i for i, mark in enumerate(self.marks) if mark == max_value]

    def update_win_counts(self, candidates):
        win_indices = self.highest_vote()
        win_count_increase = 1.0 / len(win_indices)

        for index in win_indices:
            candidates[index].no_of_wins += win_count_increase


class Candidate:
    def __init__(self, name):
        self.name = name
        self.no_of_votes = 0
        self.no_of_wins = 0.0

    def __str__(self):
        return self.name

    def get_standing(self):
        return f"{self.name} got {self.no_of_votes} votes and {self.no_of_wins} wins."


class Election:
    def __init__(self, filename):
        self.candidates = []
        self.papers = []
        with open(filename, "r") as f:
            self.lines = f.read().splitlines()

    def process_file(self):
        split = self.lines.index("")
        self.candidates = [Candidate(line) for line in self.lines[:split]]
        self.papers = [VotingPaper(line) for line in self.lines[split + 1 :]]

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
        return "".join(candidate.get_standing() + "\n" for candidate in self.candidates)

    def get_winner(self):
        max_votes = max(candidate.no_of_votes for candidate in self.candidates)
        candidates_with_max_votes = [
            candidate
            for candidate in self.candidates
            if candidate.no_of_votes == max_votes
        ]

        if len(candidates_with_max_votes) == 1:
            return candidates_with_max_votes[0]

        return max(
            candidates_with_max_votes, key=lambda candidate: candidate.no_of_wins
        )


def main(filename):
    election = Election(filename)
    election.process_file()
    election.conduct_count()
    print(election.get_standings())
    print(f"Winner: {election.get_winner()}")


if __name__ == "__main__":
    for filename in argv[1:]:
        main(filename)
