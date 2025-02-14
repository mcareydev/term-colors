#!/usr/bin/env python3

import argparse
import re
import sys


# Some needed escape sequences
ANSI = "\x1b]4;"
END = "\x07"
BG = "\x1b]11;"
BGTC = "\x1b[48;2;"
FG = "\x1b]10;"
FGTC = "\x1b[38;2;"
RESET = "\x1b[0m"


def _get_args() -> argparse.ArgumentParser:
    """Get user args

    Will print help if no args were given
    """
    parser = argparse.ArgumentParser(description="Set terminal to the specified color scheme or list/show color schemes")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--color_scheme", metavar="COLOR_SCHEME", choices=color_schemes, help="Set color scheme for the current terminal")
    group.add_argument("-e", "--regexp", metavar="PATTERN", help="Show color palettes for color schemes matching PATTERN")
    group.add_argument("-l", "--list", action="store_true", help="List all color schemes")
    group.add_argument("-s", "--show", action="store_true", help="Show color palettes for all color schemes")
    return parser.parse_args(args=None if sys.argv[1:] else ["--help"])


def _hex2rgb(hex_color: str) -> tuple:
    """Convert hex color code (#ff00ff) to semi-colon separated rgb format (255;0;255)"""
    hex_color = hex_color.lstrip("#")
    split_hex = [hex_color[i:i+2] for i in range(0, 6, 2)]
    r, g, b = map(lambda x: str(int(x, 16)), split_hex)
    return f"{r};{g};{b}"


def _hex2rgb_dict(scheme: dict) -> dict:
    """Convert entire dictionary from hex to rgb color values"""
    rgb_scheme = {}
    for k,v in scheme.items():
        if k == "colors":
            tmp_colors = list(map(_hex2rgb, v))
            rgb_scheme[k] = tmp_colors
        else:
            rgb_scheme[k] = _hex2rgb(v)
    return rgb_scheme


def set_colors(name: str) -> None:
    """Print a terminal sequence that will set the requested color scheme"""
    scheme = color_schemes[name]
    colors = scheme["colors"]
    color_string = ";".join([f"{x};{colors[x]}" for x in range(0,16)])
    print(f"{ANSI}{color_string}{END}")

    fg = f"{FG}{scheme['fg']}{END}"
    bg = f"{BG}{scheme['bg']}{END}"
    print(f"{fg}{bg}")


def show_colors(name: str) -> None:
    """Draw palette of requested color scheme"""
    scheme = color_schemes[name]
    colors = scheme["colors"]
    rgb_scheme = _hex2rgb_dict(scheme)
    rgb_colors = rgb_scheme["colors"]

    # Print title row in foreground and background color
    fg = f"{FGTC}{rgb_scheme['fg']}m"
    bg = f"{BGTC}{rgb_scheme['bg']}m"
    title = f"{name} | Foreground: {scheme['fg']} | Background: {scheme['bg']}"
    spacing = " "*(83 - len(title))
    color_display = [f"  {fg}{bg} {title}{spacing}{RESET}\n"]

    # Print text in each of the 16 colors on the background color
    fg = f"{FGTC}{rgb_scheme['fg']}m"
    bg = f"{BGTC}{rgb_scheme['bg']}m"
    color_display.extend([f"  {fg}{bg} Normal     "])
    for i in range(0,16):
        fg = f"{FGTC}{rgb_colors[i]}m"
        color_display.extend([f"{fg}{bg} {colors[i]} "])
        if (i+1) % 8 == 0:
            color_display.extend([f"{RESET}\n"])
        if i == 7:
            fg = f"{FGTC}{rgb_scheme['fg']}m"
            bg = f"{BGTC}{rgb_scheme['bg']}m"
            color_display.extend([f"  {fg}{bg} Bright     "])

    # Print foreground color over each of the 8 regular colors
    fg = f"{FGTC}{rgb_scheme['fg']}m"
    bg = f"{BGTC}{rgb_scheme['bg']}m"
    color_display.extend([f"  {fg}{bg} Background "])
    for i in range(0,8):
        bg = f"{BGTC}{rgb_colors[i]}m"
        color_display.extend([f"{fg}{bg} {colors[i]} "])
        if (i+1) % 8 == 0:
            color_display.extend([f"{RESET}\n"])
    print("".join(color_display))


def main() -> None:
    """Self-contained script for setting terminal color schemes"""
    # No default else, arg parser prints when no args are given
    args = _get_args()
    if args.color_scheme:
        set_colors(args.color_scheme)
    elif args.regexp:
        print()
        [show_colors(x) for x in color_schemes if re.search(args.regexp, x)]
    elif args.list:
        [print(x) for x in color_schemes]
    elif args.show:
        print()
        [show_colors(x) for x in color_schemes]


