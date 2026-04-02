"""
search_all_windows.py - Sublime Text plugin

Searches the content of every open view across every open window.
Invoke via Command Palette: "Search All Windows"
"""

import os
import re

import sublime
import sublime_plugin

MAX_RESULTS = 500
CONTEXT_LEN = 120


class SearchAllWindowsCommand(sublime_plugin.WindowCommand):

    def run(self):
        self._origin_window = self.window
        self._origin_view = self.window.active_view()
        self._origin_sel = (
            list(self._origin_view.sel()) if self._origin_view else []
        )
        self._results = []

        self.window.show_input_panel(
            "Search All Windows (regex):",
            "",
            self._on_done,
            None,
            None,
        )

    def _on_done(self, pattern):
        if not pattern:
            return

        try:
            re.compile(pattern)
        except re.error as exc:
            sublime.error_message("Search All Windows - invalid regex:\n" + str(exc))
            return

        results = []
        items = []
        truncated = False

        for window in sublime.windows():
            for view in window.views():
                # Skip scratch views (Find Results, output panels, our own results, etc.)
                if view.is_scratch():
                    continue
                try:
                    matches = view.find_all(pattern, sublime.IGNORECASE)
                except Exception:
                    continue

                for region in matches:
                    if len(results) >= MAX_RESULTS:
                        truncated = True
                        break

                    row, _col = view.rowcol(region.begin())
                    line_text = view.substr(view.line(region)).strip()
                    if len(line_text) > CONTEXT_LEN:
                        line_text = line_text[:CONTEXT_LEN] + "..."

                    file_name = view.file_name()
                    if file_name:
                        short = os.path.basename(file_name)
                        detail = file_name
                    else:
                        short = view.name() or ("untitled (view " + str(view.id()) + ")")
                        detail = "[unsaved buffer] - window " + str(window.id())

                    results.append((window, view, region))
                    items.append([
                        short + "  :  line " + str(row + 1),
                        line_text,
                        detail,
                    ])

                if truncated:
                    break
            if truncated:
                break

        count = len(results)
        if count == 0:
            sublime.status_message("Search All Windows: no matches for: " + pattern)
            return

        suffix = "  (first " + str(MAX_RESULTS) + " shown)" if truncated else ""
        sublime.status_message("Search All Windows: " + str(count) + " match(es)" + suffix)

        self._results = results

        self.window.show_quick_panel(
            items,
            self._on_select,
            sublime.KEEP_OPEN_ON_FOCUS_LOST,
            0,
            self._on_highlight,
        )

    def _on_highlight(self, index):
        if index < 0 or index >= len(self._results):
            return
        window, view, region = self._results[index]
        # Only preview within the same window — bringing a different window
        # to the front steals focus and collapses the quick panel.
        if window.id() == self.window.id():
            self.window.focus_view(view)
            view.show_at_center(region)

    def _on_select(self, index):
        if index < 0:
            self._origin_window.bring_to_front()
            if self._origin_view:
                self._origin_window.focus_view(self._origin_view)
                sel = self._origin_view.sel()
                sel.clear()
                for r in self._origin_sel:
                    sel.add(r)
                if self._origin_sel:
                    self._origin_view.show_at_center(self._origin_sel[0])
            return

        window, view, region = self._results[index]
        window.bring_to_front()
        window.focus_view(view)
        sel = view.sel()
        sel.clear()
        sel.add(region)
        view.show_at_center(region)
