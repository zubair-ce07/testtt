class BattingStyleChoices:
    RIGHT_HAND = 'RIGHT_HANDED'
    LEFT_HAND = 'LEFT_HANDED'

    Choices = (
        (RIGHT_HAND, 'Right Hand Bat'),
        (LEFT_HAND, 'Left Hand Bat')
    )


class BowlingStyleChoices:
    RIGHT_ARM_FAST = 'RIGHT_ARM_FAST'
    RIGHT_ARM_MEDIUM_FAST = 'RIGHT_ARM_MEDIUM_FAST'
    RIGHT_ARM_OFF_BREAK = 'RIGHT_ARM_OFF_BREAK'
    RIGHT_ARM_LEG_BREAK_GOOGLY = 'RIGHT_ARM_LEG_BREAK_GOOGLY'
    RIGHT_ARM_ORTHODOX = 'RIGHT_ARM_ORTHODOX'
    LEFT_ARM_FAST = 'LEFT_ARM_FAST'
    LEFT_ARM_MEDIUM_FAST = 'LEFT_ARM_MEDIUM_FAST'
    LEFT_ARM_ORTHODOX = 'LEFT_ARM_ORTHODOX'
    LEFT_ARM_CHINAMAN = 'LEFT_ARM_CHINAMAN'

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
    BATSMAN = 'BATSMAN'
    BOWLER = 'BOWLER'
    ALLROUNDER = 'ALLROUNDER'
    WICKETKEEPER = 'WICKETKEEPER'

    Choices = (
        (BATSMAN, 'Batsman'),
        (BOWLER, 'Bowler'),
        (ALLROUNDER, 'AllRounder'),
        (WICKETKEEPER, 'WicketKeeper'),
    )


class FormatChoices:
    TEST = 'TESTS'
    ODI = 'ODIS'
    T20I = 'T20IS'
    FIRSTCLASS = 'FIRST-CLASS'
    LISTA = 'LIST A'
    T20S = 'T20S'

    Choices = (
        (TEST, 'Test'),
        (ODI, 'ODI'),
        (T20I, 'T20I'),
        (FIRSTCLASS, 'FirstClass'),
        (LISTA, 'ListA'),
        (T20S, 'T20s'),
    )


class TeamTypeChoices:
    INTERNATIONAL = 'INTERNATIONAL'
    COUNTY = 'COUNTY'

    Choices = (
        (INTERNATIONAL, 'International'),
        (COUNTY, 'County'),
    )
