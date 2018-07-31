class BattingStyleChoices:
    RIGHT_HAND = 'rhb'
    LEFT_HAND = 'lhb'

    Choices = (
        (RIGHT_HAND, 'Right Hand Bat'),
        (LEFT_HAND, 'Left Hand Bat')
    )


class BowlingStyleChoices:
    RIGHT_ARM_FAST = 'raf'
    RIGHT_ARM_MEDIUM_FAST = 'ramf'
    RIGHT_ARM_OFF_BREAK = 'raob'
    RIGHT_ARM_LEG_BREAK_GOOGLY = 'ralg'
    RIGHT_ARM_ORTHODOX = 'rao'
    LEFT_ARM_FAST = 'laf'
    LEFT_ARM_MEDIUM_FAST = 'lamf'
    LEFT_ARM_ORTHODOX = 'lao'
    LEFT_ARM_CHINAMAN = 'lac'

    Choices = (
        (RIGHT_ARM_FAST, 'Right Arm Fast'),
        (RIGHT_ARM_MEDIUM_FAST, 'Right Arm Medium Fast'),
        (RIGHT_ARM_OFF_BREAK, 'Right Arm OffBreak'),
        (RIGHT_ARM_LEG_BREAK_GOOGLY, 'Right Arm LegBreak Googly'),
        (RIGHT_ARM_ORTHODOX, 'Right Arm Orthodox'),
        (LEFT_ARM_FAST, 'Left Arm Fast'),
        (LEFT_ARM_MEDIUM_FAST, 'Left Arm Medium Fast'),
        (LEFT_ARM_ORTHODOX, 'Left Arm Orthodox'),
        (LEFT_ARM_CHINAMAN, 'Left Arm Chinaman'),
    )


class PlayingRoleChoices:
    BATSMAN = 'bat'
    BOWLER = 'bowl'
    ALLROUNDER = 'all'
    WICKETKEEPER = 'wkt'

    Choices = (
        (BATSMAN, 'Batsman'),
        (BOWLER, 'Bowler'),
        (ALLROUNDER, 'AllRounder'),
        (WICKETKEEPER, 'WicketKeeper'),
    )


class FormatChoices:
    TEST = 'test'
    ODI = 'odi'
    T20I = 't20i'
    FIRSTCLASS = 'firstclass'
    LISTA = 'lista'
    T20S = 't20s'

    Choices = (
        (TEST, 'Test'),
        (ODI, 'ODI'),
        (T20I, 'T20I'),
        (FIRSTCLASS, 'FirstClass'),
        (LISTA, 'ListA'),
        (T20S, 'T20s'),
    )

