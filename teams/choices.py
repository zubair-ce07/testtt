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
    RIGHT_ARM_SLOW = 'RIGHT_ARM_SLOW'
    LEFT_ARM_FAST = 'LEFT_ARM_FAST'
    LEFT_ARM_MEDIUM_FAST = 'LEFT_ARM_MEDIUM_FAST'
    LEFT_ARM_ORTHODOX = 'LEFT_ARM_ORTHODOX'
    LEFT_ARM_CHINAMAN = 'LEFT_ARM_CHINAMAN'
    LEFT_ARM_SLOW = 'LEFT_ARM_SLOW'

    Choices = (
        (RIGHT_ARM_FAST, 'Right Arm Fast'),
        (RIGHT_ARM_MEDIUM_FAST, 'Right Arm Medium Fast'),
        (RIGHT_ARM_OFF_BREAK, 'Right Arm OffBreak'),
        (RIGHT_ARM_LEG_BREAK_GOOGLY, 'Right Arm LegBreak Googly'),
        (RIGHT_ARM_ORTHODOX, 'Right Arm Orthodox'),
        (RIGHT_ARM_SLOW, 'Right Arm Slow'),
        (LEFT_ARM_FAST, 'Left Arm Fast'),
        (LEFT_ARM_MEDIUM_FAST, 'Left Arm Medium Fast'),
        (LEFT_ARM_ORTHODOX, 'Left Arm Orthodox'),
        (LEFT_ARM_CHINAMAN, 'Left Arm Chinaman'),
        (LEFT_ARM_SLOW, 'Left Arm Slow'),
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


BOWLING_STYLES = {
                'Right-arm fast': BowlingStyleChoices.RIGHT_ARM_FAST,
                'Right-arm fast-medium': BowlingStyleChoices.RIGHT_ARM_MEDIUM_FAST,
                'Right-arm medium-fast': BowlingStyleChoices.RIGHT_ARM_MEDIUM_FAST,
                'Right-arm medium': BowlingStyleChoices.RIGHT_ARM_MEDIUM_FAST,
                'Right-arm offbreak': BowlingStyleChoices.RIGHT_ARM_OFF_BREAK,
                'Legbreak googly': BowlingStyleChoices.RIGHT_ARM_LEG_BREAK_GOOGLY,
                'Left-arm fast': BowlingStyleChoices.LEFT_ARM_FAST,
                'Left-arm fast-medium': BowlingStyleChoices.LEFT_ARM_MEDIUM_FAST,
                'Left-arm medium-fast': BowlingStyleChoices.LEFT_ARM_MEDIUM_FAST,
                'Left-arm medium': BowlingStyleChoices.LEFT_ARM_MEDIUM_FAST,
                'Slow left-arm chinaman': BowlingStyleChoices.LEFT_ARM_CHINAMAN,
                'Slow left-arm orthodox': BowlingStyleChoices.LEFT_ARM_ORTHODOX,
                'Legbreak': BowlingStyleChoices.RIGHT_ARM_LEG_BREAK_GOOGLY,
                'Right-arm bowler': BowlingStyleChoices.RIGHT_ARM_MEDIUM_FAST,
                'Left-arm bowler': BowlingStyleChoices.LEFT_ARM_MEDIUM_FAST,
                'Right-arm slow': BowlingStyleChoices.RIGHT_ARM_SLOW,
                'Right-arm fast (roundarm)': BowlingStyleChoices.RIGHT_ARM_FAST,
                'Right-arm slow (underarm)': BowlingStyleChoices.RIGHT_ARM_SLOW,
                'Left-arm slow-medium': BowlingStyleChoices.LEFT_ARM_SLOW,
                'Right-arm slow-medium': BowlingStyleChoices.RIGHT_ARM_SLOW
}
