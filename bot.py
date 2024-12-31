
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import re  # Import regex for extracting usernames
from selenium.common.exceptions import StaleElementReferenceException

# Setup WebDriver
driver_path = "chromedriver-win64\\chromedriver.exe"  # Ensure this path is correct
service = Service(driver_path)  # Create a Service object
driver = webdriver.Chrome(service=service)  # Pass the Service object to the WebDriver

# Login to Twitter
def login_to_twitter(username, password, user_id):
    driver.get("https://twitter.com/login")
    time.sleep(10)
    username_field = driver.find_element(By.NAME, "text")
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(10)
    username_field = driver.find_element(By.NAME, "text")
    username_field.send_keys(user_id)
    username_field.send_keys(Keys.RETURN)
    time.sleep(10)
    
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

# Check Mentions
def check_mentions():
    driver.get("https://twitter.com/notifications/mentions")
    time.sleep(5)
    mentions = driver.find_elements(By.XPATH, "//article")  # Adjust the XPath to locate tweets
    if mentions:
        # Get the text of the most recent mention
        most_recent_mention = mentions[0]
        print("Most recent mention: " + most_recent_mention.text)
        # Use regex to find the username in the mention text
        match = re.search(r'@(\w+)', most_recent_mention.text)
        if match:
            return match.group(1), most_recent_mention  # Return the username and the mention element
    return None, None  # Return None if no mentions are found

# Take Screenshot of a Profile
def screenshot_profile(username):
    print("Received username to take screenshot: " + str(username))
    driver.get(f"https://twitter.com/{username}")
    time.sleep(5)  # Wait for the page to load
    file_name = f"{username}_profile.png"
    success = driver.save_screenshot(file_name)
    if success:
        print(f"Screenshot saved as {file_name}")
        return file_name  # Return the file name of the screenshot
    else:
        print("Failed to save screenshot")
        return None

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



import os  # Import to handle file paths

def reply_to_tweet(tweet_url, reply_text, screenshot_path=None):
    try:
        # Navigate to the tweet's URL
        driver.get(tweet_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']"))
        )

        # Locate the reply text area
        reply_box = driver.find_element(By.XPATH, "//div[@data-testid='tweetTextarea_0']")
        reply_box.click()
        time.sleep(1)
        reply_box.send_keys(reply_text)

        # Attach a screenshot if provided
        if screenshot_path:
            # Convert the relative path to an absolute path
            absolute_path = os.path.abspath(screenshot_path)
            # Locate the file input for uploading media
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(absolute_path)
            time.sleep(3)  # Wait for the file to upload

        # Click the reply button
        tweet_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButtonInline']"))
        )
        tweet_button.click()
        print("Reply sent successfully")
    except Exception as e:
        print(f"Error while replying to tweet: {e}")


def main():
    username = "suyashgupta001122@gmail.com"
    password = "Ramji@123"
    user_id = "SoyashGupt29647"
    login_to_twitter(username, password, user_id)
    recent_username, recent_mention = check_mentions()
    
    if recent_username and recent_mention:
        print("Most recent username: " + recent_username)

        # Extract the tweet URL from the mention element
        tweet_url = recent_mention.find_element(By.XPATH, ".//a[contains(@href, '/status/')]").get_attribute("href")

        screenshot_path = screenshot_profile(recent_username)  # Take a screenshot of the most recent mentioned user

        if screenshot_path:
            reply_text = f"Thanks for the mention, @{recent_username}! Here's a screenshot of your profile."
            reply_to_tweet(tweet_url, reply_text, screenshot_path)  # Use the tweet URL instead of the element
    else:
        print("No recent mentions found.")


if __name__ == "__main__":
    main()