#!/usr/bin/env python3
"""
PrecisionX CLI Banner & Pixel Art Renderer
Inspired by terminal pixel art logos (e.g. Fastfetch / Neofetch)
Uses 24-bit TrueColor ANSI escape sequences.
"""

def print_banner(version="2026.1-sih"):
    art = [
        '..................',
        '........##........',
        '.......####.......',
        '......######......',
        '.################.',
        '......######......',
        '..##....##....##..',
        '..##....##....##..',
        '.####...##...####.',
        '..##....##....##..',
        '........##........',
        '..................',
        '..###........#..#.',
        '..#..#........##..',
        '..###.........##..',
        '..#..........#..#.',
        '..#.........#....#',
        '..................'
    ]

    palette_x = [
        (92, 196, 255),  # 0: Cyan Light
        (56, 175, 238),  # 1: Cyan
        (56, 175, 238),  # 2: Cyan
        (66, 190, 160),  # 3: Teal Green
        (125, 205, 75),  # 4: Lime
        (168, 208, 60),  # 5: Chartreuse
        (235, 190, 45),  # 6: Amber Gold
        (242, 130, 42),  # 7: Warm Orange
        (242, 130, 42),  # 8: Warm Orange
        (238, 76, 52),   # 9: Coral Red
        (238, 76, 52),   # 10: Coral Red
        (188, 70, 145),  # 11: Magenta
        (188, 70, 145),  # 12: Magenta
        (130, 80, 200),  # 13: Purple
        (130, 80, 200),  # 14: Purple
        (58, 115, 240),  # 15: Royal Blue
        (58, 115, 240),  # 16: Royal Blue
        (45, 95, 225)    # 17: Deep Blue
    ]

    side_text = [
        '',
        '',
        '\033[1;37mPrecisionX\033[0m \033[38;2;56;189;248mMetrology Workbench CLI\033[0m',
        '\033[38;2;148;163;184m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m',
        f'\033[1;32mVersion:\033[0m    {version}',
        '\033[1;33mStandard:\033[0m   OIML R-76 Class II/III/IIII',
        '\033[1;34mEngine:\033[0m     Automated Verification Suite',
        '\033[1;35mProtocol:\033[0m   Direct-Serial / Modbus RTU',
        '\033[1;36mTarget:\033[0m     Smart India Hackathon 2026',
        '\033[38;2;148;163;184m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m',
        '\033[38;2;148;163;184mRun \033[1;37mprecisionx --help\033[0;38;2;148;163;184m for available commands\033[0m',
        '',
        '',
        '',
        '',
        '',
        '',
        ''
    ]

    print()
    for y in range(len(art)):
        row_str = ''
        for x in range(len(art[y])):
            if art[y][x] == '#':
                r, g, b = palette_x[x]
                row_str += f'\033[38;2;{r};{g};{b}m██\033[0m'
            else:
                row_str += '  '
        txt = side_text[y] if y < len(side_text) else ''
        print(f'  {row_str}   {txt}')
    print()

if __name__ == '__main__':
    print_banner()
