
# start chrome using 'chrome.exe --remote-debugging-port=9222'

import time
from selenium import webdriver
from selenium import common

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from copier_utils import *

debug_num_refreshes = 0
# playlist link. add index (e.g. `&index=424`) at the end to start from somewhere in the middle
liked_playlist = "https://www.youtube.com/watch?v=LLyXx7Zmxkg&list=LL_nSEY2566oz2KCsyURIMhQ"
liked_playlist = "https://www.youtube.com/playlist?list=LL_nSEY2566oz2KCsyURIMhQ"
copy_to_playlist_name = "one_two"


def selenium_debug_print_element_tag_name(element):
    debug_print(element.tag_name, song_name)


def click_save(driver):
    delaySec(5, "sleeping before save button", 3)
    save_botton = driver.find_elements_by_xpath("//html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-button-renderer[2]")
    yt_save_button = save_botton[0].find_elements_by_id("button")
    if (selenium_button_click(yt_save_button[0], "save to playlist") == False):
        debug_print("Error Saving to playlist", 1)


def find_checkbox(driver):
    delaySec(3, "sleeping before finding checkbox", 3)

    one_two_checkbox = driver.find_element_by_xpath("//yt-formatted-string[@title='one_two']")
    debug_print("one_two_checkbox found", 4)
    paper_checbox__one_two_checkbox = driver.find_element_by_xpath("//yt-formatted-string[@title='one_two']/../../../..")
    if (paper_checbox__one_two_checkbox.tag_name != "paper-checkbox"):
        debug_print("Failed to get the paper checkbox")
    else:
        debug_print("Got the 'one_two' paper checkbox Successfully !", 4)

    is_checked = paper_checbox__one_two_checkbox.get_attribute("aria-checked")
    print("is_checked is " + str(is_checked))
    if is_checked == 'true':
        debug_print("DOUBLE SUCCESS::: the checkbox is checked", 2)
        #todo this break will soon need to become a 'return' when the oop is removed
    else:
        debug_print("DOUBLE SUCCESS::: the checkbox is NOT NOT NOT 'checked'", 3)
        one_two_checkbox.click()
        delaySec(1, "clicked to add to playlist")


def selenium_find_by_full_xpath(full_xpath):
    tmp_element = driver.find_element_by_xpath(full_xpath)
    return tmp_element


def selenium_button_click(tmp_element, element_name=""):

    try:
        tmp_element.click()
        return True
    except common.exceptions.ElementNotInteractableException:
        print("failed to click '" + str(element_name) + "' button (ElementNotInteractableException) ")
        return False
    except common.exceptions.NoSuchElementException:
        print("failed to click '" + str(element_name) + "' button (NoSuchElementException) ")
        return False
    return False


def selenium_actionchain_shift_N(ac):
    ac.reset_actions()
    ac.send_keys(Keys.SHIFT + 'N')
    ac.perform()


def selenium_actionchain_escape(ac):
    ac.reset_actions()
    ac.send_keys(Keys.ESCAPE)
    ac.perform()


def save_to_playlist(driver, actions):
    # open the 'save to playlist' dialog
    click_save(driver)

    # go over the checkboxes
    # see which checkbox is in a struct with a title "one_two"
    find_checkbox(driver)

    # close dialog
    selenium_actionchain_escape(actions)
    debug_print("closed", song_name, 3)


print("hey, Starting the program")

debug_print("Configuring options", 5)

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
#Change chrome driver path accordingly
chrome_driver = r"C:\Users\asaf\Downloads\Software\chromedriver_win32\chromedriver.exe"
# driver = webdriver.Chrome(chrome_driver, options=chrome_options)
driver = webdriver.Chrome(chrome_driver)

debug_print ("web page title: " + driver.title, 3)

# open the page I gave him (my youtube playlist)
driver.get(liked_playlist)
debug_print ("Got playlist : " + liked_playlist, 2)

song_iter = 0
num_songs_to_save = 400
debug_print("will now copy the first " + str(num_songs_to_save) + " songs", 1)

while song_iter < num_songs_to_save:
    actions = ActionChains(driver)
    song_iter+=1
    delaySec(2, "small delay to let page title update..", 3)
    song_name = driver.title[0:20]
    debug_print("saving song number: " + str(song_iter) + " - " + song_name, 2)

    # save to playlist
    try:
        save_to_playlist(driver, actions)
    except:
        debug_print("Error - Refreshing page", 1)
        debug_num_refreshes+=1
        driver.refresh()
        continue

    # pass to next song
    delaySec(2, "before pressing next button, waiting for player to load", 3)
    selenium_actionchain_shift_N(actions)
    debug_print("moving to next video..", 2)

# End