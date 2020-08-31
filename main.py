# Testing script for election.py
# runs tests on election0.txt, election1.txt

if __name__ == "__main__":
    from election import *

    print("Election 0")
    e0 = Election("election0.txt")
    e0.process_file()
    e0.conduct_count()
    e0.get_standings()

    print("Election 1")
    e1 = Election("election1.txt")
    e1.process_file()
    e1.conduct_count()
    e1.get_standings()
