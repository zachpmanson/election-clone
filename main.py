if __name__ == "__main__":
    from election import *

    e0 = Election("election0.txt")
    e0.process_file()
    e0.conduct_count()
    e0.get_standings()

    e1 = Election("election1.txt")
    e1.process_file()
    e1.conduct_count()
    e1.get_standings()