color_schemes = {
'0x96f' : {'fg': '#fcfcfa', 'bg': '#262427', 'colors': ['#262427', '#ff7272', '#bcdf59', '#ffca58', '#49cae4', '#a093e2', '#aee8f4', '#fcfcfa', '#545452', '#ff8787', '#c6e472', '#ffd271', '#64d2e8', '#aea3e6', '#baebf6', '#fcfcfa']},
'3024_day' : {'fg': '#4a4543', 'bg': '#f7f7f7', 'colors': ['#090300', '#db2d20', '#01a252', '#fded02', '#01a0e4', '#a16a94', '#b5e4f4', '#a5a2a2', '#5c5855', '#e8bbd0', '#3a3432', '#4a4543', '#807d7c', '#d6d5d4', '#cdab53', '#f7f7f7']},
'3024_night' : {'fg': '#a5a2a2', 'bg': '#090300', 'colors': ['#090300', '#db2d20', '#01a252', '#fded02', '#01a0e4', '#a16a94', '#b5e4f4', '#a5a2a2', '#5c5855', '#e8bbd0', '#3a3432', '#4a4543', '#807d7c', '#d6d5d4', '#cdab53', '#f7f7f7']},
'aardvark_blue' : {'fg': '#dddddd', 'bg': '#102040', 'colors': ['#191919', '#aa342e', '#4b8c0f', '#dbba00', '#1370d3', '#c43ac3', '#008eb0', '#bebebe', '#454545', '#f05b50', '#95dc55', '#ffe763', '#60a4ec', '#e26be2', '#60b6cb', '#f7f7f7']},
'abernathy' : {'fg': '#eeeeec', 'bg': '#111416', 'colors': ['#000000', '#cd0000', '#00cd00', '#cdcd00', '#1093f5', '#cd00cd', '#00cdcd', '#faebd7', '#404040', '#ff0000', '#00ff00', '#ffff00', '#11b5f6', '#ff00ff', '#00ffff', '#ffffff']},
'adventure' : {'fg': '#feffff', 'bg': '#040404', 'colors': ['#040404', '#d84a33', '#5da602', '#eebb6e', '#417ab3', '#e5c499', '#bdcfe5', '#dbded8', '#685656', '#d76b42', '#99b52c', '#ffb670', '#97d7ef', '#aa7900', '#bdcfe5', '#e4d5c7']},
'adventure_time' : {'fg': '#f8dcc0', 'bg': '#1f1d45', 'colors': ['#050404', '#bd0013', '#4ab118', '#e7741e', '#0f4ac6', '#665993', '#70a598', '#f8dcc0', '#4e7cbf', '#fc5f5a', '#9eff6e', '#efc11a', '#1997c6', '#9b5953', '#c8faf4', '#f6f5fb']},
'adwaita' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#241f31', '#c01c28', '#2ec27e', '#f5c211', '#1e78e4', '#9841bb', '#0ab9dc', '#c0bfbc', '#5e5c64', '#ed333b', '#57e389', '#f8e45c', '#51a1ff', '#c061cb', '#4fd2fd', '#f6f5f4']},
'adwaita_dark' : {'fg': '#ffffff', 'bg': '#1e1e1e', 'colors': ['#241f31', '#c01c28', '#2ec27e', '#f5c211', '#1e78e4', '#9841bb', '#0ab9dc', '#c0bfbc', '#5e5c64', '#ed333b', '#57e389', '#f8e45c', '#51a1ff', '#c061cb', '#4fd2fd', '#f6f5f4']},
'afterglow' : {'fg': '#d0d0d0', 'bg': '#212121', 'colors': ['#151515', '#ac4142', '#7e8e50', '#e5b567', '#6c99bb', '#9f4e85', '#7dd6cf', '#d0d0d0', '#505050', '#ac4142', '#7e8e50', '#e5b567', '#6c99bb', '#9f4e85', '#7dd6cf', '#f5f5f5']},
'alabaster' : {'fg': '#000000', 'bg': '#f7f7f7', 'colors': ['#000000', '#aa3731', '#448c27', '#cb9000', '#325cc0', '#7a3e9d', '#0083b2', '#f7f7f7', '#777777', '#f05050', '#60cb00', '#ffbc5d', '#007acc', '#e64ce6', '#00aacb', '#f7f7f7']},
'alien_blood' : {'fg': '#637d75', 'bg': '#0f1610', 'colors': ['#112616', '#7f2b27', '#2f7e25', '#717f24', '#2f6a7f', '#47587f', '#327f77', '#647d75', '#3c4812', '#e08009', '#18e000', '#bde000', '#00aae0', '#0058e0', '#00e0c4', '#73fa91']},
'andromeda' : {'fg': '#e5e5e5', 'bg': '#262a33', 'colors': ['#000000', '#cd3131', '#05bc79', '#e5e512', '#2472c8', '#bc3fbc', '#0fa8cd', '#e5e5e5', '#666666', '#cd3131', '#05bc79', '#e5e512', '#2472c8', '#bc3fbc', '#0fa8cd', '#e5e5e5']},
'apple_classic' : {'fg': '#d5a200', 'bg': '#2c2b2b', 'colors': ['#000000', '#c91b00', '#00c200', '#c7c400', '#0225c7', '#ca30c7', '#00c5c7', '#c7c7c7', '#686868', '#ff6e67', '#5ffa68', '#fffc67', '#6871ff', '#ff77ff', '#60fdff', '#ffffff']},
'apple_system_colors' : {'fg': '#ffffff', 'bg': '#1e1e1e', 'colors': ['#1a1a1a', '#cc372e', '#26a439', '#cdac08', '#0869cb', '#9647bf', '#479ec2', '#98989d', '#464646', '#ff453a', '#32d74b', '#ffd60a', '#0a84ff', '#bf5af2', '#76d6ff', '#ffffff']},
'apple_system_colors_light' : {'fg': '#000000', 'bg': '#feffff', 'colors': ['#1a1a1a', '#bc4437', '#51a148', '#c7ad3a', '#2e68c5', '#8c4bb8', '#5e9cbe', '#98989d', '#464646', '#eb5545', '#6bd45f', '#f8d84a', '#3b82f7', '#b260ea', '#8dd3fb', '#ffffff']},
'arcoiris' : {'fg': '#eee4d9', 'bg': '#201f1e', 'colors': ['#333333', '#da2700', '#12c258', '#ffc656', '#518bfc', '#e37bd9', '#63fad5', '#bab2b2', '#777777', '#ffb9b9', '#e3f6aa', '#ffddaa', '#b3e8f3', '#cbbaf9', '#bcffc7', '#efefef']},
'argonaut' : {'fg': '#fffaf4', 'bg': '#0e1019', 'colors': ['#232323', '#ff000f', '#8ce10b', '#ffb900', '#008df8', '#6d43a6', '#00d8eb', '#ffffff', '#444444', '#ff2740', '#abe15b', '#ffd242', '#0092ff', '#9a5feb', '#67fff0', '#ffffff']},
'arthur' : {'fg': '#ddeedd', 'bg': '#1c1c1c', 'colors': ['#3d352a', '#cd5c5c', '#86af80', '#e8ae5b', '#6495ed', '#deb887', '#b0c4de', '#bbaa99', '#554444', '#cc5533', '#88aa22', '#ffa75d', '#87ceeb', '#996600', '#b0c4de', '#ddccbb']},
'atelier_sulphurpool' : {'fg': '#979db4', 'bg': '#202746', 'colors': ['#202746', '#c94922', '#ac9739', '#c08b30', '#3d8fd1', '#6679cc', '#22a2c9', '#979db4', '#6b7394', '#c76b29', '#293256', '#5e6687', '#898ea4', '#dfe2f1', '#9c637a', '#f5f7ff']},
'atom' : {'fg': '#c5c8c6', 'bg': '#161719', 'colors': ['#000000', '#fd5ff1', '#87c38a', '#ffd7b1', '#85befd', '#b9b6fc', '#85befd', '#e0e0e0', '#000000', '#fd5ff1', '#94fa36', '#f5ffa8', '#96cbfe', '#b9b6fc', '#85befd', '#e0e0e0']},
'atom_one_light' : {'fg': '#2a2c33', 'bg': '#f9f9f9', 'colors': ['#000000', '#de3e35', '#3f953a', '#d2b67c', '#2f5af3', '#950095', '#3f953a', '#bbbbbb', '#000000', '#de3e35', '#3f953a', '#d2b67c', '#2f5af3', '#a00095', '#3f953a', '#ffffff']},
'aura' : {'fg': '#edecee', 'bg': '#15141b', 'colors': ['#110f18', '#ff6767', '#61ffca', '#ffca85', '#a277ff', '#a277ff', '#61ffca', '#edecee', '#4d4d4d', '#ffca85', '#a277ff', '#ffca85', '#a277ff', '#a277ff', '#61ffca', '#edecee']},
'aurora' : {'fg': '#ffca28', 'bg': '#23262e', 'colors': ['#23262e', '#f0266f', '#8fd46d', '#ffe66d', '#0321d7', '#ee5d43', '#03d6b8', '#c74ded', '#292e38', '#f92672', '#8fd46d', '#ffe66d', '#03d6b8', '#ee5d43', '#03d6b8', '#c74ded']},
'ayu' : {'fg': '#e6e1cf', 'bg': '#0f1419', 'colors': ['#000000', '#ff3333', '#b8cc52', '#e7c547', '#36a3d9', '#f07178', '#95e6cb', '#ffffff', '#323232', '#ff6565', '#eafe84', '#fff779', '#68d5ff', '#ffa3aa', '#c7fffd', '#ffffff']},
'ayu_light' : {'fg': '#5c6773', 'bg': '#fafafa', 'colors': ['#000000', '#ff3333', '#86b300', '#f29718', '#41a6d9', '#f07178', '#4dbf99', '#ffffff', '#323232', '#ff6565', '#b8e532', '#ffc94a', '#73d8ff', '#ffa3aa', '#7ff1cb', '#ffffff']},
'ayu_mirage' : {'fg': '#cbccc6', 'bg': '#1f2430', 'colors': ['#191e2a', '#ed8274', '#a6cc70', '#fad07b', '#6dcbfa', '#cfbafa', '#90e1c6', '#c7c7c7', '#686868', '#f28779', '#bae67e', '#ffd580', '#73d0ff', '#d4bfff', '#95e6cb', '#ffffff']},
'banana_blueberry' : {'fg': '#cccccc', 'bg': '#191323', 'colors': ['#17141f', '#ff6b7f', '#00bd9c', '#e6c62f', '#22e8df', '#dc396a', '#56b6c2', '#f1f1f1', '#495162', '#fe9ea1', '#98c379', '#f9e46b', '#91fff4', '#da70d6', '#bcf3ff', '#ffffff']},
'batman' : {'fg': '#6f6f6f', 'bg': '#1b1d1e', 'colors': ['#1b1d1e', '#e6dc44', '#c8be46', '#f4fd22', '#737174', '#747271', '#62605f', '#c6c5bf', '#505354', '#fff78e', '#fff27d', '#feed6c', '#919495', '#9a9a9d', '#a3a3a6', '#dadbd6']},
'belafonte_day' : {'fg': '#45373c', 'bg': '#d5ccba', 'colors': ['#20111b', '#be100e', '#858162', '#eaa549', '#426a79', '#97522c', '#989a9c', '#968c83', '#5e5252', '#be100e', '#858162', '#eaa549', '#426a79', '#97522c', '#989a9c', '#d5ccba']},
'belafonte_night' : {'fg': '#968c83', 'bg': '#20111b', 'colors': ['#20111b', '#be100e', '#858162', '#eaa549', '#426a79', '#97522c', '#989a9c', '#968c83', '#5e5252', '#be100e', '#858162', '#eaa549', '#426a79', '#97522c', '#989a9c', '#d5ccba']},
'birds_of_paradise' : {'fg': '#e0dbb7', 'bg': '#2a1f1d', 'colors': ['#573d26', '#be2d26', '#6ba18a', '#e99d2a', '#5a86ad', '#ac80a6', '#74a6ad', '#e0dbb7', '#9b6c4a', '#e84627', '#95d8ba', '#d0d150', '#b8d3ed', '#d19ecb', '#93cfd7', '#fff9d5']},
'blazer' : {'fg': '#d9e6f2', 'bg': '#0d1926', 'colors': ['#000000', '#b87a7a', '#7ab87a', '#b8b87a', '#7a7ab8', '#b87ab8', '#7ab8b8', '#d9d9d9', '#262626', '#dbbdbd', '#bddbbd', '#dbdbbd', '#bdbddb', '#dbbddb', '#bddbdb', '#ffffff']},
'blue_berry_pie' : {'fg': '#babab9', 'bg': '#1c0c28', 'colors': ['#0a4c62', '#99246e', '#5cb1b3', '#eab9a8', '#90a5bd', '#9d54a7', '#7e83cc', '#f0e8d6', '#201637', '#c87272', '#0a6c7e', '#7a3188', '#39173d', '#bc94b7', '#5e6071', '#0a6c7e']},
'blue_dolphin' : {'fg': '#c5f2ff', 'bg': '#006984', 'colors': ['#292d3e', '#ff8288', '#b4e88d', '#f4d69f', '#82aaff', '#e9c1ff', '#89ebff', '#d0d0d0', '#434758', '#ff8b92', '#ddffa7', '#ffe585', '#9cc4ff', '#ddb0f6', '#a3f7ff', '#ffffff']},
'blue_matrix' : {'fg': '#00a2ff', 'bg': '#101116', 'colors': ['#101116', '#ff5680', '#00ff9c', '#fffc58', '#00b0ff', '#d57bff', '#76c1ff', '#c7c7c7', '#686868', '#ff6e67', '#5ffa68', '#fffc67', '#6871ff', '#d682ec', '#60fdff', '#ffffff']},
'bluloco_dark' : {'fg': '#b9c0cb', 'bg': '#282c34', 'colors': ['#41444d', '#fc2f52', '#25a45c', '#ff936a', '#3476ff', '#7a82da', '#4483aa', '#cdd4e0', '#8f9aae', '#ff6480', '#3fc56b', '#f9c859', '#10b1fe', '#ff78f8', '#5fb9bc', '#ffffff']},
'bluloco_light' : {'fg': '#373a41', 'bg': '#f9f9f9', 'colors': ['#373a41', '#d52753', '#23974a', '#df631c', '#275fe4', '#823ff1', '#27618d', '#babbc2', '#676a77', '#ff6480', '#3cbc66', '#c5a332', '#0099e1', '#ce33c0', '#6d93bb', '#d3d3d3']},
'borland' : {'fg': '#ffff4e', 'bg': '#0000a4', 'colors': ['#4f4f4f', '#ff6c60', '#a8ff60', '#ffffb6', '#96cbfe', '#ff73fd', '#c6c5fe', '#eeeeee', '#7c7c7c', '#ffb6b0', '#ceffac', '#ffffcc', '#b5dcff', '#ff9cfe', '#dfdffe', '#ffffff']},
'breeze' : {'fg': '#eff0f1', 'bg': '#31363b', 'colors': ['#31363b', '#ed1515', '#11d116', '#f67400', '#1d99f3', '#9b59b6', '#1abc9c', '#eff0f1', '#7f8c8d', '#c0392b', '#1cdc9a', '#fdbc4b', '#3daee9', '#8e44ad', '#16a085', '#fcfcfc']},
'bright_lights' : {'fg': '#b3c9d7', 'bg': '#191919', 'colors': ['#191919', '#ff355b', '#b7e876', '#ffc251', '#76d4ff', '#ba76e7', '#6cbfb5', '#c2c8d7', '#191919', '#ff355b', '#b7e876', '#ffc251', '#76d5ff', '#ba76e7', '#6cbfb5', '#c2c8d7']},
'broadcast' : {'fg': '#e6e1dc', 'bg': '#2b2b2b', 'colors': ['#000000', '#da4939', '#519f50', '#ffd24a', '#6d9cbe', '#d0d0ff', '#6e9cbe', '#ffffff', '#323232', '#ff7b6b', '#83d182', '#ffff7c', '#9fcef0', '#ffffff', '#a0cef0', '#ffffff']},
'brogrammer' : {'fg': '#d6dbe5', 'bg': '#131313', 'colors': ['#1f1f1f', '#f81118', '#2dc55e', '#ecba0f', '#2a84d2', '#4e5ab7', '#1081d6', '#d6dbe5', '#d6dbe5', '#de352e', '#1dd361', '#f3bd09', '#1081d6', '#5350b9', '#0f7ddb', '#ffffff']},
'builtin_dark' : {'fg': '#bbbbbb', 'bg': '#000000', 'colors': ['#000000', '#bb0000', '#00bb00', '#bbbb00', '#0000bb', '#bb00bb', '#00bbbb', '#bbbbbb', '#555555', '#ff5555', '#55ff55', '#ffff55', '#5555ff', '#ff55ff', '#55ffff', '#ffffff']},
'builtin_light' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#000000', '#bb0000', '#00bb00', '#bbbb00', '#0000bb', '#bb00bb', '#00bbbb', '#bbbbbb', '#555555', '#ff5555', '#55ff55', '#ffff55', '#5555ff', '#ff55ff', '#55ffff', '#ffffff']},
'builtin_pastel_dark' : {'fg': '#bbbbbb', 'bg': '#000000', 'colors': ['#4f4f4f', '#ff6c60', '#a8ff60', '#ffffb6', '#96cbfe', '#ff73fd', '#c6c5fe', '#eeeeee', '#7c7c7c', '#ffb6b0', '#ceffac', '#ffffcc', '#b5dcff', '#ff9cfe', '#dfdffe', '#ffffff']},
'builtin_solarized_dark' : {'fg': '#839496', 'bg': '#002b36', 'colors': ['#073642', '#dc322f', '#859900', '#b58900', '#268bd2', '#d33682', '#2aa198', '#eee8d5', '#002b36', '#cb4b16', '#586e75', '#657b83', '#839496', '#6c71c4', '#93a1a1', '#fdf6e3']},
'builtin_solarized_light' : {'fg': '#657b83', 'bg': '#fdf6e3', 'colors': ['#073642', '#dc322f', '#859900', '#b58900', '#268bd2', '#d33682', '#2aa198', '#eee8d5', '#002b36', '#cb4b16', '#586e75', '#657b83', '#839496', '#6c71c4', '#93a1a1', '#fdf6e3']},
'builtin_tango_dark' : {'fg': '#ffffff', 'bg': '#000000', 'colors': ['#000000', '#cc0000', '#4e9a06', '#c4a000', '#3465a4', '#75507b', '#06989a', '#d3d7cf', '#555753', '#ef2929', '#8ae234', '#fce94f', '#729fcf', '#ad7fa8', '#34e2e2', '#eeeeec']},
'builtin_tango_light' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#000000', '#cc0000', '#4e9a06', '#c4a000', '#3465a4', '#75507b', '#06989a', '#d3d7cf', '#555753', '#ef2929', '#8ae234', '#fce94f', '#729fcf', '#ad7fa8', '#34e2e2', '#eeeeec']},
'c64' : {'fg': '#7869c4', 'bg': '#40318d', 'colors': ['#090300', '#883932', '#55a049', '#bfce72', '#40318d', '#8b3f96', '#67b6bd', '#ffffff', '#000000', '#883932', '#55a049', '#bfce72', '#40318d', '#8b3f96', '#67b6bd', '#f7f7f7']},
'calamity' : {'fg': '#d5ced9', 'bg': '#2f2833', 'colors': ['#2f2833', '#fc644d', '#a5f69c', '#e9d7a5', '#3b79c7', '#f92672', '#74d3de', '#d5ced9', '#7e6c88', '#fc644d', '#a5f69c', '#e9d7a5', '#3b79c7', '#f92672', '#74d3de', '#ffffff']},
'catppuccin_frappe' : {'fg': '#c6d0f5', 'bg': '#303446', 'colors': ['#51576d', '#e78284', '#a6d189', '#e5c890', '#8caaee', '#f4b8e4', '#81c8be', '#a5adce', '#626880', '#e67172', '#8ec772', '#d9ba73', '#7b9ef0', '#f2a4db', '#5abfb5', '#b5bfe2']},
'catppuccin_latte' : {'fg': '#4c4f69', 'bg': '#eff1f5', 'colors': ['#5c5f77', '#d20f39', '#40a02b', '#df8e1d', '#1e66f5', '#ea76cb', '#179299', '#acb0be', '#6c6f85', '#de293e', '#49af3d', '#eea02d', '#456eff', '#fe85d8', '#2d9fa8', '#bcc0cc']},
'catppuccin_macchiato' : {'fg': '#cad3f5', 'bg': '#24273a', 'colors': ['#494d64', '#ed8796', '#a6da95', '#eed49f', '#8aadf4', '#f5bde6', '#8bd5ca', '#a5adcb', '#5b6078', '#ec7486', '#8ccf7f', '#e1c682', '#78a1f6', '#f2a9dd', '#63cbc0', '#b8c0e0']},
'catppuccin_mocha' : {'fg': '#cdd6f4', 'bg': '#1e1e2e', 'colors': ['#45475a', '#f38ba8', '#a6e3a1', '#f9e2af', '#89b4fa', '#f5c2e7', '#94e2d5', '#a6adc8', '#585b70', '#f37799', '#89d88b', '#ebd391', '#74a8fc', '#f2aede', '#6bd7ca', '#bac2de']},
'cga' : {'fg': '#aaaaaa', 'bg': '#000000', 'colors': ['#000000', '#aa0000', '#00aa00', '#aa5500', '#0000aa', '#aa00aa', '#00aaaa', '#aaaaaa', '#555555', '#ff5555', '#55ff55', '#ffff55', '#5555ff', '#ff55ff', '#55ffff', '#ffffff']},
'chalk' : {'fg': '#d2d8d9', 'bg': '#2b2d2e', 'colors': ['#7d8b8f', '#b23a52', '#789b6a', '#b9ac4a', '#2a7fac', '#bd4f5a', '#44a799', '#d2d8d9', '#888888', '#f24840', '#80c470', '#ffeb62', '#4196ff', '#fc5275', '#53cdbd', '#d2d8d9']},
'chalkboard' : {'fg': '#d9e6f2', 'bg': '#29262f', 'colors': ['#000000', '#c37372', '#72c373', '#c2c372', '#7372c3', '#c372c2', '#72c2c3', '#d9d9d9', '#323232', '#dbaaaa', '#aadbaa', '#dadbaa', '#aaaadb', '#dbaada', '#aadadb', '#ffffff']},
'challenger_deep' : {'fg': '#cbe1e7', 'bg': '#1e1c31', 'colors': ['#141228', '#ff5458', '#62d196', '#ffb378', '#65b2ff', '#906cff', '#63f2f1', '#a6b3cc', '#565575', '#ff8080', '#95ffa4', '#ffe9aa', '#91ddff', '#c991e1', '#aaffe4', '#cbe3e7']},
'chester' : {'fg': '#ffffff', 'bg': '#2c3643', 'colors': ['#080200', '#fa5e5b', '#16c98d', '#ffc83f', '#288ad6', '#d34590', '#28ddde', '#e7e7e7', '#6f6b68', '#fa5e5b', '#16c98d', '#feef6d', '#278ad6', '#d34590', '#27dede', '#ffffff']},
'ciapre' : {'fg': '#aea47a', 'bg': '#191c27', 'colors': ['#181818', '#810009', '#48513b', '#cc8b3f', '#576d8c', '#724d7c', '#5c4f4b', '#aea47f', '#555555', '#ac3835', '#a6a75d', '#dcdf7c', '#3097c6', '#d33061', '#f3dbb2', '#f4f4f4']},
'citruszest' : {'fg': '#bfbfbf', 'bg': '#121212', 'colors': ['#404040', '#ff5454', '#00cc7a', '#ffd400', '#00bfff', '#ff90fe', '#48d1cc', '#bfbfbf', '#808080', '#ff1a75', '#1affa3', '#ffff00', '#33cfff', '#ffb2fe', '#00fff2', '#f9f9f9']},
'clrs' : {'fg': '#262626', 'bg': '#ffffff', 'colors': ['#000000', '#f8282a', '#328a5d', '#fa701d', '#135cd0', '#9f00bd', '#33c3c1', '#b3b3b3', '#555753', '#fb0416', '#2cc631', '#fdd727', '#1670ff', '#e900b0', '#3ad5ce', '#eeeeec']},
'cobalt2' : {'fg': '#ffffff', 'bg': '#132738', 'colors': ['#000000', '#ff0000', '#38de21', '#ffe50a', '#1460d2', '#ff005d', '#00bbbb', '#bbbbbb', '#555555', '#f40e17', '#3bd01d', '#edc809', '#5555ff', '#ff55ff', '#6ae3fa', '#ffffff']},
'cobalt_neon' : {'fg': '#8ff586', 'bg': '#142838', 'colors': ['#142631', '#ff2320', '#3ba5ff', '#e9e75c', '#8ff586', '#781aa0', '#8ff586', '#ba46b2', '#fff688', '#d4312e', '#8ff586', '#e9f06d', '#3c7dd2', '#8230a7', '#6cbc67', '#8ff586']},
'cobalt_next' : {'fg': '#d8dee9', 'bg': '#1b2b34', 'colors': ['#000000', '#ed5f7d', '#99c794', '#fac863', '#5a9bcf', '#c5a5c5', '#5fb3b3', '#d8dee9', '#65737e', '#d6838c', '#c1dcbe', '#ffde9b', '#8abee7', '#edcded', '#9be2e2', '#ffffff']},
'cobalt_next_dark' : {'fg': '#d8dee9', 'bg': '#0f1c23', 'colors': ['#282f36', '#e6576a', '#99c794', '#fac863', '#5a9bcf', '#c5a5c5', '#5fb3b3', '#d8dee9', '#65737e', '#d6838c', '#c1dcbe', '#ffde9b', '#8abee7', '#edcded', '#9be2e2', '#ffffff']},
'cobalt_next_minimal' : {'fg': '#d8dee9', 'bg': '#0f1c23', 'colors': ['#343d46', '#ed6f7d', '#99c794', '#fac863', '#5a9bcf', '#c5a5c5', '#5fb3b3', '#d8dee9', '#65737e', '#d6838c', '#c1dcbe', '#ffde9b', '#8abee7', '#edcded', '#9be2e2', '#ffffff']},
'coffee_theme' : {'fg': '#000000', 'bg': '#f5deb3', 'colors': ['#000000', '#c91b00', '#00c200', '#c7c400', '#0225c7', '#ca30c7', '#00c5c7', '#c7c7c7', '#686868', '#ff6e67', '#5ffa68', '#fffc67', '#6871ff', '#ff77ff', '#60fdff', '#ffffff']},
'crayon_pony_fish' : {'fg': '#68525a', 'bg': '#150707', 'colors': ['#2b1b1d', '#91002b', '#579524', '#ab311b', '#8c87b0', '#692f50', '#e8a866', '#68525a', '#3d2b2e', '#c5255d', '#8dff57', '#c8381d', '#cfc9ff', '#fc6cba', '#ffceaf', '#b0949d']},
'cutie_pro' : {'fg': '#d5d0c9', 'bg': '#181818', 'colors': ['#000000', '#f56e7f', '#bec975', '#f58669', '#42d9c5', '#d286b7', '#37cb8a', '#d5c3c3', '#88847f', '#e5a1a3', '#e8d6a7', '#f1bb79', '#80c5de', '#b294bb', '#9dccbb', '#ffffff']},
'cyberdyne' : {'fg': '#00ff92', 'bg': '#151144', 'colors': ['#080808', '#ff8373', '#00c172', '#d2a700', '#0071cf', '#ff90fe', '#6bffdd', '#f1f1f1', '#2e2e2e', '#ffc4be', '#d6fcba', '#fffed5', '#c2e3ff', '#ffb2fe', '#e6e7fe', '#ffffff']},
'cyberpunk' : {'fg': '#e5e5e5', 'bg': '#332a57', 'colors': ['#000000', '#ff7092', '#00fbac', '#fffa6a', '#00bfff', '#df95ff', '#86cbfe', '#ffffff', '#000000', '#ff8aa4', '#21f6bc', '#fff787', '#1bccfd', '#e6aefe', '#99d6fc', '#ffffff']},
'cyberpunk_scarlet_protocol' : {'fg': '#d13554', 'bg': '#101116', 'colors': ['#101116', '#ea3356', '#64d98c', '#faf968', '#306fb1', '#ba3ec1', '#59c2c6', '#c7c7c7', '#686868', '#ed776d', '#8df77a', '#fefc7f', '#6a71f6', '#ae40e4', '#8efafd', '#ffffff']},
'dark+' : {'fg': '#cccccc', 'bg': '#1e1e1e', 'colors': ['#000000', '#cd3131', '#0dbc79', '#e5e510', '#2472c8', '#bc3fbc', '#11a8cd', '#e5e5e5', '#666666', '#f14c4c', '#23d18b', '#f5f543', '#3b8eea', '#d670d6', '#29b8db', '#e5e5e5']},
'dark_modern' : {'fg': '#cccccc', 'bg': '#1f1f1f', 'colors': ['#272727', '#f74949', '#2ea043', '#9e6a03', '#0078d4', '#d01273', '#1db4d6', '#cccccc', '#5d5d5d', '#dc5452', '#23d18b', '#f5f543', '#3b8eea', '#d670d6', '#29b8db', '#e5e5e5']},
'dark_pastel' : {'fg': '#ffffff', 'bg': '#000000', 'colors': ['#000000', '#ff5555', '#55ff55', '#ffff55', '#5555ff', '#ff55ff', '#55ffff', '#bbbbbb', '#555555', '#ff5555', '#55ff55', '#ffff55', '#5555ff', '#ff55ff', '#55ffff', '#ffffff']},
'darkermatrix' : {'fg': '#28380d', 'bg': '#070c0e', 'colors': ['#091013', '#002e18', '#6fa64c', '#595900', '#00cb6b', '#412a4d', '#125459', '#002e19', '#333333', '#00381d', '#90d762', '#e2e500', '#00ff87', '#412a4d', '#176c73', '#00381e']},
'darkmatrix' : {'fg': '#3e5715', 'bg': '#070c0e', 'colors': ['#091013', '#006536', '#6fa64c', '#7e8000', '#2c9a84', '#452d53', '#114d53', '#006536', '#333333', '#00733d', '#90d762', '#e2e500', '#46d8b8', '#4a3059', '#12545a', '#006536']},
'darkside' : {'fg': '#bababa', 'bg': '#222324', 'colors': ['#000000', '#e8341c', '#68c256', '#f2d42c', '#1c98e8', '#8e69c9', '#1c98e8', '#bababa', '#000000', '#e05a4f', '#77b869', '#efd64b', '#387cd3', '#957bbe', '#3d97e2', '#bababa']},
'dayfox' : {'fg': '#3d2b5a', 'bg': '#f6f2ee', 'colors': ['#352c24', '#a5222f', '#396847', '#ac5402', '#2848a9', '#6e33ce', '#287980', '#f2e9e1', '#534c45', '#b3434e', '#577f63', '#b86e28', '#4863b6', '#8452d5', '#488d93', '#f4ece6']},
'deep' : {'fg': '#cdcdcd', 'bg': '#090909', 'colors': ['#000000', '#d70005', '#1cd915', '#d9bd26', '#5665ff', '#b052da', '#50d2da', '#e0e0e0', '#535353', '#fb0007', '#22ff18', '#fedc2b', '#9fa9ff', '#e09aff', '#8df9ff', '#ffffff']},
'desert' : {'fg': '#ffffff', 'bg': '#333333', 'colors': ['#4d4d4d', '#ff2b2b', '#98fb98', '#f0e68c', '#cd853f', '#ffdead', '#ffa0a0', '#f5deb3', '#555555', '#ff5555', '#55ff55', '#ffff55', '#87ceff', '#ff55ff', '#ffd700', '#ffffff']},
'detuned' : {'fg': '#c7c7c7', 'bg': '#000000', 'colors': ['#171717', '#ea5386', '#b3e153', '#e4da81', '#4192d3', '#8f3ef6', '#6cb4d5', '#c7c7c7', '#686868', '#ea86ac', '#c5e280', '#fdf38f', '#55bbf9', '#b9a0f9', '#7fd4fb', '#ffffff']},
'dimidium' : {'fg': '#bab7b6', 'bg': '#141414', 'colors': ['#000000', '#cf494c', '#60b442', '#db9c11', '#0575d8', '#af5ed2', '#1db6bb', '#bab7b6', '#817e7e', '#ff643b', '#37e57b', '#fccd1a', '#688dfd', '#ed6fe9', '#32e0fb', '#d3d8d9']},
'dimmed_monokai' : {'fg': '#b9bcba', 'bg': '#1f1f1f', 'colors': ['#3a3d43', '#be3f48', '#879a3b', '#c5a635', '#4f76a1', '#855c8d', '#578fa4', '#b9bcba', '#888987', '#fb001f', '#0f722f', '#c47033', '#186de3', '#fb0067', '#2e706d', '#fdffb9']},
'django' : {'fg': '#f8f8f8', 'bg': '#0b2f20', 'colors': ['#000000', '#fd6209', '#41a83e', '#ffe862', '#245032', '#f8f8f8', '#9df39f', '#ffffff', '#323232', '#ff943b', '#73da70', '#ffff94', '#568264', '#ffffff', '#cfffd1', '#ffffff']},
'django_reborn_again' : {'fg': '#dadedc', 'bg': '#051f14', 'colors': ['#000000', '#fd6209', '#41a83e', '#ffe862', '#245032', '#f8f8f8', '#9df39f', '#ffffff', '#323232', '#ff943b', '#73da70', '#ffff94', '#568264', '#ffffff', '#cfffd1', '#ffffff']},
'django_smooth' : {'fg': '#f8f8f8', 'bg': '#245032', 'colors': ['#000000', '#fd6209', '#41a83e', '#ffe862', '#989898', '#f8f8f8', '#9df39f', '#e8e8e7', '#323232', '#ff943b', '#73da70', '#ffff94', '#cacaca', '#ffffff', '#cfffd1', '#ffffff']},
'doom_one' : {'fg': '#bbc2cf', 'bg': '#282c34', 'colors': ['#000000', '#ff6c6b', '#98be65', '#ecbe7b', '#a9a1e1', '#c678dd', '#51afef', '#bbc2cf', '#000000', '#ff6655', '#99bb66', '#ecbe7b', '#a9a1e1', '#c678dd', '#51afef', '#bfbfbf']},
'doom_peacock' : {'fg': '#ede0ce', 'bg': '#2b2a27', 'colors': ['#1c1f24', '#cb4b16', '#26a6a6', '#bcd42a', '#2a6cc6', '#a9a1e1', '#5699af', '#ede0ce', '#2b2a27', '#ff5d38', '#98be65', '#e6f972', '#51afef', '#c678dd', '#46d9ff', '#dfdfdf']},
'dot_gov' : {'fg': '#ebebeb', 'bg': '#262c35', 'colors': ['#191919', '#bf091d', '#3d9751', '#f6bb34', '#17b2e0', '#7830b0', '#8bd2ed', '#ffffff', '#191919', '#bf091d', '#3d9751', '#f6bb34', '#17b2e0', '#7830b0', '#8bd2ed', '#ffffff']},
'dracula' : {'fg': '#e6e6e6', 'bg': '#1e1f29', 'colors': ['#000000', '#ff5555', '#50fa7b', '#f1fa8c', '#bd93f9', '#ff79c6', '#8be9fd', '#bbbbbb', '#555555', '#ff5555', '#50fa7b', '#f1fa8c', '#bd93f9', '#ff79c6', '#8be9fd', '#ffffff']},
'dracula+' : {'fg': '#f8f8f2', 'bg': '#212121', 'colors': ['#21222c', '#ff5555', '#50fa7b', '#ffcb6b', '#82aaff', '#c792ea', '#8be9fd', '#f8f8f2', '#545454', '#ff6e6e', '#69ff94', '#ffcb6b', '#d6acff', '#ff92df', '#a4ffff', '#f8f8f2']},
'duckbones' : {'fg': '#ebefc0', 'bg': '#0e101a', 'colors': ['#0e101a', '#e03600', '#5dcd97', '#e39500', '#00a3cb', '#795ccc', '#00a3cb', '#ebefc0', '#2b2f46', '#ff4821', '#58db9e', '#f6a100', '#00b4e0', '#b3a1e6', '#00b4e0', '#b3b692']},
'duotone_dark' : {'fg': '#b7a1ff', 'bg': '#1f1d27', 'colors': ['#1f1d27', '#d9393e', '#2dcd73', '#d9b76e', '#ffc284', '#de8d40', '#2488ff', '#b7a1ff', '#353147', '#d9393e', '#2dcd73', '#d9b76e', '#ffc284', '#de8d40', '#2488ff', '#eae5ff']},
'earthsong' : {'fg': '#e5c7a9', 'bg': '#292520', 'colors': ['#121418', '#c94234', '#85c54c', '#f5ae2e', '#1398b9', '#d0633d', '#509552', '#e5c6aa', '#675f54', '#ff645a', '#98e036', '#e0d561', '#5fdaff', '#ff9269', '#84f088', '#f6f7ec']},
'electron_highlighter' : {'fg': '#a8b5d1', 'bg': '#24283b', 'colors': ['#15161e', '#f7768e', '#58ffc7', '#ffd9af', '#82aaff', '#d2a6ef', '#57f9ff', '#7c8eac', '#506686', '#f7768e', '#58ffc7', '#ffd9af', '#82aaff', '#d2a6ef', '#57f9ff', '#c5cee0']},
'elegant' : {'fg': '#cfd2d6', 'bg': '#292b31', 'colors': ['#0c1221', '#ea335b', '#95ca9a', '#f7cd94', '#93aadd', '#bf94e5', '#8ccaec', '#ffffff', '#575656', '#ea335b', '#95ca9a', '#f7cd94', '#93aadd', '#bf94e5', '#5faae9', '#ffffff']},
'elemental' : {'fg': '#807a74', 'bg': '#22211d', 'colors': ['#3c3c30', '#98290f', '#479a43', '#7f7111', '#497f7d', '#7f4e2f', '#387f58', '#807974', '#555445', '#e0502a', '#61e070', '#d69927', '#79d9d9', '#cd7c54', '#59d599', '#fff1e9']},
'elementary' : {'fg': '#efefef', 'bg': '#181818', 'colors': ['#242424', '#d71c15', '#5aa513', '#fdb40c', '#063b8c', '#e40038', '#2595e1', '#efefef', '#4b4b4b', '#fc1c18', '#6bc219', '#fec80e', '#0955ff', '#fb0050', '#3ea8fc', '#8c00ec']},
'embers_dark' : {'fg': '#a39a90', 'bg': '#16130f', 'colors': ['#16130f', '#826d57', '#57826d', '#6d8257', '#6d5782', '#82576d', '#576d82', '#a39a90', '#5a5047', '#828257', '#2c2620', '#433b32', '#8a8075', '#beb6ae', '#825757', '#dbd6d1']},
'encom' : {'fg': '#00a595', 'bg': '#000000', 'colors': ['#000000', '#9f0000', '#008b00', '#ffd000', '#0081ff', '#bc00ca', '#008b8b', '#bbbbbb', '#555555', '#ff0000', '#00ee00', '#ffff00', '#0000ff', '#ff00ff', '#00cdcd', '#ffffff']},
'espresso' : {'fg': '#ffffff', 'bg': '#323232', 'colors': ['#353535', '#d25252', '#a5c261', '#ffc66d', '#6c99bb', '#d197d9', '#bed6ff', '#eeeeec', '#535353', '#f00c0c', '#c2e075', '#e1e48b', '#8ab7d9', '#efb5f7', '#dcf4ff', '#ffffff']},
'espresso_libre' : {'fg': '#b8a898', 'bg': '#2a211c', 'colors': ['#000000', '#cc0000', '#1a921c', '#f0e53a', '#0066ff', '#c5656b', '#06989a', '#d3d7cf', '#555753', '#ef2929', '#9aff87', '#fffb5c', '#43a8ed', '#ff818a', '#34e2e2', '#eeeeec']},
'everblush' : {'fg': '#dadada', 'bg': '#141b1e', 'colors': ['#232a2d', '#e57474', '#8ccf7e', '#e5c76b', '#67b0e8', '#c47fd5', '#6cbfbf', '#b3b9b8', '#2d3437', '#ef7e7e', '#96d988', '#f4d67a', '#71baf2', '#ce89df', '#67cbe7', '#bdc3c2']},
'everforest_dark_hard' : {'fg': '#d3c6aa', 'bg': '#1e2326', 'colors': ['#7a8478', '#e67e80', '#a7c080', '#dbbc7f', '#7fbbb3', '#d699b6', '#83c092', '#f2efdf', '#a6b0a0', '#f85552', '#8da101', '#dfa000', '#3a94c5', '#df69ba', '#35a77c', '#fffbef']},
'fahrenheit' : {'fg': '#ffffce', 'bg': '#000000', 'colors': ['#1d1d1d', '#cda074', '#9e744d', '#fecf75', '#720102', '#734c4d', '#979797', '#ffffce', '#000000', '#fecea0', '#cc734d', '#fd9f4d', '#cb4a05', '#4e739f', '#fed04d', '#ffffff']},
'fairyfloss' : {'fg': '#f8f8f2', 'bg': '#5a5475', 'colors': ['#040303', '#f92672', '#c2ffdf', '#e6c000', '#c2ffdf', '#ffb8d1', '#c5a3ff', '#f8f8f0', '#6090cb', '#ff857f', '#c2ffdf', '#ffea00', '#c2ffdf', '#ffb8d1', '#c5a3ff', '#f8f8f0']},
'farmhouse_dark' : {'fg': '#e8e4e1', 'bg': '#1d2027', 'colors': ['#1d2027', '#ba0004', '#549d00', '#c87300', '#0049e6', '#9f1b61', '#1fb65c', '#e8e4e1', '#394047', '#eb0009', '#7ac100', '#ea9a00', '#006efe', '#bf3b7f', '#19e062', '#f4eef0']},
'farmhouse_light' : {'fg': '#1d2027', 'bg': '#e8e4e1', 'colors': ['#1d2027', '#8d0003', '#3a7d00', '#a95600', '#092ccd', '#820046', '#229256', '#e8e4e1', '#394047', '#eb0009', '#7ac100', '#ea9a00', '#006efe', '#bf3b7f', '#19e062', '#f4eef0']},
'fideloper' : {'fg': '#dbdae0', 'bg': '#292f33', 'colors': ['#292f33', '#cb1e2d', '#edb8ac', '#b7ab9b', '#2e78c2', '#c0236f', '#309186', '#eae3ce', '#092028', '#d4605a', '#d4605a', '#a86671', '#7c85c4', '#5c5db2', '#819090', '#fcf4df']},
'firefly_traditional' : {'fg': '#f5f5f5', 'bg': '#000000', 'colors': ['#000000', '#c23720', '#33bc26', '#afad24', '#5a63ff', '#d53ad2', '#33bbc7', '#cccccc', '#828282', '#ff3b1e', '#2ee720', '#ecec16', '#838dff', '#ff5cfe', '#29f0f0', '#ebebeb']},
'firefox_dev' : {'fg': '#7c8fa4', 'bg': '#0e1011', 'colors': ['#002831', '#e63853', '#5eb83c', '#a57706', '#359ddf', '#d75cff', '#4b73a2', '#dcdcdc', '#001e27', '#e1003f', '#1d9000', '#cd9409', '#006fc0', '#a200da', '#005794', '#e2e2e2']},
'firewatch' : {'fg': '#9ba2b2', 'bg': '#1e2027', 'colors': ['#585f6d', '#d95360', '#5ab977', '#dfb563', '#4d89c4', '#d55119', '#44a8b6', '#e6e5ff', '#585f6d', '#d95360', '#5ab977', '#dfb563', '#4c89c5', '#d55119', '#44a8b6', '#e6e5ff']},
'fish_tank' : {'fg': '#ecf0fe', 'bg': '#232537', 'colors': ['#03073c', '#c6004a', '#acf157', '#fecd5e', '#525fb8', '#986f82', '#968763', '#ecf0fc', '#6c5b30', '#da4b8a', '#dbffa9', '#fee6a9', '#b2befa', '#fda5cd', '#a5bd86', '#f6ffec']},
'flat' : {'fg': '#2cc55d', 'bg': '#002240', 'colors': ['#222d3f', '#a82320', '#32a548', '#e58d11', '#3167ac', '#781aa0', '#2c9370', '#b0b6ba', '#212c3c', '#d4312e', '#2d9440', '#e5be0c', '#3c7dd2', '#8230a7', '#35b387', '#e7eced']},
'flatland' : {'fg': '#b8dbef', 'bg': '#1d1f21', 'colors': ['#1d1d19', '#f18339', '#9fd364', '#f4ef6d', '#5096be', '#695abc', '#d63865', '#ffffff', '#1d1d19', '#d22a24', '#a7d42c', '#ff8949', '#61b9d0', '#695abc', '#d63865', '#ffffff']},
'flexoki_dark' : {'fg': '#cecdc3', 'bg': '#100f0f', 'colors': ['#100f0f', '#d14d41', '#879a39', '#d0a215', '#4385be', '#ce5d97', '#3aa99f', '#878580', '#575653', '#af3029', '#66800b', '#ad8301', '#205ea6', '#a02f6f', '#24837b', '#cecdc3']},
'flexoki_light' : {'fg': '#100f0f', 'bg': '#fffcf0', 'colors': ['#100f0f', '#af3029', '#66800b', '#ad8301', '#205ea6', '#a02f6f', '#24837b', '#6f6e69', '#b7b5ac', '#d14d41', '#879a39', '#d0a215', '#4385be', '#ce5d97', '#3aa99f', '#cecdc3']},
'floraverse' : {'fg': '#dbd1b9', 'bg': '#0e0d15', 'colors': ['#08002e', '#64002c', '#5d731a', '#cd751c', '#1d6da1', '#b7077e', '#42a38c', '#f3e0b8', '#331e4d', '#d02063', '#b4ce59', '#fac357', '#40a4cf', '#f12aae', '#62caa8', '#fff5db']},
'forest_blue' : {'fg': '#e2d8cd', 'bg': '#051519', 'colors': ['#333333', '#f8818e', '#92d3a2', '#1a8e63', '#8ed0ce', '#5e468c', '#31658c', '#e2d8cd', '#3d3d3d', '#fb3d66', '#6bb48d', '#30c85a', '#39a7a2', '#7e62b3', '#6096bf', '#e2d8cd']},
'framer' : {'fg': '#777777', 'bg': '#111111', 'colors': ['#141414', '#ff5555', '#98ec65', '#ffcc33', '#00aaff', '#aa88ff', '#88ddff', '#cccccc', '#414141', '#ff8888', '#b6f292', '#ffd966', '#33bbff', '#cebbff', '#bbecff', '#ffffff']},
'front_end_delight' : {'fg': '#adadad', 'bg': '#1b1c1d', 'colors': ['#242526', '#f8511b', '#565747', '#fa771d', '#2c70b7', '#f02e4f', '#3ca1a6', '#adadad', '#5fac6d', '#f74319', '#74ec4c', '#fdc325', '#3393ca', '#e75e4f', '#4fbce6', '#8c735b']},
'fun_forrest' : {'fg': '#dec165', 'bg': '#251200', 'colors': ['#000000', '#d6262b', '#919c00', '#be8a13', '#4699a3', '#8d4331', '#da8213', '#ddc265', '#7f6a55', '#e55a1c', '#bfc65a', '#ffcb1b', '#7cc9cf', '#d26349', '#e6a96b', '#ffeaa3']},
'galaxy' : {'fg': '#ffffff', 'bg': '#1d2837', 'colors': ['#000000', '#f9555f', '#21b089', '#fef02a', '#589df6', '#944d95', '#1f9ee7', '#bbbbbb', '#555555', '#fa8c8f', '#35bb9a', '#ffff55', '#589df6', '#e75699', '#3979bc', '#ffffff']},
'galizur' : {'fg': '#ddeeff', 'bg': '#071317', 'colors': ['#223344', '#aa1122', '#33aa11', '#ccaa22', '#2255cc', '#7755aa', '#22bbdd', '#8899aa', '#556677', '#ff1133', '#33ff11', '#ffdd33', '#3377ff', '#aa77ff', '#33ddff', '#bbccdd']},
'ghostty_default_style_dark' : {'fg': '#ffffff', 'bg': '#292c33', 'colors': ['#1d1f21', '#bf6b69', '#b7bd73', '#e9c880', '#88a1bb', '#ad95b8', '#95bdb7', '#c5c8c6', '#666666', '#c55757', '#bcc95f', '#e1c65e', '#83a5d6', '#bc99d4', '#83beb1', '#eaeaea']},
'git_hub_dark' : {'fg': '#8b949e', 'bg': '#101216', 'colors': ['#000000', '#f78166', '#56d364', '#e3b341', '#6ca4f8', '#db61a2', '#2b7489', '#ffffff', '#4d4d4d', '#f78166', '#56d364', '#e3b341', '#6ca4f8', '#db61a2', '#2b7489', '#ffffff']},
'git_hub_dark_colorblind' : {'fg': '#c9d1d9', 'bg': '#0d1117', 'colors': ['#484f58', '#ec8e2c', '#58a6ff', '#d29922', '#58a6ff', '#bc8cff', '#39c5cf', '#b1bac4', '#6e7681', '#fdac54', '#79c0ff', '#e3b341', '#79c0ff', '#d2a8ff', '#56d4dd', '#ffffff']},
'git_hub_dark_default' : {'fg': '#e6edf3', 'bg': '#0d1117', 'colors': ['#484f58', '#ff7b72', '#3fb950', '#d29922', '#58a6ff', '#bc8cff', '#39c5cf', '#b1bac4', '#6e7681', '#ffa198', '#56d364', '#e3b341', '#79c0ff', '#d2a8ff', '#56d4dd', '#ffffff']},
'git_hub_dark_dimmed' : {'fg': '#adbac7', 'bg': '#22272e', 'colors': ['#545d68', '#f47067', '#57ab5a', '#c69026', '#539bf5', '#b083f0', '#39c5cf', '#909dab', '#636e7b', '#ff938a', '#6bc46d', '#daaa3f', '#6cb6ff', '#dcbdfb', '#56d4dd', '#cdd9e5']},
'git_hub_dark_high_contrast' : {'fg': '#f0f3f6', 'bg': '#0a0c10', 'colors': ['#7a828e', '#ff9492', '#26cd4d', '#f0b72f', '#71b7ff', '#cb9eff', '#39c5cf', '#d9dee3', '#9ea7b3', '#ffb1af', '#4ae168', '#f7c843', '#91cbff', '#dbb7ff', '#56d4dd', '#ffffff']},
'git_hub_light_colorblind' : {'fg': '#24292f', 'bg': '#ffffff', 'colors': ['#24292f', '#b35900', '#0550ae', '#4d2d00', '#0969da', '#8250df', '#1b7c83', '#6e7781', '#57606a', '#8a4600', '#0969da', '#633c01', '#218bff', '#a475f9', '#3192aa', '#8c959f']},
'git_hub_light_default' : {'fg': '#1f2328', 'bg': '#ffffff', 'colors': ['#24292f', '#cf222e', '#116329', '#4d2d00', '#0969da', '#8250df', '#1b7c83', '#6e7781', '#57606a', '#a40e26', '#1a7f37', '#633c01', '#218bff', '#a475f9', '#3192aa', '#8c959f']},
'git_hub_light_high_contrast' : {'fg': '#0e1116', 'bg': '#ffffff', 'colors': ['#0e1116', '#a0111f', '#024c1a', '#3f2200', '#0349b4', '#622cbc', '#1b7c83', '#66707b', '#4b535d', '#86061d', '#055d20', '#4e2c00', '#1168e3', '#844ae7', '#3192aa', '#88929d']},
'git_lab_dark' : {'fg': '#ffffff', 'bg': '#28262b', 'colors': ['#000000', '#f57f6c', '#52b87a', '#d99530', '#7fb6ed', '#f88aaf', '#32c5d2', '#ffffff', '#666666', '#fcb5aa', '#91d4a8', '#e9be74', '#498dd1', '#fcacc5', '#5edee3', '#ffffff']},
'git_lab_dark_grey' : {'fg': '#ffffff', 'bg': '#222222', 'colors': ['#000000', '#f57f6c', '#52b87a', '#d99530', '#7fb6ed', '#f88aaf', '#32c5d2', '#ffffff', '#666666', '#fcb5aa', '#91d4a8', '#e9be74', '#498dd1', '#fcacc5', '#5edee3', '#ffffff']},
'git_lab_light' : {'fg': '#303030', 'bg': '#fafaff', 'colors': ['#303030', '#a31700', '#0a7f3d', '#af551d', '#006cd8', '#583cac', '#00798a', '#303030', '#303030', '#a31700', '#0a7f3d', '#af551d', '#006cd8', '#583cac', '#00798a', '#303030']},
'github' : {'fg': '#3e3e3e', 'bg': '#f4f4f4', 'colors': ['#3e3e3e', '#970b16', '#07962a', '#f8eec7', '#003e8a', '#e94691', '#89d1ec', '#ffffff', '#666666', '#de0000', '#87d5a2', '#f1d007', '#2e6cba', '#ffa29f', '#1cfafe', '#ffffff']},
'glacier' : {'fg': '#ffffff', 'bg': '#0c1115', 'colors': ['#2e343c', '#bd0f2f', '#35a770', '#fb9435', '#1f5872', '#bd2523', '#778397', '#ffffff', '#404a55', '#bd0f2f', '#49e998', '#fddf6e', '#2a8bc1', '#ea4727', '#a0b6d3', '#ffffff']},
'grape' : {'fg': '#9f9fa1', 'bg': '#171423', 'colors': ['#2d283f', '#ed2261', '#1fa91b', '#8ddc20', '#487df4', '#8d35c9', '#3bdeed', '#9e9ea0', '#59516a', '#f0729a', '#53aa5e', '#b2dc87', '#a9bcec', '#ad81c2', '#9de3eb', '#a288f7']},
'grass' : {'fg': '#fff0a5', 'bg': '#13773d', 'colors': ['#000000', '#bb0000', '#00bb00', '#e7b000', '#0000a3', '#950062', '#00bbbb', '#bbbbbb', '#555555', '#bb0000', '#00bb00', '#e7b000', '#0000bb', '#ff55ff', '#55ffff', '#ffffff']},
'grey_green' : {'fg': '#ffffff', 'bg': '#002a1a', 'colors': ['#000000', '#fe1414', '#74ff00', '#f1ff01', '#00deff', '#ff00f0', '#00ffbc', '#ffffff', '#666666', '#ff3939', '#00ff44', '#ffd100', '#00afff', '#ff008a', '#00ffd3', '#f5ecec']},
'gruber_darker' : {'fg': '#e4e4e4', 'bg': '#181818', 'colors': ['#181818', '#f43841', '#73d936', '#ffdd33', '#96a6c8', '#9e95c7', '#95a99f', '#e4e4e4', '#52494e', '#ff4f58', '#73d936', '#ffdd33', '#96a6c8', '#afafd7', '#95a99f', '#f5f5f5']},
'gruvbox_dark' : {'fg': '#ebdbb2', 'bg': '#282828', 'colors': ['#282828', '#cc241d', '#98971a', '#d79921', '#458588', '#b16286', '#689d6a', '#a89984', '#928374', '#fb4934', '#b8bb26', '#fabd2f', '#83a598', '#d3869b', '#8ec07c', '#ebdbb2']},
'gruvbox_dark_hard' : {'fg': '#ebdbb2', 'bg': '#1d2021', 'colors': ['#1d2021', '#cc241d', '#98971a', '#d79921', '#458588', '#b16286', '#689d6a', '#a89984', '#928374', '#fb4934', '#b8bb26', '#fabd2f', '#83a598', '#d3869b', '#8ec07c', '#ebdbb2']},
'gruvbox_light' : {'fg': '#282828', 'bg': '#fbf1c7', 'colors': ['#fbf1c7', '#9d0006', '#79740e', '#b57614', '#076678', '#8f3f71', '#427b58', '#3c3836', '#9d8374', '#cc241d', '#98971a', '#d79921', '#458588', '#b16186', '#689d69', '#7c6f64']},
'gruvbox_light_hard' : {'fg': '#282828', 'bg': '#f8f4d6', 'colors': ['#f8f4d6', '#9d0006', '#79740e', '#b57614', '#076678', '#8f3f71', '#427b58', '#3c3836', '#9d8374', '#cc241d', '#98971a', '#d79921', '#458588', '#b16186', '#689d69', '#7c6f64']},
'gruvbox_material' : {'fg': '#d4be98', 'bg': '#1d2021', 'colors': ['#141617', '#ea6926', '#c1d041', '#eecf75', '#6da3ec', '#fd9bc1', '#fe9d6e', '#ffffff', '#000000', '#d3573b', '#c1d041', '#eecf75', '#2c86ff', '#fd9bc1', '#92a5df', '#ffffff']},
'guezwhoz' : {'fg': '#d0d0d0', 'bg': '#1c1c1c', 'colors': ['#080808', '#ff5f5f', '#87d7af', '#d7d787', '#5fafd7', '#afafff', '#5fd7d7', '#dadada', '#8a8a8a', '#d75f5f', '#afd7af', '#d7d7af', '#87afd7', '#afafd7', '#87d7d7', '#dadada']},
'ha_x0r_blue' : {'fg': '#11b7ff', 'bg': '#010515', 'colors': ['#010921', '#10b6ff', '#10b6ff', '#10b6ff', '#10b6ff', '#10b6ff', '#10b6ff', '#fafafa', '#080117', '#00b3f7', '#00b3f7', '#00b3f7', '#00b3f7', '#00b3f7', '#00b3f7', '#fefefe']},
'ha_x0r_gr33n' : {'fg': '#16b10e', 'bg': '#020f01', 'colors': ['#001f0b', '#15d00d', '#15d00d', '#15d00d', '#15d00d', '#15d00d', '#15d00d', '#fafafa', '#001510', '#19e20e', '#19e20e', '#19e20e', '#19e20e', '#19e20e', '#19e20e', '#fefefe']},
'ha_x0r_r3d' : {'fg': '#b10e0e', 'bg': '#200101', 'colors': ['#1f0000', '#b00d0d', '#b00d0d', '#b00d0d', '#b00d0d', '#b00d0d', '#b00d0d', '#fafafa', '#150000', '#ff1111', '#ff1010', '#ff1010', '#ff1010', '#ff1010', '#ff1010', '#fefefe']},
'hacktober' : {'fg': '#c9c9c9', 'bg': '#141414', 'colors': ['#191918', '#b34538', '#587744', '#d08949', '#206ec5', '#864651', '#ac9166', '#f1eee7', '#2c2b2a', '#b33323', '#42824a', '#c75a22', '#5389c5', '#e795a5', '#ebc587', '#ffffff']},
'hardcore' : {'fg': '#a0a0a0', 'bg': '#121212', 'colors': ['#1b1d1e', '#f92672', '#a6e22e', '#fd971f', '#66d9ef', '#9e6ffe', '#5e7175', '#ccccc6', '#505354', '#ff669d', '#beed5f', '#e6db74', '#66d9ef', '#9e6ffe', '#a3babf', '#f8f8f2']},
'harper' : {'fg': '#a8a49d', 'bg': '#010101', 'colors': ['#010101', '#f8b63f', '#7fb5e1', '#d6da25', '#489e48', '#b296c6', '#f5bfd7', '#a8a49d', '#726e6a', '#f8b63f', '#7fb5e1', '#d6da25', '#489e48', '#b296c6', '#f5bfd7', '#fefbea']},
'havn_daggry' : {'fg': '#3e4a77', 'bg': '#f8f9fb', 'colors': ['#212840', '#8f564b', '#5c705b', '#b36f00', '#40567a', '#775d93', '#8a5a7e', '#d7dbea', '#212840', '#bd533e', '#79957b', '#f3b550', '#6988bc', '#7b7393', '#a4879c', '#d7dbea']},
'havn_skumring' : {'fg': '#d7dbea', 'bg': '#121521', 'colors': ['#262c45', '#d96048', '#7cab7f', '#eeb64e', '#5d6bef', '#7a729a', '#ca8cbe', '#dde0ed', '#212840', '#c47768', '#8f9d90', '#e4c693', '#5d85c6', '#967de7', '#c57eb3', '#fdf6e3']},
'heeler' : {'fg': '#fdfdfd', 'bg': '#211f44', 'colors': ['#000000', '#d3573b', '#c1d041', '#eecf75', '#6da3ec', '#fd9bc1', '#fe9d6e', '#ffffff', '#000000', '#d3573b', '#c1d041', '#eecf75', '#2c86ff', '#fd9bc1', '#92a5df', '#ffffff']},
'highway' : {'fg': '#ededed', 'bg': '#222225', 'colors': ['#000000', '#d00e18', '#138034', '#ffcb3e', '#006bb3', '#6b2775', '#384564', '#ededed', '#5d504a', '#f07e18', '#b1d130', '#fff120', '#4fc2fd', '#de0071', '#5d504a', '#ffffff']},
'hipster_green' : {'fg': '#84c138', 'bg': '#100b05', 'colors': ['#000000', '#b6214a', '#00a600', '#bfbf00', '#246eb2', '#b200b2', '#00a6b2', '#bfbfbf', '#666666', '#e50000', '#86a93e', '#e5e500', '#0000ff', '#e500e5', '#00e5e5', '#e5e5e5']},
'hivacruz' : {'fg': '#ede4e4', 'bg': '#132638', 'colors': ['#202746', '#c94922', '#ac9739', '#c08b30', '#3d8fd1', '#6679cc', '#22a2c9', '#979db4', '#6b7394', '#c76b29', '#73ad43', '#5e6687', '#898ea4', '#dfe2f1', '#9c637a', '#f5f7ff']},
'homebrew' : {'fg': '#00ff00', 'bg': '#000000', 'colors': ['#000000', '#990000', '#00a600', '#999900', '#0000b2', '#b200b2', '#00a6b2', '#bfbfbf', '#666666', '#e50000', '#00d900', '#e5e500', '#0000ff', '#e500e5', '#00e5e5', '#e5e5e5']},
'hopscotch' : {'fg': '#b9b5b8', 'bg': '#322931', 'colors': ['#322931', '#dd464c', '#8fc13e', '#fdcc59', '#1290bf', '#c85e7c', '#149b93', '#b9b5b8', '#797379', '#fd8b19', '#433b42', '#5c545b', '#989498', '#d5d3d5', '#b33508', '#ffffff']},
'hopscotch256' : {'fg': '#b9b5b8', 'bg': '#322931', 'colors': ['#322931', '#dd464c', '#8fc13e', '#fdcc59', '#1290bf', '#c85e7c', '#149b93', '#b9b5b8', '#797379', '#dd464c', '#8fc13e', '#fdcc59', '#1290bf', '#c85e7c', '#149b93', '#ffffff']},
'horizon' : {'fg': '#d5d8da', 'bg': '#1c1e26', 'colors': ['#000000', '#e95678', '#29d398', '#fab795', '#26bbd9', '#ee64ac', '#59e1e3', '#e5e5e5', '#666666', '#ec6a88', '#3fdaa4', '#fbc3a7', '#3fc4de', '#f075b5', '#6be4e6', '#e5e5e5']},
'horizon_bright' : {'fg': '#16161c', 'bg': '#fbf0ee', 'colors': ['#16161c', '#e95678', '#29d398', '#fab795', '#26bbd9', '#ee64ae', '#59e3e3', '#fdf0ed', '#1a1c23', '#ec6a88', '#3fdaa4', '#fbc3a7', '#3fc6de', '#f075b7', '#6be6e6', '#fff3f0']},
'hurtado' : {'fg': '#dbdbdb', 'bg': '#000000', 'colors': ['#575757', '#ff1b00', '#a5e055', '#fbe74a', '#496487', '#fd5ff1', '#86e9fe', '#cbcccb', '#262626', '#d51d00', '#a5df55', '#fbe84a', '#89beff', '#c001c1', '#86eafe', '#dbdbdb']},
'hybrid' : {'fg': '#b7bcba', 'bg': '#161719', 'colors': ['#2a2e33', '#b84d51', '#b3bf5a', '#e4b55e', '#6e90b0', '#a17eac', '#7fbfb4', '#b5b9b6', '#1d1f22', '#8d2e32', '#798431', '#e58a50', '#4b6b88', '#6e5079', '#4d7b74', '#5a626a']},
'i_term2_dark_background' : {'fg': '#c7c7c7', 'bg': '#000000', 'colors': ['#000000', '#c91b00', '#00c200', '#c7c400', '#0225c7', '#ca30c7', '#00c5c7', '#c7c7c7', '#686868', '#ff6e67', '#5ffa68', '#fffc67', '#6871ff', '#ff77ff', '#60fdff', '#ffffff']},
'i_term2_default' : {'fg': '#ffffff', 'bg': '#000000', 'colors': ['#000000', '#c91b00', '#00c200', '#c7c400', '#2225c4', '#ca30c7', '#00c5c7', '#ffffff', '#686868', '#ff6e67', '#5ffa68', '#fffc67', '#6871ff', '#ff77ff', '#60fdff', '#ffffff']},
'i_term2_light_background' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#000000', '#c91b00', '#00c200', '#c7c400', '#0225c7', '#ca30c7', '#00c5c7', '#c7c7c7', '#686868', '#ff6e67', '#5ffa68', '#fffc67', '#6871ff', '#ff77ff', '#60fdff', '#ffffff']},
'i_term2_pastel_dark_background' : {'fg': '#c7c7c7', 'bg': '#000000', 'colors': ['#626262', '#ff8373', '#b4fb73', '#fffdc3', '#a5d5fe', '#ff90fe', '#d1d1fe', '#f1f1f1', '#8f8f8f', '#ffc4be', '#d6fcba', '#fffed5', '#c2e3ff', '#ffb2fe', '#e6e6fe', '#ffffff']},
'i_term2_smoooooth' : {'fg': '#dcdcdc', 'bg': '#15191f', 'colors': ['#14191e', '#b43c2a', '#00c200', '#c7c400', '#2744c7', '#c040be', '#00c5c7', '#c7c7c7', '#686868', '#dd7975', '#58e790', '#ece100', '#a7abf2', '#e17ee1', '#60fdff', '#ffffff']},
'i_term2_solarized_dark' : {'fg': '#839496', 'bg': '#002b36', 'colors': ['#073642', '#dc322f', '#859900', '#b58900', '#268bd2', '#d33682', '#2aa198', '#eee8d5', '#002b36', '#cb4b16', '#586e75', '#657b83', '#839496', '#6c71c4', '#93a1a1', '#fdf6e3']},
'i_term2_solarized_light' : {'fg': '#657b83', 'bg': '#fdf6e3', 'colors': ['#073642', '#dc322f', '#859900', '#b58900', '#268bd2', '#d33682', '#2aa198', '#eee8d5', '#002b36', '#cb4b16', '#586e75', '#657b83', '#839496', '#6c71c4', '#93a1a1', '#fdf6e3']},
'i_term2_tango_dark' : {'fg': '#ffffff', 'bg': '#000000', 'colors': ['#000000', '#d81e00', '#5ea702', '#cfae00', '#427ab3', '#89658e', '#00a7aa', '#dbded8', '#686a66', '#f54235', '#99e343', '#fdeb61', '#84b0d8', '#bc94b7', '#37e6e8', '#f1f1f0']},
'i_term2_tango_light' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#000000', '#d81e00', '#5ea702', '#cfae00', '#427ab3', '#89658e', '#00a7aa', '#dbded8', '#686a66', '#f54235', '#99e343', '#fdeb61', '#84b0d8', '#bc94b7', '#37e6e8', '#f1f1f0']},
'ic_green_ppl' : {'fg': '#e0f1dc', 'bg': '#2c2c2c', 'colors': ['#014401', '#ff2736', '#41a638', '#76a831', '#2ec3b9', '#50a096', '#3ca078', '#e6fef2', '#035c03', '#b4fa5c', '#aefb86', '#dafa87', '#2efaeb', '#50fafa', '#3cfac8', '#e0f1dc']},
'ic_orange_ppl' : {'fg': '#ffcb83', 'bg': '#262626', 'colors': ['#000000', '#c13900', '#a4a900', '#caaf00', '#bd6d00', '#fc5e00', '#f79500', '#ffc88a', '#6a4f2a', '#ff8c68', '#f6ff40', '#ffe36e', '#ffbe55', '#fc874f', '#c69752', '#fafaff']},
'iceberg_dark' : {'fg': '#c6c8d1', 'bg': '#161821', 'colors': ['#1e2132', '#e27878', '#b4be82', '#e2a478', '#84a0c6', '#a093c7', '#89b8c2', '#c6c8d1', '#6b7089', '#e98989', '#c0ca8e', '#e9b189', '#91acd1', '#ada0d3', '#95c4ce', '#d2d4de']},
'iceberg_light' : {'fg': '#33374c', 'bg': '#e8e9ec', 'colors': ['#dcdfe7', '#cc517a', '#668e3d', '#c57339', '#2d539e', '#7759b4', '#3f83a6', '#33374c', '#8389a3', '#cc3768', '#598030', '#b6662d', '#22478e', '#6845ad', '#327698', '#262a3f']},
'idea' : {'fg': '#adadad', 'bg': '#202020', 'colors': ['#adadad', '#fc5256', '#98b61c', '#ccb444', '#437ee7', '#9d74b0', '#248887', '#181818', '#ffffff', '#fc7072', '#98b61c', '#ffff0b', '#6c9ced', '#fc7eff', '#248887', '#181818']},
'idle_toes' : {'fg': '#ffffff', 'bg': '#323232', 'colors': ['#323232', '#d25252', '#7fe173', '#ffc66d', '#4099ff', '#f680ff', '#bed6ff', '#eeeeec', '#535353', '#f07070', '#9dff91', '#ffe48b', '#5eb7f7', '#ff9dff', '#dcf4ff', '#ffffff']},
'ir_black' : {'fg': '#f1f1f1', 'bg': '#000000', 'colors': ['#4f4f4f', '#fa6c60', '#a8ff60', '#fffeb7', '#96cafe', '#fa73fd', '#c6c5fe', '#efedef', '#7b7b7b', '#fcb6b0', '#cfffab', '#ffffcc', '#b5dcff', '#fb9cfe', '#e0e0fe', '#ffffff']},
'jackie_brown' : {'fg': '#ffcc2f', 'bg': '#2c1d16', 'colors': ['#2c1d16', '#ef5734', '#2baf2b', '#bebf00', '#246eb2', '#d05ec1', '#00acee', '#bfbfbf', '#666666', '#e50000', '#86a93e', '#e5e500', '#0000ff', '#e500e5', '#00e5e5', '#e5e5e5']},
'japanesque' : {'fg': '#f7f6ec', 'bg': '#1e1e1e', 'colors': ['#343935', '#cf3f61', '#7bb75b', '#e9b32a', '#4c9ad4', '#a57fc4', '#389aad', '#fafaf6', '#595b59', '#d18fa6', '#767f2c', '#78592f', '#135979', '#604291', '#76bbca', '#b2b5ae']},
'jellybeans' : {'fg': '#dedede', 'bg': '#121212', 'colors': ['#929292', '#e27373', '#94b979', '#ffba7b', '#97bedc', '#e1c0fa', '#00988e', '#dedede', '#bdbdbd', '#ffa1a1', '#bddeab', '#ffdca0', '#b1d8f6', '#fbdaff', '#1ab2a8', '#ffffff']},
'jet_brains_darcula' : {'fg': '#adadad', 'bg': '#202020', 'colors': ['#000000', '#fa5355', '#126e00', '#c2c300', '#4581eb', '#fa54ff', '#33c2c1', '#adadad', '#555555', '#fb7172', '#67ff4f', '#ffff00', '#6d9df1', '#fb82ff', '#60d3d1', '#eeeeee']},
'jubi' : {'fg': '#c3d3de', 'bg': '#262b33', 'colors': ['#3b3750', '#cf7b98', '#90a94b', '#6ebfc0', '#576ea6', '#bc4f68', '#75a7d2', '#c3d3de', '#a874ce', '#de90ab', '#bcdd61', '#87e9ea', '#8c9fcd', '#e16c87', '#b7c9ef', '#d5e5f1']},
'kanagawa_dragon' : {'fg': '#c8c093', 'bg': '#181616', 'colors': ['#0d0c0c', '#c4746e', '#8a9a7b', '#c4b28a', '#8ba4b0', '#a292a3', '#8ea4a2', '#c8c093', '#a6a69c', '#e46876', '#87a987', '#e6c384', '#7fb4ca', '#938aa9', '#7aa89f', '#c5c9c5']},
'kanagawa_wave' : {'fg': '#dcd7ba', 'bg': '#1f1f28', 'colors': ['#090618', '#c34043', '#76946a', '#c0a36e', '#7e9cd8', '#957fb8', '#6a9589', '#c8c093', '#727169', '#e82424', '#98bb6c', '#e6c384', '#7fb4ca', '#938aa9', '#7aa89f', '#dcd7ba']},
'kanagawabones' : {'fg': '#ddd8bb', 'bg': '#1f1f28', 'colors': ['#1f1f28', '#e46a78', '#98bc6d', '#e5c283', '#7eb3c9', '#957fb8', '#7eb3c9', '#ddd8bb', '#3c3c51', '#ec818c', '#9ec967', '#f1c982', '#7bc2df', '#a98fd2', '#7bc2df', '#a8a48d']},
'kibble' : {'fg': '#f7f7f7', 'bg': '#0e100a', 'colors': ['#4d4d4d', '#c70031', '#29cf13', '#d8e30e', '#3449d1', '#8400ff', '#0798ab', '#e2d1e3', '#5a5a5a', '#f01578', '#6ce05c', '#f3f79e', '#97a4f7', '#c495f0', '#68f2e0', '#ffffff']},
'kolorit' : {'fg': '#efecec', 'bg': '#1d1a1e', 'colors': ['#1d1a1e', '#ff5b82', '#47d7a1', '#e8e562', '#5db4ee', '#da6cda', '#57e9eb', '#ededed', '#1d1a1e', '#ff5b82', '#47d7a1', '#e8e562', '#5db4ee', '#da6cda', '#57e9eb', '#ededed']},
'konsolas' : {'fg': '#c8c1c1', 'bg': '#060606', 'colors': ['#000000', '#aa1717', '#18b218', '#ebae1f', '#2323a5', '#ad1edc', '#42b0c8', '#c8c1c1', '#7b716e', '#ff4141', '#5fff5f', '#ffff55', '#4b4bff', '#ff54ff', '#69ffff', '#ffffff']},
'kurokula' : {'fg': '#ddd0c4', 'bg': '#141515', 'colors': ['#333333', '#b66056', '#85b1a9', '#dbbb43', '#6890d7', '#887aa3', '#837369', '#ddd0c4', '#515151', '#ffc663', '#c1ffae', '#fff700', '#a1d9ff', '#a994ff', '#f9cfb9', '#ffffff']},
'lab_fox' : {'fg': '#ffffff', 'bg': '#2e2e2e', 'colors': ['#2e2e2e', '#fc6d26', '#3eb383', '#fca121', '#db3b21', '#380d75', '#6e49cb', '#ffffff', '#464646', '#ff6517', '#53eaa8', '#fca013', '#db501f', '#441090', '#7d53e7', '#ffffff']},
'laser' : {'fg': '#f106e3', 'bg': '#030d18', 'colors': ['#626262', '#ff8373', '#b4fb73', '#09b4bd', '#fed300', '#ff90fe', '#d1d1fe', '#f1f1f1', '#8f8f8f', '#ffc4be', '#d6fcba', '#fffed5', '#f92883', '#ffb2fe', '#e6e7fe', '#ffffff']},
'later_this_evening' : {'fg': '#959595', 'bg': '#222222', 'colors': ['#2b2b2b', '#d45a60', '#afba67', '#e5d289', '#a0bad6', '#c092d6', '#91bfb7', '#3c3d3d', '#454747', '#d3232f', '#aabb39', '#e5be39', '#6699d6', '#ab53d6', '#5fc0ae', '#c1c2c2']},
'lavandula' : {'fg': '#736e7d', 'bg': '#050014', 'colors': ['#230046', '#7d1625', '#337e6f', '#7f6f49', '#4f4a7f', '#5a3f7f', '#58777f', '#736e7d', '#372d46', '#e05167', '#52e0c4', '#e0c386', '#8e87e0', '#a776e0', '#9ad4e0', '#8c91fa']},
'liquid_carbon' : {'fg': '#afc2c2', 'bg': '#303030', 'colors': ['#000000', '#ff3030', '#559a70', '#ccac00', '#0099cc', '#cc69c8', '#7ac4cc', '#bccccc', '#000000', '#ff3030', '#559a70', '#ccac00', '#0099cc', '#cc69c8', '#7ac4cc', '#bccccc']},
'liquid_carbon_transparent' : {'fg': '#afc2c2', 'bg': '#000000', 'colors': ['#000000', '#ff3030', '#559a70', '#ccac00', '#0099cc', '#cc69c8', '#7ac4cc', '#bccccc', '#000000', '#ff3030', '#559a70', '#ccac00', '#0099cc', '#cc69c8', '#7ac4cc', '#bccccc']},
'liquid_carbon_transparent_inverse' : {'fg': '#afc2c2', 'bg': '#000000', 'colors': ['#bccccd', '#ff3030', '#559a70', '#ccac00', '#0099cc', '#cc69c8', '#7ac4cc', '#000000', '#ffffff', '#ff3030', '#559a70', '#ccac00', '#0099cc', '#cc69c8', '#7ac4cc', '#000000']},
'lovelace' : {'fg': '#fdfdfd', 'bg': '#1d1f28', 'colors': ['#282a36', '#f37f97', '#5adecd', '#f2a272', '#8897f4', '#c574dd', '#79e6f3', '#fdfdfd', '#414458', '#ff4971', '#18e3c8', '#ff8037', '#556fff', '#b043d1', '#3fdcee', '#bebec1']},
'man_page' : {'fg': '#000000', 'bg': '#fef49c', 'colors': ['#000000', '#cc0000', '#00a600', '#999900', '#0000b2', '#b200b2', '#00a6b2', '#cccccc', '#666666', '#e50000', '#00d900', '#e5e500', '#0000ff', '#e500e5', '#00e5e5', '#e5e5e5']},
'mariana' : {'fg': '#d8dee9', 'bg': '#343d46', 'colors': ['#000000', '#ec5f66', '#99c794', '#f9ae58', '#6699cc', '#c695c6', '#5fb4b4', '#f7f7f7', '#333333', '#f97b58', '#acd1a8', '#fac761', '#85add6', '#d8b6d8', '#82c4c4', '#ffffff']},
'material' : {'fg': '#232322', 'bg': '#eaeaea', 'colors': ['#212121', '#b7141f', '#457b24', '#f6981e', '#134eb2', '#560088', '#0e717c', '#efefef', '#424242', '#e83b3f', '#7aba3a', '#ffea2e', '#54a4f3', '#aa4dbc', '#26bbd1', '#d9d9d9']},
'material_dark' : {'fg': '#e5e5e5', 'bg': '#232322', 'colors': ['#212121', '#b7141f', '#457b24', '#f6981e', '#134eb2', '#560088', '#0e717c', '#efefef', '#424242', '#e83b3f', '#7aba3a', '#ffea2e', '#54a4f3', '#aa4dbc', '#26bbd1', '#d9d9d9']},
'material_darker' : {'fg': '#eeffff', 'bg': '#212121', 'colors': ['#000000', '#ff5370', '#c3e88d', '#ffcb6b', '#82aaff', '#c792ea', '#89ddff', '#ffffff', '#545454', '#ff5370', '#c3e88d', '#ffcb6b', '#82aaff', '#c792ea', '#89ddff', '#ffffff']},
'material_design_colors' : {'fg': '#e7ebed', 'bg': '#1d262a', 'colors': ['#435b67', '#fc3841', '#5cf19e', '#fed032', '#37b6ff', '#fc226e', '#59ffd1', '#ffffff', '#a1b0b8', '#fc746d', '#adf7be', '#fee16c', '#70cfff', '#fc669b', '#9affe6', '#ffffff']},
'material_ocean' : {'fg': '#8f93a2', 'bg': '#0f111a', 'colors': ['#546e7a', '#ff5370', '#c3e88d', '#ffcb6b', '#82aaff', '#c792ea', '#89ddff', '#ffffff', '#546e7a', '#ff5370', '#c3e88d', '#ffcb6b', '#82aaff', '#c792ea', '#89ddff', '#ffffff']},
'mathias' : {'fg': '#bbbbbb', 'bg': '#000000', 'colors': ['#000000', '#e52222', '#a6e32d', '#fc951e', '#c48dff', '#fa2573', '#67d9f0', '#f2f2f2', '#555555', '#ff5555', '#55ff55', '#ffff55', '#5555ff', '#ff55ff', '#55ffff', '#ffffff']},
'matrix' : {'fg': '#426644', 'bg': '#0f191c', 'colors': ['#0f191c', '#23755a', '#82d967', '#ffd700', '#3f5242', '#409931', '#50b45a', '#507350', '#688060', '#2fc079', '#90d762', '#faff00', '#4f7e7e', '#11ff25', '#c1ff8a', '#678c61']},
'medallion' : {'fg': '#cac296', 'bg': '#1d1908', 'colors': ['#000000', '#b64c00', '#7c8b16', '#d3bd26', '#616bb0', '#8c5a90', '#916c25', '#cac29a', '#5e5219', '#ff9149', '#b2ca3b', '#ffe54a', '#acb8ff', '#ffa0ff', '#ffbc51', '#fed698']},
'melange_dark' : {'fg': '#ece1d7', 'bg': '#292522', 'colors': ['#34302c', '#bd8183', '#78997a', '#e49b5d', '#7f91b2', '#b380b0', '#7b9695', '#c1a78e', '#867462', '#d47766', '#85b695', '#ebc06d', '#a3a9ce', '#cf9bc2', '#89b3b6', '#ece1d7']},
'melange_light' : {'fg': '#54433a', 'bg': '#f1f1f1', 'colors': ['#e9e1db', '#c77b8b', '#6e9b72', '#bc5c00', '#7892bd', '#be79bb', '#739797', '#7d6658', '#a98a78', '#bf0021', '#3a684a', '#a06d00', '#465aa4', '#904180', '#3d6568', '#54433a']},
'mellifluous' : {'fg': '#dadada', 'bg': '#1a1a1a', 'colors': ['#1a1a1a', '#d29393', '#b3b393', '#cbaa89', '#a8a1be', '#b39fb0', '#c0af8c', '#dadada', '#5b5b5b', '#c95954', '#828040', '#a6794c', '#5a6599', '#9c6995', '#74a39e', '#ffffff']},
'mellow' : {'fg': '#c9c7cd', 'bg': '#161617', 'colors': ['#27272a', '#f5a191', '#90b99f', '#e6b99d', '#aca1cf', '#e29eca', '#ea83a5', '#c1c0d4', '#353539', '#ffae9f', '#9dc6ac', '#f0c5a9', '#b9aeda', '#ecaad6', '#f591b2', '#cac9dd']},
'miasma' : {'fg': '#c2c2b0', 'bg': '#222222', 'colors': ['#000000', '#685742', '#5f875f', '#b36d43', '#78824b', '#bb7744', '#c9a554', '#d7c483', '#666666', '#685742', '#5f875f', '#b36d43', '#78824b', '#bb7744', '#c9a554', '#d7c483']},
'midnight_in_mojave' : {'fg': '#ffffff', 'bg': '#1e1e1e', 'colors': ['#1e1e1e', '#ff453a', '#32d74b', '#ffd60a', '#0a84ff', '#bf5af2', '#5ac8fa', '#ffffff', '#1e1e1e', '#ff453a', '#32d74b', '#ffd60a', '#0a84ff', '#bf5af2', '#5ac8fa', '#ffffff']},
'mirage' : {'fg': '#a6b2c0', 'bg': '#1b2738', 'colors': ['#011627', '#ff9999', '#85cc95', '#ffd700', '#7fb5ff', '#ddb3ff', '#21c7a8', '#ffffff', '#575656', '#ff9999', '#85cc95', '#ffd700', '#7fb5ff', '#ddb3ff', '#85cc95', '#ffffff']},
'misterioso' : {'fg': '#e1e1e0', 'bg': '#2d3743', 'colors': ['#000000', '#ff4242', '#74af68', '#ffad29', '#338f86', '#9414e6', '#23d7d7', '#e1e1e0', '#555555', '#ff3242', '#74cd68', '#ffb929', '#23d7d7', '#ff37ff', '#00ede1', '#ffffff']},
'molokai' : {'fg': '#bbbbbb', 'bg': '#121212', 'colors': ['#121212', '#fa2573', '#98e123', '#dfd460', '#1080d0', '#8700ff', '#43a8d0', '#bbbbbb', '#555555', '#f6669d', '#b1e05f', '#fff26d', '#00afff', '#af87ff', '#51ceff', '#ffffff']},
'mona_lisa' : {'fg': '#f7d66a', 'bg': '#120b0d', 'colors': ['#351b0e', '#9b291c', '#636232', '#c36e28', '#515c5d', '#9b1d29', '#588056', '#f7d75c', '#874228', '#ff4331', '#b4b264', '#ff9566', '#9eb2b4', '#ff5b6a', '#8acd8f', '#ffe598']},
'monokai_classic' : {'fg': '#fdfff1', 'bg': '#272822', 'colors': ['#272822', '#f92672', '#a6e22e', '#e6db74', '#fd971f', '#ae81ff', '#66d9ef', '#fdfff1', '#6e7066', '#f92672', '#a6e22e', '#e6db74', '#fd971f', '#ae81ff', '#66d9ef', '#fdfff1']},
'monokai_pro' : {'fg': '#fcfcfa', 'bg': '#2d2a2e', 'colors': ['#2d2a2e', '#ff6188', '#a9dc76', '#ffd866', '#fc9867', '#ab9df2', '#78dce8', '#fcfcfa', '#727072', '#ff6188', '#a9dc76', '#ffd866', '#fc9867', '#ab9df2', '#78dce8', '#fcfcfa']},
'monokai_pro_light' : {'fg': '#29242a', 'bg': '#faf4f2', 'colors': ['#faf4f2', '#e14775', '#269d69', '#cc7a0a', '#e16032', '#7058be', '#1c8ca8', '#29242a', '#a59fa0', '#e14775', '#269d69', '#cc7a0a', '#e16032', '#7058be', '#1c8ca8', '#29242a']},
'monokai_pro_light_sun' : {'fg': '#2c232e', 'bg': '#f8efe7', 'colors': ['#f8efe7', '#ce4770', '#218871', '#b16803', '#d4572b', '#6851a2', '#2473b6', '#2c232e', '#a59c9c', '#ce4770', '#218871', '#b16803', '#d4572b', '#6851a2', '#2473b6', '#2c232e']},
'monokai_pro_machine' : {'fg': '#f2fffc', 'bg': '#273136', 'colors': ['#273136', '#ff6d7e', '#a2e57b', '#ffed72', '#ffb270', '#baa0f8', '#7cd5f1', '#f2fffc', '#6b7678', '#ff6d7e', '#a2e57b', '#ffed72', '#ffb270', '#baa0f8', '#7cd5f1', '#f2fffc']},
'monokai_pro_octagon' : {'fg': '#eaf2f1', 'bg': '#282a3a', 'colors': ['#282a3a', '#ff657a', '#bad761', '#ffd76d', '#ff9b5e', '#c39ac9', '#9cd1bb', '#eaf2f1', '#696d77', '#ff657a', '#bad761', '#ffd76d', '#ff9b5e', '#c39ac9', '#9cd1bb', '#eaf2f1']},
'monokai_pro_ristretto' : {'fg': '#fff1f3', 'bg': '#2c2525', 'colors': ['#2c2525', '#fd6883', '#adda78', '#f9cc6c', '#f38d70', '#a8a9eb', '#85dacc', '#fff1f3', '#72696a', '#fd6883', '#adda78', '#f9cc6c', '#f38d70', '#a8a9eb', '#85dacc', '#fff1f3']},
'monokai_pro_spectrum' : {'fg': '#f7f1ff', 'bg': '#222222', 'colors': ['#222222', '#fc618d', '#7bd88f', '#fce566', '#fd9353', '#948ae3', '#5ad4e6', '#f7f1ff', '#69676c', '#fc618d', '#7bd88f', '#fce566', '#fd9353', '#948ae3', '#5ad4e6', '#f7f1ff']},
'monokai_remastered' : {'fg': '#d9d9d9', 'bg': '#0c0c0c', 'colors': ['#1a1a1a', '#f4005f', '#98e024', '#fd971f', '#9d65ff', '#f4005f', '#58d1eb', '#c4c5b5', '#625e4c', '#f4005f', '#98e024', '#e0d561', '#9d65ff', '#f4005f', '#58d1eb', '#f6f6ef']},
'monokai_soda' : {'fg': '#c4c5b5', 'bg': '#1a1a1a', 'colors': ['#1a1a1a', '#f4005f', '#98e024', '#fa8419', '#9d65ff', '#f4005f', '#58d1eb', '#c4c5b5', '#625e4c', '#f4005f', '#98e024', '#e0d561', '#9d65ff', '#f4005f', '#58d1eb', '#f6f6ef']},
'monokai_vivid' : {'fg': '#f9f9f9', 'bg': '#121212', 'colors': ['#121212', '#fa2934', '#98e123', '#fff30a', '#0443ff', '#f800f8', '#01b6ed', '#ffffff', '#838383', '#f6669d', '#b1e05f', '#fff26d', '#0443ff', '#f200f6', '#51ceff', '#ffffff']},
'n0tch2k' : {'fg': '#a0a0a0', 'bg': '#222222', 'colors': ['#383838', '#a95551', '#666666', '#a98051', '#657d3e', '#767676', '#c9c9c9', '#d0b8a3', '#474747', '#a97775', '#8c8c8c', '#a99175', '#98bd5e', '#a3a3a3', '#dcdcdc', '#d8c8bb']},
'neobones_dark' : {'fg': '#c6d5cf', 'bg': '#0f191f', 'colors': ['#0f191f', '#de6e7c', '#90ff6b', '#b77e64', '#8190d4', '#b279a7', '#66a5ad', '#c6d5cf', '#263945', '#e8838f', '#a0ff85', '#d68c67', '#92a0e2', '#cf86c1', '#65b8c1', '#98a39e']},
'neobones_light' : {'fg': '#202e18', 'bg': '#e5ede6', 'colors': ['#e5ede6', '#a8334c', '#567a30', '#944927', '#286486', '#88507d', '#3b8992', '#202e18', '#b3c6b6', '#94253e', '#3f5a22', '#803d1c', '#1d5573', '#7b3b70', '#2b747c', '#415934']},
'neon' : {'fg': '#00fffc', 'bg': '#14161a', 'colors': ['#000000', '#ff3045', '#5ffa74', '#fffc7e', '#0208cb', '#f924e7', '#00fffc', '#c7c7c7', '#686868', '#ff5a5a', '#75ff88', '#fffd96', '#3c40cb', '#f15be5', '#88fffe', '#ffffff']},
'neopolitan' : {'fg': '#ffffff', 'bg': '#271f19', 'colors': ['#000000', '#800000', '#61ce3c', '#fbde2d', '#253b76', '#ff0080', '#8da6ce', '#f8f8f8', '#000000', '#800000', '#61ce3c', '#fbde2d', '#253b76', '#ff0080', '#8da6ce', '#f8f8f8']},
'neutron' : {'fg': '#e6e8ef', 'bg': '#1c1e22', 'colors': ['#23252b', '#b54036', '#5ab977', '#deb566', '#6a7c93', '#a4799d', '#3f94a8', '#e6e8ef', '#23252b', '#b54036', '#5ab977', '#deb566', '#6a7c93', '#a4799d', '#3f94a8', '#ebedf2']},
'night_lion_v1' : {'fg': '#bbbbbb', 'bg': '#000000', 'colors': ['#4c4c4c', '#bb0000', '#5fde8f', '#f3f167', '#276bd8', '#bb00bb', '#00dadf', '#bbbbbb', '#555555', '#ff5555', '#55ff55', '#ffff55', '#5555ff', '#ff55ff', '#55ffff', '#ffffff']},
'night_lion_v2' : {'fg': '#bbbbbb', 'bg': '#171717', 'colors': ['#4c4c4c', '#bb0000', '#04f623', '#f3f167', '#64d0f0', '#ce6fdb', '#00dadf', '#bbbbbb', '#555555', '#ff5555', '#7df71d', '#ffff55', '#62cbe8', '#ff9bf5', '#00ccd8', '#ffffff']},
'night_owlish_light' : {'fg': '#403f53', 'bg': '#ffffff', 'colors': ['#011627', '#d3423e', '#2aa298', '#daaa01', '#4876d6', '#403f53', '#08916a', '#7a8181', '#7a8181', '#f76e6e', '#49d0c5', '#dac26b', '#5ca7e4', '#697098', '#00c990', '#989fb1']},
'nightfox' : {'fg': '#cdcecf', 'bg': '#192330', 'colors': ['#393b44', '#c94f6d', '#81b29a', '#dbc074', '#719cd6', '#9d79d6', '#63cdcf', '#dfdfe0', '#575860', '#d16983', '#8ebaa4', '#e0c989', '#86abdc', '#baa1e2', '#7ad5d6', '#e4e4e5']},
'niji' : {'fg': '#ffffff', 'bg': '#141515', 'colors': ['#333333', '#d23e08', '#54ca74', '#fff700', '#2ab9ff', '#ff50da', '#1ef9f5', '#ddd0c4', '#515151', '#ffb7b7', '#c1ffae', '#fcffb8', '#8efff3', '#ffa2ed', '#bcffc7', '#ffffff']},
'nocturnal_winter' : {'fg': '#e6e5e5', 'bg': '#0d0d17', 'colors': ['#4d4d4d', '#f12d52', '#09cd7e', '#f5f17a', '#3182e0', '#ff2b6d', '#09c87a', '#fcfcfc', '#808080', '#f16d86', '#0ae78d', '#fffc67', '#6096ff', '#ff78a2', '#0ae78d', '#ffffff']},
'nord' : {'fg': '#d8dee9', 'bg': '#2e3440', 'colors': ['#3b4252', '#bf616a', '#a3be8c', '#ebcb8b', '#81a1c1', '#b48ead', '#88c0d0', '#e5e9f0', '#4c566a', '#bf616a', '#a3be8c', '#ebcb8b', '#81a1c1', '#b48ead', '#8fbcbb', '#eceff4']},
'nord_light' : {'fg': '#414858', 'bg': '#e5e9f0', 'colors': ['#3b4252', '#bf616a', '#a3be8c', '#ebcb8b', '#81a1c1', '#b48ead', '#88c0d0', '#d8dee9', '#4c566a', '#bf616a', '#a3be8c', '#ebcb8b', '#81a1c1', '#b48ead', '#8fbcbb', '#eceff4']},
'nord_wave' : {'fg': '#d8dee9', 'bg': '#212121', 'colors': ['#3b4252', '#bf616a', '#a3be8c', '#ebcb8b', '#81a1c1', '#b48ead', '#88c0d0', '#e5e9f0', '#4c566a', '#bf616a', '#a3be8c', '#ebcb8b', '#81a1c1', '#b48ead', '#8fbcbb', '#eceff4']},
'novel' : {'fg': '#3b2322', 'bg': '#dfdbc3', 'colors': ['#000000', '#cc0000', '#009600', '#d06b00', '#0000cc', '#cc00cc', '#0087cc', '#cccccc', '#808080', '#cc0000', '#009600', '#d06b00', '#0000cc', '#cc00cc', '#0087cc', '#ffffff']},
'nvim_dark' : {'fg': '#e0e2ea', 'bg': '#14161b', 'colors': ['#07080d', '#ffc0b9', '#b3f6c0', '#fce094', '#a6dbff', '#ffcaff', '#8cf8f7', '#eef1f8', '#4f5258', '#ffc0b9', '#b3f6c0', '#fce094', '#a6dbff', '#ffcaff', '#8cf8f7', '#eef1f8']},
'nvim_light' : {'fg': '#14161b', 'bg': '#e0e2ea', 'colors': ['#07080d', '#590008', '#005523', '#6b5300', '#004c73', '#470045', '#007373', '#eef1f8', '#4f5258', '#590008', '#005523', '#6b5300', '#004c73', '#470045', '#007373', '#eef1f8']},
'obsidian' : {'fg': '#cdcdcd', 'bg': '#283033', 'colors': ['#000000', '#a60001', '#00bb00', '#fecd22', '#3a9bdb', '#bb00bb', '#00bbbb', '#bbbbbb', '#555555', '#ff0003', '#93c863', '#fef874', '#a1d7ff', '#ff55ff', '#55ffff', '#ffffff']},
'ocean' : {'fg': '#ffffff', 'bg': '#224fbc', 'colors': ['#000000', '#990000', '#00a600', '#999900', '#0000b2', '#b200b2', '#00a6b2', '#bfbfbf', '#666666', '#e50000', '#00d900', '#e5e500', '#0000ff', '#e500e5', '#00e5e5', '#e5e5e5']},
'oceanic_material' : {'fg': '#c2c8d7', 'bg': '#1c262b', 'colors': ['#000000', '#ee2b2a', '#40a33f', '#ffea2e', '#1e80f0', '#8800a0', '#16afca', '#a4a4a4', '#777777', '#dc5c60', '#70be71', '#fff163', '#54a4f3', '#aa4dbc', '#42c7da', '#ffffff']},
'oceanic_next' : {'fg': '#c1c5cd', 'bg': '#1b2b34', 'colors': ['#1b2b34', '#db686b', '#a2c699', '#f2ca73', '#7198c8', '#bd96c2', '#74b1b2', '#ffffff', '#68737d', '#db686b', '#a2c699', '#f2ca73', '#7198c8', '#bd96c2', '#74b1b2', '#ffffff']},
'ollie' : {'fg': '#8a8dae', 'bg': '#222125', 'colors': ['#000000', '#ac2e31', '#31ac61', '#ac4300', '#2d57ac', '#b08528', '#1fa6ac', '#8a8eac', '#5b3725', '#ff3d48', '#3bff99', '#ff5e1e', '#4488ff', '#ffc21d', '#1ffaff', '#5b6ea7']},
'one_half_dark' : {'fg': '#dcdfe4', 'bg': '#282c34', 'colors': ['#282c34', '#e06c75', '#98c379', '#e5c07b', '#61afef', '#c678dd', '#56b6c2', '#dcdfe4', '#282c34', '#e06c75', '#98c379', '#e5c07b', '#61afef', '#c678dd', '#56b6c2', '#dcdfe4']},
'one_half_light' : {'fg': '#383a42', 'bg': '#fafafa', 'colors': ['#383a42', '#e45649', '#50a14f', '#c18401', '#0184bc', '#a626a4', '#0997b3', '#fafafa', '#4f525e', '#e06c75', '#98c379', '#e5c07b', '#61afef', '#c678dd', '#56b6c2', '#ffffff']},
'operator_mono_dark' : {'fg': '#c3cac2', 'bg': '#191919', 'colors': ['#5a5a5a', '#ca372d', '#4d7b3a', '#d4d697', '#4387cf', '#b86cb4', '#72d5c6', '#ced4cd', '#9a9b99', '#c37d62', '#83d0a2', '#fdfdc5', '#89d3f6', '#ff2c7a', '#82eada', '#fdfdf6']},
'overnight_slumber' : {'fg': '#ced2d6', 'bg': '#0e1729', 'colors': ['#0a1222', '#ffa7c4', '#85cc95', '#ffcb8b', '#8dabe1', '#c792eb', '#78ccf0', '#ffffff', '#575656', '#ffa7c4', '#85cc95', '#ffcb8b', '#8dabe1', '#c792eb', '#ffa7c4', '#ffffff']},
'oxocarbon' : {'fg': '#f2f4f8', 'bg': '#161616', 'colors': ['#161616', '#3ddbd9', '#33b1ff', '#ee5396', '#42be65', '#be95ff', '#ff7eb6', '#f2f4f8', '#585858', '#3ddbd9', '#33b1ff', '#ee5396', '#42be65', '#be95ff', '#ff7eb6', '#f2f4f8']},
'pale_night_hc' : {'fg': '#cccccc', 'bg': '#3e4251', 'colors': ['#000000', '#f07178', '#c3e88d', '#ffcb6b', '#82aaff', '#c792ea', '#89ddff', '#ffffff', '#666666', '#f6a9ae', '#dbf1ba', '#ffdfa6', '#b4ccff', '#ddbdf2', '#b8eaff', '#999999']},
'pandora' : {'fg': '#e1e1e1', 'bg': '#141e43', 'colors': ['#000000', '#ff4242', '#74af68', '#ffad29', '#338f86', '#9414e6', '#23d7d7', '#e2e2e2', '#3f5648', '#ff3242', '#74cd68', '#ffb929', '#23d7d7', '#ff37ff', '#00ede1', '#ffffff']},
'paraiso_dark' : {'fg': '#a39e9b', 'bg': '#2f1e2e', 'colors': ['#2f1e2e', '#ef6155', '#48b685', '#fec418', '#06b6ef', '#815ba4', '#5bc4bf', '#a39e9b', '#776e71', '#ef6155', '#48b685', '#fec418', '#06b6ef', '#815ba4', '#5bc4bf', '#e7e9db']},
'paul_millr' : {'fg': '#f2f2f2', 'bg': '#000000', 'colors': ['#2a2a2a', '#ff0000', '#79ff0f', '#e7bf00', '#396bd7', '#b449be', '#66ccff', '#bbbbbb', '#666666', '#ff0080', '#66ff66', '#f3d64e', '#709aed', '#db67e6', '#7adff2', '#ffffff']},
'pencil_dark' : {'fg': '#f1f1f1', 'bg': '#212121', 'colors': ['#212121', '#c30771', '#10a778', '#a89c14', '#008ec4', '#523c79', '#20a5ba', '#d9d9d9', '#424242', '#fb007a', '#5fd7af', '#f3e430', '#20bbfc', '#6855de', '#4fb8cc', '#f1f1f1']},
'pencil_light' : {'fg': '#424242', 'bg': '#f1f1f1', 'colors': ['#212121', '#c30771', '#10a778', '#a89c14', '#008ec4', '#523c79', '#20a5ba', '#d9d9d9', '#424242', '#fb007a', '#5fd7af', '#f3e430', '#20bbfc', '#6855de', '#4fb8cc', '#f1f1f1']},
'peppermint' : {'fg': '#c8c8c8', 'bg': '#000000', 'colors': ['#353535', '#e74669', '#89d287', '#dab853', '#449fd0', '#da62dc', '#65aaaf', '#b4b4b4', '#535353', '#e4859b', '#a3cca2', '#e1e487', '#6fbce2', '#e586e7', '#96dcdb', '#dfdfdf']},
'piatto_light' : {'fg': '#414141', 'bg': '#ffffff', 'colors': ['#414141', '#b23771', '#66781e', '#cd6f34', '#3c5ea8', '#a454b2', '#66781e', '#ffffff', '#3f3f3f', '#db3365', '#829429', '#cd6f34', '#3c5ea8', '#a454b2', '#829429', '#f2f2f2']},
'pnevma' : {'fg': '#d0d0d0', 'bg': '#1c1c1c', 'colors': ['#2f2e2d', '#a36666', '#90a57d', '#d7af87', '#7fa5bd', '#c79ec4', '#8adbb4', '#d0d0d0', '#4a4845', '#d78787', '#afbea2', '#e4c9af', '#a1bdce', '#d7beda', '#b1e7dd', '#efefef']},
'popping_and_locking' : {'fg': '#ebdbb2', 'bg': '#181921', 'colors': ['#1d2021', '#cc241d', '#98971a', '#d79921', '#458588', '#b16286', '#689d6a', '#a89984', '#928374', '#f42c3e', '#b8bb26', '#fabd2f', '#99c6ca', '#d3869b', '#7ec16e', '#ebdbb2']},
'primary' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#000000', '#db4437', '#0f9d58', '#f4b400', '#4285f4', '#db4437', '#4285f4', '#ffffff', '#000000', '#db4437', '#0f9d58', '#f4b400', '#4285f4', '#4285f4', '#0f9d58', '#ffffff']},
'pro' : {'fg': '#f2f2f2', 'bg': '#000000', 'colors': ['#000000', '#990000', '#00a600', '#999900', '#2009db', '#b200b2', '#00a6b2', '#bfbfbf', '#666666', '#e50000', '#00d900', '#e5e500', '#0000ff', '#e500e5', '#00e5e5', '#e5e5e5']},
'pro_light' : {'fg': '#191919', 'bg': '#ffffff', 'colors': ['#000000', '#e5492b', '#50d148', '#c6c440', '#3b75ff', '#ed66e8', '#4ed2de', '#dcdcdc', '#9f9f9f', '#ff6640', '#61ef57', '#f2f156', '#0082ff', '#ff7eff', '#61f7f8', '#f2f2f2']},
'purple_rain' : {'fg': '#fffbf6', 'bg': '#21084a', 'colors': ['#000000', '#ff260e', '#9be205', '#ffc400', '#00a2fa', '#815bb5', '#00deef', '#ffffff', '#565656', '#ff4250', '#b8e36e', '#ffd852', '#00a6ff', '#ac7bf0', '#74fdf3', '#ffffff']},
'purplepeter' : {'fg': '#ece7fa', 'bg': '#2a1a4a', 'colors': ['#0a0520', '#ff796d', '#99b481', '#efdfac', '#66d9ef', '#e78fcd', '#ba8cff', '#ffba81', '#100b23', '#f99f92', '#b4be8f', '#f2e9bf', '#79daed', '#ba91d4', '#a0a0d6', '#b9aed3']},
'rapture' : {'fg': '#c0c9e5', 'bg': '#111e2a', 'colors': ['#000000', '#fc644d', '#7afde1', '#fff09b', '#6c9bf5', '#ff4fa1', '#64e0ff', '#c0c9e5', '#304b66', '#fc644d', '#7afde1', '#fff09b', '#6c9bf5', '#ff4fa1', '#64e0ff', '#ffffff']},
'raycast_dark' : {'fg': '#ffffff', 'bg': '#1a1a1a', 'colors': ['#000000', '#ff5360', '#59d499', '#ffc531', '#56c2ff', '#cf2f98', '#52eee5', '#ffffff', '#000000', '#ff6363', '#59d499', '#ffc531', '#56c2ff', '#cf2f98', '#52eee5', '#ffffff']},
'raycast_light' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#000000', '#b12424', '#006b4f', '#f8a300', '#138af2', '#9a1b6e', '#3eb8bf', '#ffffff', '#000000', '#b12424', '#006b4f', '#f8a300', '#138af2', '#9a1b6e', '#3eb8bf', '#ffffff']},
'rebecca' : {'fg': '#e8e6ed', 'bg': '#292a44', 'colors': ['#12131e', '#dd7755', '#04dbb5', '#f2e7b7', '#7aa5ff', '#bf9cf9', '#56d3c2', '#e4e3e9', '#666699', '#ff92cd', '#01eac0', '#fffca8', '#69c0fa', '#c17ff8', '#8bfde1', '#f4f2f9']},
'red_alert' : {'fg': '#ffffff', 'bg': '#762423', 'colors': ['#000000', '#d62e4e', '#71be6b', '#beb86b', '#489bee', '#e979d7', '#6bbeb8', '#d6d6d6', '#262626', '#e02553', '#aff08c', '#dfddb7', '#65aaf1', '#ddb7df', '#b7dfdd', '#ffffff']},
'red_planet' : {'fg': '#c2b790', 'bg': '#222222', 'colors': ['#202020', '#8c3432', '#728271', '#e8bf6a', '#69819e', '#896492', '#5b8390', '#b9aa99', '#676767', '#b55242', '#869985', '#ebeb91', '#60827e', '#de4974', '#38add8', '#d6bfb8']},
'red_sands' : {'fg': '#d7c9a7', 'bg': '#7a251e', 'colors': ['#000000', '#ff3f00', '#00bb00', '#e7b000', '#0072ff', '#bb00bb', '#00bbbb', '#bbbbbb', '#555555', '#bb0000', '#00bb00', '#e7b000', '#0072ae', '#ff55ff', '#55ffff', '#ffffff']},
'relaxed' : {'fg': '#d9d9d9', 'bg': '#353a44', 'colors': ['#151515', '#bc5653', '#909d63', '#ebc17a', '#6a8799', '#b06698', '#c9dfff', '#d9d9d9', '#636363', '#bc5653', '#a0ac77', '#ebc17a', '#7eaac7', '#b06698', '#acbbd0', '#f7f7f7']},
'retro' : {'fg': '#13a10e', 'bg': '#000000', 'colors': ['#13a10e', '#13a10e', '#13a10e', '#13a10e', '#13a10e', '#13a10e', '#13a10e', '#13a10e', '#16ba10', '#16ba10', '#16ba10', '#16ba10', '#16ba10', '#16ba10', '#16ba10', '#16ba10']},
'retro_legends' : {'fg': '#45eb45', 'bg': '#0d0d0d', 'colors': ['#262626', '#de5454', '#45eb45', '#f7bf2b', '#4066f2', '#bf4cf2', '#40d9e6', '#bfe6bf', '#4c594c', '#ff6666', '#59ff59', '#ffd933', '#4c80ff', '#e666ff', '#59e6ff', '#f2fff2']},
'rippedcasts' : {'fg': '#ffffff', 'bg': '#2b2b2b', 'colors': ['#000000', '#cdaf95', '#a8ff60', '#bfbb1f', '#75a5b0', '#ff73fd', '#5a647e', '#bfbfbf', '#666666', '#eecbad', '#bcee68', '#e5e500', '#86bdc9', '#e500e5', '#8c9bc4', '#e5e5e5']},
'rose_pine' : {'fg': '#e0def4', 'bg': '#191724', 'colors': ['#26233a', '#eb6f92', '#31748f', '#f6c177', '#9ccfd8', '#c4a7e7', '#ebbcba', '#e0def4', '#6e6a86', '#eb6f92', '#31748f', '#f6c177', '#9ccfd8', '#c4a7e7', '#ebbcba', '#e0def4']},
'rose_pine_dawn' : {'fg': '#575279', 'bg': '#faf4ed', 'colors': ['#f2e9e1', '#b4637a', '#286983', '#ea9d34', '#56949f', '#907aa9', '#d7827e', '#575279', '#9893a5', '#b4637a', '#286983', '#ea9d34', '#56949f', '#907aa9', '#d7827e', '#575279']},
'rose_pine_moon' : {'fg': '#e0def4', 'bg': '#232136', 'colors': ['#393552', '#eb6f92', '#3e8fb0', '#f6c177', '#9ccfd8', '#c4a7e7', '#ea9a97', '#e0def4', '#6e6a86', '#eb6f92', '#3e8fb0', '#f6c177', '#9ccfd8', '#c4a7e7', '#ea9a97', '#e0def4']},
'rouge_2' : {'fg': '#a2a3aa', 'bg': '#17182b', 'colors': ['#5d5d6b', '#c6797e', '#969e92', '#dbcdab', '#6e94b9', '#4c4e78', '#8ab6c1', '#e8e8ea', '#616274', '#c6797e', '#e6dcc4', '#e6dcc4', '#98b3cd', '#8283a1', '#abcbd3', '#e8e8ea']},
'royal' : {'fg': '#514968', 'bg': '#100815', 'colors': ['#241f2b', '#91284c', '#23801c', '#b49d27', '#6580b0', '#674d96', '#8aaabe', '#524966', '#312d3d', '#d5356c', '#2cd946', '#fde83b', '#90baf9', '#a479e3', '#acd4eb', '#9e8cbd']},
'ryuuko' : {'fg': '#ececec', 'bg': '#2c3941', 'colors': ['#2c3941', '#865f5b', '#66907d', '#b1a990', '#6a8e95', '#b18a73', '#88b2ac', '#ececec', '#5d7079', '#865f5b', '#66907d', '#b1a990', '#6a8e95', '#b18a73', '#88b2ac', '#ececec']},
'sakura' : {'fg': '#dd7bdc', 'bg': '#18131e', 'colors': ['#000000', '#d52370', '#41af1a', '#bc7053', '#6964ab', '#c71fbf', '#939393', '#998eac', '#786d69', '#f41d99', '#22e529', '#f59574', '#9892f1', '#e90cdd', '#eeeeee', '#cbb6ff']},
'scarlet_protocol' : {'fg': '#e41951', 'bg': '#1c153d', 'colors': ['#101116', '#ff0051', '#00dc84', '#faf945', '#0271b6', '#ca30c7', '#00c5c7', '#c7c7c7', '#686868', '#ff6e67', '#5ffa68', '#fffc67', '#6871ff', '#bd35ec', '#60fdff', '#ffffff']},
'sea_shells' : {'fg': '#deb88d', 'bg': '#09141b', 'colors': ['#17384c', '#d15123', '#027c9b', '#fca02f', '#1e4950', '#68d4f1', '#50a3b5', '#deb88d', '#434b53', '#d48678', '#628d98', '#fdd39f', '#1bbcdd', '#bbe3ee', '#87acb4', '#fee4ce']},
'seafoam_pastel' : {'fg': '#d4e7d4', 'bg': '#243435', 'colors': ['#757575', '#825d4d', '#728c62', '#ada16d', '#4d7b82', '#8a7267', '#729494', '#e0e0e0', '#8a8a8a', '#cf937a', '#98d9aa', '#fae79d', '#7ac3cf', '#d6b2a1', '#ade0e0', '#e0e0e0']},
'seoulbones_dark' : {'fg': '#dddddd', 'bg': '#4b4b4b', 'colors': ['#4b4b4b', '#e388a3', '#98bd99', '#ffdf9b', '#97bdde', '#a5a6c5', '#6fbdbe', '#dddddd', '#6c6465', '#eb99b1', '#8fcd92', '#ffe5b3', '#a2c8e9', '#b2b3da', '#6bcacb', '#a8a8a8']},
'seoulbones_light' : {'fg': '#555555', 'bg': '#e2e2e2', 'colors': ['#e2e2e2', '#dc5284', '#628562', '#c48562', '#0084a3', '#896788', '#008586', '#555555', '#bfbabb', '#be3c6d', '#487249', '#a76b48', '#006f89', '#7f4c7e', '#006f70', '#777777']},
'seti' : {'fg': '#cacecd', 'bg': '#111213', 'colors': ['#323232', '#c22832', '#8ec43d', '#e0c64f', '#43a5d5', '#8b57b5', '#8ec43d', '#eeeeee', '#323232', '#c22832', '#8ec43d', '#e0c64f', '#43a5d5', '#8b57b5', '#8ec43d', '#ffffff']},
'shades_of_purple' : {'fg': '#ffffff', 'bg': '#1e1d40', 'colors': ['#000000', '#d90429', '#3ad900', '#ffe700', '#6943ff', '#ff2c70', '#00c5c7', '#c7c7c7', '#686868', '#f92a1c', '#43d426', '#f1d000', '#6871ff', '#ff77ff', '#79e8fb', '#ffffff']},
'shaman' : {'fg': '#405555', 'bg': '#001015', 'colors': ['#012026', '#b2302d', '#00a941', '#5e8baa', '#449a86', '#00599d', '#5d7e19', '#405555', '#384451', '#ff4242', '#2aea5e', '#8ed4fd', '#61d5ba', '#1298ff', '#98d028', '#58fbd6']},
'slate' : {'fg': '#35b1d2', 'bg': '#222222', 'colors': ['#222222', '#e2a8bf', '#81d778', '#c4c9c0', '#264b49', '#a481d3', '#15ab9c', '#02c5e0', '#ffffff', '#ffcdd9', '#beffa8', '#d0ccca', '#7ab0d2', '#c5a7d9', '#8cdfe0', '#e0e0e0']},
'sleepy_hollow' : {'fg': '#af9a91', 'bg': '#121214', 'colors': ['#572100', '#ba3934', '#91773f', '#b55600', '#5f63b4', '#a17c7b', '#8faea9', '#af9a91', '#4e4b61', '#d9443f', '#d6b04e', '#f66813', '#8086ef', '#e2c2bb', '#a4dce7', '#d2c7a9']},
'smyck' : {'fg': '#f7f7f7', 'bg': '#1b1b1b', 'colors': ['#000000', '#b84131', '#7da900', '#c4a500', '#62a3c4', '#ba8acc', '#207383', '#a1a1a1', '#7a7a7a', '#d6837c', '#c4f137', '#fee14d', '#8dcff0', '#f79aff', '#6ad9cf', '#f7f7f7']},
'snazzy' : {'fg': '#ebece6', 'bg': '#1e1f29', 'colors': ['#000000', '#fc4346', '#50fb7c', '#f0fb8c', '#49baff', '#fc4cb4', '#8be9fe', '#ededec', '#555555', '#fc4346', '#50fb7c', '#f0fb8c', '#49baff', '#fc4cb4', '#8be9fe', '#ededec']},
'snazzy_soft' : {'fg': '#eff0eb', 'bg': '#282a36', 'colors': ['#000000', '#ff5c57', '#5af78e', '#f3f99d', '#57c7ff', '#ff6ac1', '#9aedfe', '#f1f1f0', '#686868', '#ff5c57', '#5af78e', '#f3f99d', '#57c7ff', '#ff6ac1', '#9aedfe', '#f1f1f0']},
'soft_server' : {'fg': '#99a3a2', 'bg': '#242626', 'colors': ['#000000', '#a2686a', '#9aa56a', '#a3906a', '#6b8fa3', '#6a71a3', '#6ba58f', '#99a3a2', '#666c6c', '#dd5c60', '#bfdf55', '#deb360', '#62b1df', '#606edf', '#64e39c', '#d2e0de']},
'solarized_darcula' : {'fg': '#d2d8d9', 'bg': '#3d3f41', 'colors': ['#25292a', '#f24840', '#629655', '#b68800', '#2075c7', '#797fd4', '#15968d', '#d2d8d9', '#25292a', '#f24840', '#629655', '#b68800', '#2075c7', '#797fd4', '#15968d', '#d2d8d9']},
'solarized_dark_higher_contrast' : {'fg': '#9cc2c3', 'bg': '#001e27', 'colors': ['#002831', '#d11c24', '#6cbe6c', '#a57706', '#2176c7', '#c61c6f', '#259286', '#eae3cb', '#006488', '#f5163b', '#51ef84', '#b27e28', '#178ec8', '#e24d8e', '#00b39e', '#fcf4dc']},
'solarized_dark_patched' : {'fg': '#708284', 'bg': '#001e27', 'colors': ['#002831', '#d11c24', '#738a05', '#a57706', '#2176c7', '#c61c6f', '#259286', '#eae3cb', '#475b62', '#bd3613', '#475b62', '#536870', '#708284', '#5956ba', '#819090', '#fcf4dc']},
'solarized_osaka_night' : {'fg': '#c2caf1', 'bg': '#1a1b25', 'colors': ['#15161d', '#e77d8f', '#a8cd76', '#d8b172', '#82a1f1', '#b69bf1', '#90cdfa', '#aab1d3', '#424866', '#e77d8f', '#a8cd76', '#d8b172', '#82a1f1', '#b69bf1', '#90cdfa', '#c2caf1']},
'space_gray' : {'fg': '#b3b8c3', 'bg': '#20242d', 'colors': ['#000000', '#b04b57', '#87b379', '#e5c179', '#7d8fa4', '#a47996', '#85a7a5', '#b3b8c3', '#000000', '#b04b57', '#87b379', '#e5c179', '#7d8fa4', '#a47996', '#85a7a5', '#ffffff']},
'space_gray_bright' : {'fg': '#f3f3f3', 'bg': '#2a2e3a', 'colors': ['#080808', '#bc5553', '#a0b56c', '#f6c987', '#7baec1', '#b98aae', '#85c9b8', '#d8d8d8', '#626262', '#bc5553', '#a0b56c', '#f6c987', '#7baec1', '#b98aae', '#85c9b8', '#f7f7f7']},
'space_gray_eighties' : {'fg': '#bdbaae', 'bg': '#222222', 'colors': ['#15171c', '#ec5f67', '#81a764', '#fec254', '#5486c0', '#bf83c1', '#57c2c1', '#efece7', '#555555', '#ff6973', '#93d493', '#ffd256', '#4d84d1', '#ff55ff', '#83e9e4', '#ffffff']},
'space_gray_eighties_dull' : {'fg': '#c9c6bc', 'bg': '#222222', 'colors': ['#15171c', '#b24a56', '#92b477', '#c6735a', '#7c8fa5', '#a5789e', '#80cdcb', '#b3b8c3', '#555555', '#ec5f67', '#89e986', '#fec254', '#5486c0', '#bf83c1', '#58c2c1', '#ffffff']},
'spacedust' : {'fg': '#ecf0c1', 'bg': '#0a1e24', 'colors': ['#6e5346', '#e35b00', '#5cab96', '#e3cd7b', '#0f548b', '#e35b00', '#06afc7', '#f0f1ce', '#684c31', '#ff8a3a', '#aecab8', '#ffc878', '#67a0ce', '#ff8a3a', '#83a7b4', '#fefff1']},
'spiderman' : {'fg': '#e3e3e3', 'bg': '#1b1d1e', 'colors': ['#1b1d1e', '#e60813', '#e22928', '#e24756', '#2c3fff', '#2435db', '#3256ff', '#fffef6', '#505354', '#ff0325', '#ff3338', '#fe3a35', '#1d50ff', '#747cff', '#6184ff', '#fffff9']},
'spring' : {'fg': '#4d4d4c', 'bg': '#ffffff', 'colors': ['#000000', '#ff4d83', '#1f8c3b', '#1fc95b', '#1dd3ee', '#8959a8', '#3e999f', '#ffffff', '#000000', '#ff0021', '#1fc231', '#d5b807', '#15a9fd', '#8959a8', '#3e999f', '#ffffff']},
'square' : {'fg': '#acacab', 'bg': '#1a1a1a', 'colors': ['#050505', '#e9897c', '#b6377d', '#ecebbe', '#a9cdeb', '#75507b', '#c9caec', '#f2f2f2', '#141414', '#f99286', '#c3f786', '#fcfbcc', '#b6defb', '#ad7fa8', '#d7d9fc', '#e2e2e2']},
'squirrelsong_dark' : {'fg': '#ad9c8b', 'bg': '#352a21', 'colors': ['#352a21', '#ac493e', '#558240', '#ceb250', '#5993c2', '#7f61b3', '#4f9593', '#cfbaa5', '#6b503c', '#ce574a', '#719955', '#e2c358', '#63a2d6', '#9672d4', '#72aaa8', '#edd5be']},
'srcery' : {'fg': '#fce8c3', 'bg': '#1c1b19', 'colors': ['#1c1b19', '#ef2f27', '#519f50', '#fbb829', '#2c78bf', '#e02c6d', '#0aaeb3', '#baa67f', '#918175', '#f75341', '#98bc37', '#fed06e', '#68a8e4', '#ff5c8f', '#2be4d0', '#fce8c3']},
'starlight' : {'fg': '#ffffff', 'bg': '#242424', 'colors': ['#242424', '#e2425d', '#66b238', '#dec541', '#54aad0', '#e8b2f8', '#5abf9b', '#e6e6e6', '#616161', '#ec5b58', '#6bd162', '#e9e85c', '#78c3f3', '#f2afee', '#6adcc5', '#ffffff']},
'sublette' : {'fg': '#ccced0', 'bg': '#202535', 'colors': ['#253045', '#ee5577', '#55ee77', '#ffdd88', '#5588ff', '#ff77cc', '#44eeee', '#f5f5da', '#405570', '#ee6655', '#99ee77', '#ffff77', '#77bbff', '#aa88ff', '#55ffbb', '#ffffee']},
'subliminal' : {'fg': '#d4d4d4', 'bg': '#282c35', 'colors': ['#7f7f7f', '#e15a60', '#a9cfa4', '#ffe2a9', '#6699cc', '#f1a5ab', '#5fb3b3', '#d4d4d4', '#7f7f7f', '#e15a60', '#a9cfa4', '#ffe2a9', '#6699cc', '#f1a5ab', '#5fb3b3', '#d4d4d4']},
'sugarplum' : {'fg': '#db7ddd', 'bg': '#111147', 'colors': ['#111147', '#5ca8dc', '#53b397', '#249a84', '#db7ddd', '#d0beee', '#f9f3f9', '#a175d4', '#111147', '#5cb5dc', '#52deb5', '#01f5c7', '#fa5dfd', '#c6a5fd', '#ffffff', '#b577fd']},
'sundried' : {'fg': '#c9c9c9', 'bg': '#1a1818', 'colors': ['#302b2a', '#a7463d', '#587744', '#9d602a', '#485b98', '#864651', '#9c814f', '#c9c9c9', '#4d4e48', '#aa000c', '#128c21', '#fc6a21', '#7999f7', '#fd8aa1', '#fad484', '#ffffff']},
'symfonic' : {'fg': '#ffffff', 'bg': '#000000', 'colors': ['#000000', '#dc322f', '#56db3a', '#ff8400', '#0084d4', '#b729d9', '#ccccff', '#ffffff', '#1b1d21', '#dc322f', '#56db3a', '#ff8400', '#0084d4', '#b729d9', '#ccccff', '#ffffff']},
'synthwave' : {'fg': '#dad9c7', 'bg': '#000000', 'colors': ['#000000', '#f6188f', '#1ebb2b', '#fdf834', '#2186ec', '#f85a21', '#12c3e2', '#ffffff', '#000000', '#f841a0', '#25c141', '#fdf454', '#2f9ded', '#f97137', '#19cde6', '#ffffff']},
'synthwave_alpha' : {'fg': '#f2f2e3', 'bg': '#241b30', 'colors': ['#241b30', '#e60a70', '#00986c', '#adad3e', '#6e29ad', '#b300ad', '#00b0b1', '#b9b1bc', '#7f7094', '#e60a70', '#0ae4a4', '#f9f972', '#aa54f9', '#ff00f6', '#00fbfd', '#f2f2e3']},
'synthwave_everything' : {'fg': '#f0eff1', 'bg': '#2a2139', 'colors': ['#fefefe', '#f97e72', '#72f1b8', '#fede5d', '#6d77b3', '#c792ea', '#f772e0', '#fefefe', '#fefefe', '#f88414', '#72f1b8', '#fff951', '#36f9f6', '#e1acff', '#f92aad', '#fefefe']},
'tango_adapted' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#000000', '#ff0000', '#59d600', '#f0cb00', '#00a2ff', '#c17ecc', '#00d0d6', '#e6ebe1', '#8f928b', '#ff0013', '#93ff00', '#fff121', '#88c9ff', '#e9a7e1', '#00feff', '#f6f6f4']},
'tango_half_adapted' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#000000', '#ff0000', '#4cc300', '#e2c000', '#008ef6', '#a96cb3', '#00bdc3', '#e0e5db', '#797d76', '#ff0013', '#8af600', '#ffec00', '#76bfff', '#d898d1', '#00f6fa', '#f4f4f2']},
'teerb' : {'fg': '#d0d0d0', 'bg': '#262626', 'colors': ['#1c1c1c', '#d68686', '#aed686', '#d7af87', '#86aed6', '#d6aed6', '#8adbb4', '#d0d0d0', '#1c1c1c', '#d68686', '#aed686', '#e4c9af', '#86aed6', '#d6aed6', '#b1e7dd', '#efefef']},
'terafox' : {'fg': '#e6eaea', 'bg': '#152528', 'colors': ['#2f3239', '#e85c51', '#7aa4a1', '#fda47f', '#5a93aa', '#ad5c7c', '#a1cdd8', '#ebebeb', '#4e5157', '#eb746b', '#8eb2af', '#fdb292', '#73a3b7', '#b97490', '#afd4de', '#eeeeee']},
'terminal_basic' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#000000', '#990000', '#00a600', '#999900', '#0000b2', '#b200b2', '#00a6b2', '#bfbfbf', '#666666', '#e50000', '#00d900', '#e5e500', '#0000ff', '#e500e5', '#00e5e5', '#e5e5e5']},
'thayer_bright' : {'fg': '#f8f8f8', 'bg': '#1b1d1e', 'colors': ['#1b1d1e', '#f92672', '#4df840', '#f4fd22', '#2757d6', '#8c54fe', '#38c8b5', '#ccccc6', '#505354', '#ff5995', '#b6e354', '#feed6c', '#3f78ff', '#9e6ffe', '#23cfd5', '#f8f8f2']},
'the_hulk' : {'fg': '#b5b5b5', 'bg': '#1b1d1e', 'colors': ['#1b1d1e', '#269d1b', '#13ce30', '#63e457', '#2525f5', '#641f74', '#378ca9', '#d9d8d1', '#505354', '#8dff2a', '#48ff77', '#3afe16', '#506b95', '#72589d', '#4085a6', '#e5e6e1']},
'tinacious_design_dark' : {'fg': '#cbcbf0', 'bg': '#1d1d26', 'colors': ['#1d1d26', '#ff3399', '#00d364', '#ffcc66', '#00cbff', '#cc66ff', '#00ceca', '#cbcbf0', '#636667', '#ff2f92', '#00d364', '#ffd479', '#00cbff', '#d783ff', '#00d5d4', '#d5d6f3']},
'tinacious_design_light' : {'fg': '#1d1d26', 'bg': '#f8f8ff', 'colors': ['#1d1d26', '#ff3399', '#00d364', '#ffcc66', '#00cbff', '#cc66ff', '#00ceca', '#cbcbf0', '#636667', '#ff2f92', '#00d364', '#ffd479', '#00cbff', '#d783ff', '#00d5d4', '#d5d6f3']},
'tokyonight' : {'fg': '#c0caf5', 'bg': '#1a1b26', 'colors': ['#15161e', '#f7768e', '#9ece6a', '#e0af68', '#7aa2f7', '#bb9af7', '#7dcfff', '#a9b1d6', '#414868', '#f7768e', '#9ece6a', '#e0af68', '#7aa2f7', '#bb9af7', '#7dcfff', '#c0caf5']},
'tokyonight_day' : {'fg': '#3760bf', 'bg': '#e1e2e7', 'colors': ['#e9e9ed', '#f52a65', '#587539', '#8c6c3e', '#2e7de9', '#9854f1', '#007197', '#6172b0', '#a1a6c5', '#f52a65', '#587539', '#8c6c3e', '#2e7de9', '#9854f1', '#007197', '#3760bf']},
'tokyonight_moon' : {'fg': '#c8d3f5', 'bg': '#222436', 'colors': ['#1b1d2b', '#ff757f', '#c3e88d', '#ffc777', '#82aaff', '#c099ff', '#86e1fc', '#828bb8', '#444a73', '#ff757f', '#c3e88d', '#ffc777', '#82aaff', '#c099ff', '#86e1fc', '#c8d3f5']},
'tokyonight_night' : {'fg': '#c0caf5', 'bg': '#1a1b26', 'colors': ['#15161e', '#f7768e', '#9ece6a', '#e0af68', '#7aa2f7', '#bb9af7', '#7dcfff', '#a9b1d6', '#414868', '#f7768e', '#9ece6a', '#e0af68', '#7aa2f7', '#bb9af7', '#7dcfff', '#c0caf5']},
'tokyonight_storm' : {'fg': '#c0caf5', 'bg': '#24283b', 'colors': ['#1d202f', '#f7768e', '#9ece6a', '#e0af68', '#7aa2f7', '#bb9af7', '#7dcfff', '#a9b1d6', '#414868', '#f7768e', '#9ece6a', '#e0af68', '#7aa2f7', '#bb9af7', '#7dcfff', '#c0caf5']},
'tomorrow' : {'fg': '#4d4d4c', 'bg': '#ffffff', 'colors': ['#000000', '#c82829', '#718c00', '#eab700', '#4271ae', '#8959a8', '#3e999f', '#ffffff', '#000000', '#c82829', '#718c00', '#eab700', '#4271ae', '#8959a8', '#3e999f', '#ffffff']},
'tomorrow_night' : {'fg': '#c5c8c6', 'bg': '#1d1f21', 'colors': ['#000000', '#cc6666', '#b5bd68', '#f0c674', '#81a2be', '#b294bb', '#8abeb7', '#ffffff', '#000000', '#cc6666', '#b5bd68', '#f0c674', '#81a2be', '#b294bb', '#8abeb7', '#ffffff']},
'tomorrow_night_blue' : {'fg': '#ffffff', 'bg': '#002451', 'colors': ['#000000', '#ff9da4', '#d1f1a9', '#ffeead', '#bbdaff', '#ebbbff', '#99ffff', '#ffffff', '#000000', '#ff9da4', '#d1f1a9', '#ffeead', '#bbdaff', '#ebbbff', '#99ffff', '#ffffff']},
'tomorrow_night_bright' : {'fg': '#eaeaea', 'bg': '#000000', 'colors': ['#000000', '#d54e53', '#b9ca4a', '#e7c547', '#7aa6da', '#c397d8', '#70c0b1', '#ffffff', '#000000', '#d54e53', '#b9ca4a', '#e7c547', '#7aa6da', '#c397d8', '#70c0b1', '#ffffff']},
'tomorrow_night_burns' : {'fg': '#a1b0b8', 'bg': '#151515', 'colors': ['#252525', '#832e31', '#a63c40', '#d3494e', '#fc595f', '#df9395', '#ba8586', '#f5f5f5', '#5d6f71', '#832e31', '#a63c40', '#d2494e', '#fc595f', '#df9395', '#ba8586', '#f5f5f5']},
'tomorrow_night_eighties' : {'fg': '#cccccc', 'bg': '#2d2d2d', 'colors': ['#000000', '#f2777a', '#99cc99', '#ffcc66', '#6699cc', '#cc99cc', '#66cccc', '#ffffff', '#000000', '#f2777a', '#99cc99', '#ffcc66', '#6699cc', '#cc99cc', '#66cccc', '#ffffff']},
'toy_chest' : {'fg': '#31d07b', 'bg': '#24364b', 'colors': ['#2c3f58', '#be2d26', '#1a9172', '#db8e27', '#325d96', '#8a5edc', '#35a08f', '#23d183', '#336889', '#dd5944', '#31d07b', '#e7d84b', '#34a6da', '#ae6bdc', '#42c3ae', '#d5d5d5']},
'treehouse' : {'fg': '#786b53', 'bg': '#191919', 'colors': ['#321300', '#b2270e', '#44a900', '#aa820c', '#58859a', '#97363d', '#b25a1e', '#786b53', '#433626', '#ed5d20', '#55f238', '#f2b732', '#85cfed', '#e14c5a', '#f07d14', '#ffc800']},
'twilight' : {'fg': '#ffffd4', 'bg': '#141414', 'colors': ['#141414', '#c06d44', '#afb97a', '#c2a86c', '#44474a', '#b4be7c', '#778385', '#ffffd4', '#262626', '#de7c4c', '#ccd88c', '#e2c47e', '#5a5e62', '#d0dc8e', '#8a989b', '#ffffd4']},
'ubuntu' : {'fg': '#eeeeec', 'bg': '#300a24', 'colors': ['#2e3436', '#cc0000', '#4e9a06', '#c4a000', '#3465a4', '#75507b', '#06989a', '#d3d7cf', '#555753', '#ef2929', '#8ae234', '#fce94f', '#729fcf', '#ad7fa8', '#34e2e2', '#eeeeec']},
'ultra_dark' : {'fg': '#ffffff', 'bg': '#000000', 'colors': ['#000000', '#f07178', '#c3e88d', '#ffcb6b', '#82aaff', '#c792ea', '#89ddff', '#cccccc', '#333333', '#f6a9ae', '#dbf1ba', '#ffdfa6', '#b4ccff', '#ddbdf2', '#b8eaff', '#ffffff']},
'ultra_violent' : {'fg': '#c1c1c1', 'bg': '#242728', 'colors': ['#242728', '#ff0090', '#b6ff00', '#fff727', '#47e0fb', '#d731ff', '#0effbb', '#e1e1e1', '#636667', '#fb58b4', '#deff8c', '#ebe087', '#7fecff', '#e681ff', '#69fcd3', '#f9f9f5']},
'under_the_sea' : {'fg': '#ffffff', 'bg': '#011116', 'colors': ['#022026', '#b2302d', '#00a941', '#59819c', '#459a86', '#00599d', '#5d7e19', '#405555', '#384451', '#ff4242', '#2aea5e', '#8ed4fd', '#61d5ba', '#1298ff', '#98d028', '#58fbd6']},
'unikitty' : {'fg': '#0b0b0b', 'bg': '#ff8cd9', 'colors': ['#0c0c0c', '#a80f20', '#bafc8b', '#eedf4b', '#145fcd', '#ff36a2', '#6bd1bc', '#e2d7e1', '#434343', '#d91329', '#d3ffaf', '#ffef50', '#0075ea', '#fdd5e5', '#79ecd5', '#fff3fe']},
'urple' : {'fg': '#877a9b', 'bg': '#1b1b23', 'colors': ['#000000', '#b0425b', '#37a415', '#ad5c42', '#564d9b', '#6c3ca1', '#808080', '#87799c', '#5d3225', '#ff6388', '#29e620', '#f08161', '#867aed', '#a05eee', '#eaeaea', '#bfa3ff']},
'vaughn' : {'fg': '#dcdccc', 'bg': '#25234f', 'colors': ['#25234f', '#705050', '#60b48a', '#dfaf8f', '#5555ff', '#f08cc3', '#8cd0d3', '#709080', '#709080', '#dca3a3', '#60b48a', '#f0dfaf', '#5555ff', '#ec93d3', '#93e0e3', '#ffffff']},
'vesper' : {'fg': '#ffffff', 'bg': '#101010', 'colors': ['#101010', '#f5a191', '#90b99f', '#e6b99d', '#aca1cf', '#e29eca', '#ea83a5', '#a0a0a0', '#7e7e7e', '#ff8080', '#99ffe4', '#ffc799', '#b9aeda', '#ecaad6', '#f591b2', '#ffffff']},
'vibrant_ink' : {'fg': '#ffffff', 'bg': '#000000', 'colors': ['#878787', '#ff6600', '#ccff04', '#ffcc00', '#44b4cc', '#9933cc', '#44b4cc', '#f5f5f5', '#555555', '#ff0000', '#00ff00', '#ffff00', '#0000ff', '#ff00ff', '#00ffff', '#e5e5e5']},
'vimbones' : {'fg': '#353535', 'bg': '#f0f0ca', 'colors': ['#f0f0ca', '#a8334c', '#4f6c31', '#944927', '#286486', '#88507d', '#3b8992', '#353535', '#c6c6a3', '#94253e', '#3f5a22', '#803d1c', '#1d5573', '#7b3b70', '#2b747c', '#5c5c5c']},
'violet_dark' : {'fg': '#708284', 'bg': '#1c1d1f', 'colors': ['#56595c', '#c94c22', '#85981c', '#b4881d', '#2e8bce', '#d13a82', '#32a198', '#c9c6bd', '#45484b', '#bd3613', '#738a04', '#a57705', '#2176c7', '#c61c6f', '#259286', '#c9c6bd']},
'violet_light' : {'fg': '#536870', 'bg': '#fcf4dc', 'colors': ['#56595c', '#c94c22', '#85981c', '#b4881d', '#2e8bce', '#d13a82', '#32a198', '#d3d0c9', '#45484b', '#bd3613', '#738a04', '#a57705', '#2176c7', '#c61c6f', '#259286', '#c9c6bd']},
'warm_neon' : {'fg': '#afdab6', 'bg': '#404040', 'colors': ['#000000', '#e24346', '#39b13a', '#dae145', '#4261c5', '#f920fb', '#2abbd4', '#d0b8a3', '#fefcfc', '#e97071', '#9cc090', '#ddda7a', '#7b91d6', '#f674ba', '#5ed1e5', '#d8c8bb']},
'wez' : {'fg': '#b3b3b3', 'bg': '#000000', 'colors': ['#000000', '#cc5555', '#55cc55', '#cdcd55', '#5555cc', '#cc55cc', '#7acaca', '#cccccc', '#555555', '#ff5555', '#55ff55', '#ffff55', '#5555ff', '#ff55ff', '#55ffff', '#ffffff']},
'whimsy' : {'fg': '#b3b0d6', 'bg': '#29283b', 'colors': ['#535178', '#ef6487', '#5eca89', '#fdd877', '#65aef7', '#aa7ff0', '#43c1be', '#ffffff', '#535178', '#ef6487', '#5eca89', '#fdd877', '#65aef7', '#aa7ff0', '#43c1be', '#ffffff']},
'wild_cherry' : {'fg': '#dafaff', 'bg': '#1f1726', 'colors': ['#000507', '#d94085', '#2ab250', '#ffd16f', '#883cdc', '#ececec', '#c1b8b7', '#fff8de', '#009cc9', '#da6bac', '#f4dca5', '#eac066', '#308cba', '#ae636b', '#ff919d', '#e4838d']},
'wilmersdorf' : {'fg': '#c6c6c6', 'bg': '#282b33', 'colors': ['#34373e', '#e06383', '#7ebebd', '#cccccc', '#a6c1e0', '#e1c1ee', '#5b94ab', '#ababab', '#434750', '#fa7193', '#8fd7d6', '#d1dfff', '#b2cff0', '#efccfd', '#69abc5', '#d3d3d3']},
'wombat' : {'fg': '#dedacf', 'bg': '#171717', 'colors': ['#000000', '#ff615a', '#b1e969', '#ebd99c', '#5da9f6', '#e86aff', '#82fff7', '#dedacf', '#313131', '#f58c80', '#ddf88f', '#eee5b2', '#a5c7ff', '#ddaaff', '#b7fff9', '#ffffff']},
'wryan' : {'fg': '#999993', 'bg': '#101010', 'colors': ['#333333', '#8c4665', '#287373', '#7c7c99', '#395573', '#5e468c', '#31658c', '#899ca1', '#3d3d3d', '#bf4d80', '#53a6a6', '#9e9ecb', '#477ab3', '#7e62b3', '#6096bf', '#c0c0c0']},
'xcodedark' : {'fg': '#dfdfe0', 'bg': '#292a30', 'colors': ['#414453', '#ff8170', '#78c2b3', '#d9c97c', '#4eb0cc', '#ff7ab2', '#b281eb', '#dfdfe0', '#7f8c98', '#ff8170', '#acf2e4', '#ffa14f', '#6bdfff', '#ff7ab2', '#dabaff', '#dfdfe0']},
'xcodedarkhc' : {'fg': '#ffffff', 'bg': '#1f1f24', 'colors': ['#43454b', '#ff8a7a', '#83c9bc', '#d9c668', '#4ec4e6', '#ff85b8', '#cda1ff', '#ffffff', '#838991', '#ff8a7a', '#b1faeb', '#ffa14f', '#6bdfff', '#ff85b8', '#e5cfff', '#ffffff']},
'xcodelight' : {'fg': '#262626', 'bg': '#ffffff', 'colors': ['#b4d8fd', '#d12f1b', '#3e8087', '#78492a', '#0f68a0', '#ad3da4', '#804fb8', '#262626', '#8a99a6', '#d12f1b', '#23575c', '#78492a', '#0b4f79', '#ad3da4', '#4b21b0', '#262626']},
'xcodelighthc' : {'fg': '#000000', 'bg': '#ffffff', 'colors': ['#b4d8fd', '#ad1805', '#355d61', '#78492a', '#0058a1', '#9c2191', '#703daa', '#000000', '#8a99a6', '#ad1805', '#174145', '#78492a', '#003f73', '#9c2191', '#441ea1', '#000000']},
'xcodewwdc' : {'fg': '#e7e8eb', 'bg': '#292c36', 'colors': ['#494d5c', '#bb383a', '#94c66e', '#d28e5d', '#8884c5', '#b73999', '#00aba4', '#e7e8eb', '#7f869e', '#bb383a', '#94c66e', '#d28e5d', '#8884c5', '#b73999', '#00aba4', '#e7e8eb']},
'zenbones' : {'fg': '#2c363c', 'bg': '#f0edec', 'colors': ['#f0edec', '#a8334c', '#4f6c31', '#944927', '#286486', '#88507d', '#3b8992', '#2c363c', '#cfc1ba', '#94253e', '#3f5a22', '#803d1c', '#1d5573', '#7b3b70', '#2b747c', '#4f5e68']},
'zenbones_dark' : {'fg': '#b4bdc3', 'bg': '#1c1917', 'colors': ['#1c1917', '#de6e7c', '#819b69', '#b77e64', '#6099c0', '#b279a7', '#66a5ad', '#b4bdc3', '#403833', '#e8838f', '#8bae68', '#d68c67', '#61abda', '#cf86c1', '#65b8c1', '#888f94']},
'zenbones_light' : {'fg': '#2c363c', 'bg': '#f0edec', 'colors': ['#f0edec', '#a8334c', '#4f6c31', '#944927', '#286486', '#88507d', '#3b8992', '#2c363c', '#cfc1ba', '#94253e', '#3f5a22', '#803d1c', '#1d5573', '#7b3b70', '#2b747c', '#4f5e68']},
'zenburn' : {'fg': '#dcdccc', 'bg': '#3f3f3f', 'colors': ['#4d4d4d', '#705050', '#60b48a', '#f0dfaf', '#506070', '#dc8cc3', '#8cd0d3', '#dcdccc', '#709080', '#dca3a3', '#c3bf9f', '#e0cf9f', '#94bff3', '#ec93d3', '#93e0e3', '#ffffff']},
'zenburned' : {'fg': '#f0e4cf', 'bg': '#404040', 'colors': ['#404040', '#e3716e', '#819b69', '#b77e64', '#6099c0', '#b279a7', '#66a5ad', '#f0e4cf', '#625a5b', '#ec8685', '#8bae68', '#d68c67', '#61abda', '#cf86c1', '#65b8c1', '#c0ab86']},
'zenwritten_dark' : {'fg': '#bbbbbb', 'bg': '#191919', 'colors': ['#191919', '#de6e7c', '#819b69', '#b77e64', '#6099c0', '#b279a7', '#66a5ad', '#bbbbbb', '#3d3839', '#e8838f', '#8bae68', '#d68c67', '#61abda', '#cf86c1', '#65b8c1', '#8e8e8e']},
'zenwritten_light' : {'fg': '#353535', 'bg': '#eeeeee', 'colors': ['#eeeeee', '#a8334c', '#4f6c31', '#944927', '#286486', '#88507d', '#3b8992', '#353535', '#c6c3c3', '#94253e', '#3f5a22', '#803d1c', '#1d5573', '#7b3b70', '#2b747c', '#5c5c5c']},
}


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Exiting...")
