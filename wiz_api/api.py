import time
from typing import Optional, List, Tuple, Union
import pyautogui
import win32gui
import cv2

class Client:
    def __init__(self, handle: Optional[int] = None) -> None:
        self._handle: Optional[int] = handle
        self._spell_memory: dict[str, Tuple[float, float]] = {}
        
        # rectangles defined as (x, y, width, height)
        self._friends_area: Tuple[int, int, int, int] = (625, 65, 20, 240)
        self._spell_area: Tuple[int, int, int, int] = (215, 300, 370, 80)
        self._enemy_area: Tuple[int, int, int, int] = (60, 40, 650, 45)

    def wait(self, s: float) -> "Client":
        """Alias for time.sleep() that return self for function chaining"""
        time.sleep(s)
        return self

    def register_window(self, name: str = "Wizard101", nth: int = 0) -> "Client":
        """Assigns the instance to a wizard101 window (Required before using any other API functions)"""
        def win_enum_callback(handle: int, param: list) -> None:
            if name == str(win32gui.GetWindowText(handle)):
                param.append(handle)

        handles: List[int] = []
        # Get all windows with the name "Wizard101"
        win32gui.EnumWindows(win_enum_callback, handles)
        handles.sort()
        # Assigns the one at index nth
        self._handle = handles[nth]
        return self
    
    def is_active(self) -> bool:
        """Returns true if the window is focused"""
        return self._handle == win32gui.GetForegroundWindow()

    def set_active(self) -> "Client":
        """Sets the window to active if it isn't already"""
        if not self.is_active():
            """Press alt before and after to prevent a nasty bug"""
            pyautogui.press('alt')
            win32gui.SetForegroundWindow(self._handle)
            pyautogui.press('alt')
        return self
    
    def get_window_rect(self) -> List[int]:
        """Get the bounding rectangle of the window """
        rect = win32gui.GetWindowRect(self._handle)
        return [rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]]

    def mouse_out_of_area(self, area: Tuple[int, int, int, int]) -> "Client":
        """Move the mouse outside of an area, to make sure the mouse doesn't interfere with image matching"""
        # Adjust the region so that it is relative to the window
        wx, wy = self.get_window_rect()[:2]
        region = list(area)
        region[0] += wx
        region[1] += wy

        def in_area(area: Tuple[int, int, int, int]) -> bool:
            px, py = pyautogui.position()
            x, y, w, h = area
            return (px > x and px < (x + w) and py > y and py < (y + h))

        while in_area(region):
            pyautogui.moveRel(0, -100, duration=0.5)

        return self

    def match_image(self, largeImg: str, smallImg: str, threshold: float = 0.1, debug: bool = False) -> Union[Tuple[float, float], bool]:
        """ Finds smallImg in largeImg using template matching
            Adjust threshold for the precision of the match (between 0 and 1, the lowest being more precise)
            Returns false if no match was found with the given threshold
        """
        method = cv2.TM_SQDIFF_NORMED

        # Read the images from the file
        small_image = cv2.imread(smallImg)
        large_image = cv2.imread(largeImg)
        w, h = small_image.shape[:-1]

        result = cv2.matchTemplate(small_image, large_image, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        if (mn >= threshold):
            return False

        # Extract the coordinates of our best match
        x, y = mnLoc

        if debug:
            # Draw the rectangle:
            # Get the size of the template. This is the same size as the match.
            trows, tcols = small_image.shape[:2]

            # Draw the rectangle on large_image
            cv2.rectangle(large_image, (x, y),
                          (x + tcols, y + trows), (0, 0, 255), 2)

            # Display the original image with the rectangle around the match.
            cv2.imshow('output', large_image)

            # The image is only displayed if we call this
            cv2.waitKey(0)

        # Return coordinates to center of match
        return (x + (w * 0.5), y + (h * 0.5))

    def pixel_matches_color(self, coords: Tuple[int, int], rgb: Tuple[int, int, int], threshold: int = 0) -> bool:
        """Matches the color of a pixel relative to the window's position"""
        wx, wy = self.get_window_rect()[:2]
        x, y = coords
        # self.move_mouse(x, y)
        return pyautogui.pixelMatchesColor(x + wx, y + wy, rgb, tolerance=threshold)
    
    def move_mouse(self, x: int, y: int, speed: float = 0.5) -> "Client":
        """Moves the mouse to the position (x, y) relative to the window's position"""
        wx, wy = self.get_window_rect()[:2]
        pyautogui.moveTo(wx + x, wy + y, speed)
        return self

    def click(self, x: int, y: int, delay: float = 0.1, speed: float = 0.5, button: str = 'left') -> "Client":
        """Moves the mouse to (x, y) relative to the window and presses the mouse button"""
        (self.set_active()
         .move_mouse(x, y, speed=speed)
         .wait(delay))

        pyautogui.click(button=button)
        return self
    
    def hold_key(self, key: str, holdtime: float) -> "Client":
        """ 
        Holds a key for a specific amount of time, useful for moving with the W A S D keys 
        """
        self.set_active()
        pyautogui.keyDown(key)
        time.sleep(holdtime)
        pyautogui.keyUp(key)
        return self

    def screenshot(self, name: str, region: Union[Tuple[int, int, int, int], bool] = False) -> None:
        """ 
        - Captures a screenshot of the window and saves it to 'name' 
        - Can also be used the capture specific parts of the window by passing in the region arg. (x, y, width, height) (Relative to the window position) 
        """
        self.set_active()
        # region should be a tuple
        # Example: (x, y, width, height)
        window = self.get_window_rect()
        if not region:
            # Set the default region to the area of the window
            region = window
        else:
            # Adjust the region so that it is relative to the window
            wx, wy = window[:2]
            region = list(region)
            region[0] += wx
            region[1] += wy

        pyautogui.screenshot(f"screenshots/{name}", region=region)

    def match_image(self, largeImg: str, smallImg: str, threshold: float = 0.1, debug: bool = False) -> Union[Tuple[float, float], bool]:
        """ Finds smallImg in largeImg using template matching
            Adjust threshold for the precision of the match (between 0 and 1, the lowest being more precise)
            Returns false if no match was found with the given threshold
        """
        method = cv2.TM_SQDIFF_NORMED

        # Read the images from the file
        small_image = cv2.imread(smallImg)
        large_image = cv2.imread(largeImg)
        w, h = small_image.shape[:-1]

        result = cv2.matchTemplate(small_image, large_image, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        if (mn >= threshold):
            return False

        # Extract the coordinates of our best match
        x, y = mnLoc

        if debug:
            # Draw the rectangle:
            # Get the size of the template. This is the same size as the match.
            trows, tcols = small_image.shape[:2]

            # Draw the rectangle on large_image
            cv2.rectangle(large_image, (x, y),
                          (x + tcols, y + trows), (0, 0, 255), 2)

            # Display the original image with the rectangle around the match.
            cv2.imshow('output', large_image)

            # The image is only displayed if we call this
            cv2.waitKey(0)

        # Return coordinates to center of match
        return (x + (w * 0.5), y + (h * 0.5))
    
    def find_spell(self, spell_name: str, threshold: float = 0.15, max_tries: int = 2, recapture: bool = True) -> Union[Tuple[float, float], bool]:
        """ 
        Attempts the find the spell passed in 'spell_name'
        returns False if not found with the given threshold
        Use recapture=False to not re-take the screenshot of the spell_area
        Adds spell position to memory for later use
        """
        self.set_active()
        tries: int = 0
        res: Union[Tuple[float, float], bool] = False
        while not res and tries < max_tries:
            tries += 1

            if tries > 1:
                # Wait 1 second before re-trying
                self.wait(1)
                recapture = True

            if recapture:
                self.mouse_out_of_area(self._spell_area)
                self.screenshot('spell_area.png', region=self._spell_area)

            res = self.match_image(
                'screenshots/spell_area.png', ('spells/' + spell_name + '.png'), threshold)

        if res is not False:
            x, y = res
            offset_x, offset_y = self._spell_area[:2]
            spell_pos: Tuple[float, float] = (offset_x + x, offset_y + y)
            # Remember location
            self._spell_memory[spell_name] = spell_pos
            return spell_pos
        else:
            return False
        
    def flush_spell_memory(self) -> None:
        """ 
        This action gets called every time there is a destructive action to the spells (The spells change position)
        For example: Casting, Enchanting, Discarding
        """
        self._spell_memory = {}
        return

    def select_spell(self, spell: str) -> Union["Client", bool]:
        """ 
        Clicks on a spell
        Attempts to look in memory to see if we already have found this spell
        Returns False if the spell can't be found
        """
        try:
            spell_pos = self._spell_memory[spell]
        except KeyError:
            spell_pos = self.find_spell(spell)

        if spell_pos is not False:
            self.click(*spell_pos, delay=0.3)
            return self
        else:
            return False
        
    def cast_spell(self, spell: str) -> Union["Client", bool]:
        """ 
        Clicks on the spell and clears memory cache
        if the spell requires a target, chain it with .at_target([enemy_pos])
        """
        if self.find_spell(spell):
            print('casting', spell)
            self.flush_spell_memory()
            return self.select_spell(spell)
        else:
            print("couldn't find", spell)
            return False

    def enchant(self, spell_name: str, enchant_name: str, threshold: float = 0.1, silent_fail: bool = False) -> Union["Client", bool]:
        """ 
        Attempts the enchant 'spell_name' with 'enchant_name'
        """
        if self.find_spell(spell_name, threshold=threshold) and self.find_spell(enchant_name, recapture=False, threshold=threshold):
            print('enchanting', spell_name, 'with', enchant_name)
            self.select_spell(enchant_name)
            self.select_spell(spell_name)
            self.flush_spell_memory()
            return self
        else:
            if not silent_fail:
                print("one or more spells couldn't be found:", spell_name, enchant_name)
            return False
    
    def is_player_idle(self) -> bool:
        """Matches pixel in pet pig icon"""
        return self.pixel_matches_color((152, 559), (252, 146, 206))

    def is_player_turn(self) -> bool:
        """Matches a yellow pixel in the 'pass' button"""
        return self.pixel_matches_color((244, 415), (255, 255, 0), 20)
    
    def wait_for_player_turn(self) -> None:
        while not self.is_player_turn():
            self.wait(1)

    def pass_turn(self) -> None:
        self.click(260, 410)

    def is_mana_low(self) -> bool:
        color = (99, 81, 70)
        pos = (100, 605)
        return self.pixel_matches_color(pos, color, 10)
    
    def has_potion(self) -> bool:
        color = (181,142,41)
        pos = (144, 582)
        return self.pixel_matches_color(pos, color, 10)

    def consume_potion(self) -> None:
        self.click(144, 582)
    
    def teleport_to_commons(self) -> None:
        self.click(633, 580)

    def count_enemies(self) -> int:
        Y = 52
        Xi = 177
        color = (183, 147, 100)
        num_enemies = 0
        for i in range(4):
            X = (171 * i) + 177
            if self.pixel_matches_color((X, Y), color, threshold=30):
                num_enemies += 1

        return num_enemies
def count_windows(name: str = "Wizard101") -> int:
    def win_enum_callback(handle: int, param: list) -> None:
        if name == str(win32gui.GetWindowText(handle)):
            param.append(handle)

    handles: List[int] = []
    # Get all windows with the name "Wizard101"
    win32gui.EnumWindows(win_enum_callback, handles)
    return len(handles)
