# Search All Windows

A [Sublime Text](https://www.sublimetext.com) plugin that searches across every open document in every open window — something the built-in Find doesn't do.

Sublime Text's built-in **Find** (`Cmd+F`) only searches the current file, and **Find in Files** only searches files on disk. This plugin searches the live buffer contents of every open tab across every open window, including **unsaved documents**.

## Usage

Open the Command Palette (`Cmd+Shift+P`) and run **Search All Windows**.

- Type a search term (plain text or regex, case-insensitive)
- A results panel shows every match across all open windows and tabs
- Scroll through results to preview matches within the current window
- Press **Enter** to jump to a match (switches windows/tabs automatically)
- Press **Escape** to cancel and return to your original position

## Optional keybinding

Add to your key bindings (`Preferences → Key Bindings`):

```json
{ "keys": ["super+shift+f"], "command": "search_all_windows" }
```

## Installation

### Via Package Control (recommended)

1. Open the Command Palette and run `Package Control: Install Package`
2. Search for **Search All Windows** and install

### Manual

Copy `search_all_windows.py` and `SearchAllWindows.sublime-commands` into your Sublime Text `Packages/User/` directory:

```
~/Library/Application Support/Sublime Text/Packages/User/
```

## Requirements

Sublime Text 4 (build 4050+)

## License

MIT
