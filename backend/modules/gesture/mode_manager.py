from enum import Enum


class Mode(Enum):
    IDLE = 0
    NAVIGATION = 1
    CURSOR = 2


class ModeManager:
    def __init__(self):

        # ==========================
        # Current Active Mode
        # ==========================

        self.current_mode = Mode.IDLE

        # ==========================
        # Gesture Timers
        # ==========================

        self.palm_timer = None
        self.cursor_timer = None
        self.collapse_timer = None

        # ==========================
        # Gesture Locks
        # ==========================

        self.cursor_lock = False
        self.navigation_lock = False

    # =====================================================
    # Mode Switching
    # =====================================================

    def enter_idle(self):
        self.current_mode = Mode.IDLE

    def enter_navigation(self):
        self.current_mode = Mode.NAVIGATION

    def enter_cursor(self):
        self.current_mode = Mode.CURSOR

    # =====================================================
    # Mode Queries
    # =====================================================

    def is_idle(self):
        return self.current_mode == Mode.IDLE

    def is_navigation(self):
        return self.current_mode == Mode.NAVIGATION

    def is_cursor(self):
        return self.current_mode == Mode.CURSOR

    # =====================================================
    # Timer Management
    # =====================================================

    def reset_palm_timer(self):
        self.palm_timer = None

    def reset_cursor_timer(self):
        self.cursor_timer = None

    def reset_collapse_timer(self):
        self.collapse_timer = None

    def reset_all_timers(self):
        self.palm_timer = None
        self.cursor_timer = None
        self.collapse_timer = None

    # =====================================================
    # Lock Management
    # =====================================================

    def lock_cursor(self):
        self.cursor_lock = True

    def unlock_cursor(self):
        self.cursor_lock = False

    def lock_navigation(self):
        self.navigation_lock = True

    def unlock_navigation(self):
        self.navigation_lock = False

    def reset_locks(self):
        self.cursor_lock = False
        self.navigation_lock = False

    # =====================================================
    # Full Reset
    # =====================================================

    def reset(self):
        self.enter_idle()
        self.reset_all_timers()
        self.reset_locks()

    # =====================================================
    # Debug Helper
    # =====================================================

    def __str__(self):
        return (
            f"Mode={self.current_mode.name}, "
            f"CursorLock={self.cursor_lock}, "
            f"NavigationLock={self.navigation_lock}"
        )