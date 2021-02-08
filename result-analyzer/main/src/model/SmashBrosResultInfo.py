from enums.Rank import Rank


class SmashBrosResultInfo:
    def __init__(self, ownFighterName: str, ownRank: Rank, opponentFighterName: str, opponentRank: Rank):
        self.ownFighterName = ownFighterName
        self.ownRank = ownRank
        self.opponentFighterName = opponentFighterName
        self.opponentRank = opponentRank
