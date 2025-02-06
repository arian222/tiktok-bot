import logging
import random
import os
import sys
import time
from typing import Optional
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.common.exceptions import WebDriverException
import threading

# Disable webdriver-manager logs
os.environ['WDM_LOG_LEVEL'] = '0'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tiktok_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TikTokBotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("ALECS TikTok Bot")
        self.geometry("800x600")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize bot as None
        self.bot = None
        self.is_running = False
        
        # Create GUI elements
        self.create_gui()
        
    def create_gui(self):
        # Create main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            title_frame, 
            text="ALECS TikTok Bot",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=10)
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Created by ALECS",
            font=ctk.CTkFont(size=14)
        )
        subtitle.pack()
        
        # Input frame
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # URL Input
        url_label = ctk.CTkLabel(input_frame, text="TikTok URL:")
        url_label.pack(anchor="w", pady=(10, 0))
        
        self.url_entry = ctk.CTkEntry(input_frame, width=400, placeholder_text="Enter TikTok URL here...")
        self.url_entry.pack(fill="x", pady=(5, 10))
        
        # Bot Type Selection
        type_label = ctk.CTkLabel(input_frame, text="Select Action Type:")
        type_label.pack(anchor="w", pady=(10, 0))
        
        self.bot_type = ctk.CTkSegmentedButton(
            input_frame,
            values=["Views", "Hearts", "Followers"],
            command=self.on_bot_type_change
        )
        self.bot_type.pack(fill="x", pady=(5, 10))
        self.bot_type.set("Views")
        
        # Delay Settings
        delay_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        delay_frame.pack(fill="x", pady=10)
        
        delay_label = ctk.CTkLabel(delay_frame, text="Delay Range (seconds):")
        delay_label.pack(anchor="w")
        
        delay_inputs = ctk.CTkFrame(delay_frame, fg_color="transparent")
        delay_inputs.pack(fill="x", pady=(5, 0))
        
        self.min_delay = ctk.CTkEntry(delay_inputs, width=100, placeholder_text="Min")
        self.min_delay.pack(side="left", padx=(0, 10))
        self.min_delay.insert(0, "30")
        
        self.max_delay = ctk.CTkEntry(delay_inputs, width=100, placeholder_text="Max")
        self.max_delay.pack(side="left")
        self.max_delay.insert(0, "60")
        
        # Number of Actions
        actions_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=10)
        
        actions_label = ctk.CTkLabel(actions_frame, text="Number of Actions (empty for infinite):")
        actions_label.pack(anchor="w")
        
        self.num_actions = ctk.CTkEntry(actions_frame, width=100)
        self.num_actions.pack(anchor="w", pady=(5, 0))
        
        # Status and Control Frame
        status_frame = ctk.CTkFrame(self.main_frame)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to start...",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=10)
        
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(status_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)
        
        # Control Buttons
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start Bot",
            command=self.start_bot,
            width=200
        )
        self.start_button.pack(side="left", padx=10, expand=True)
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Stop Bot",
            command=self.stop_bot,
            width=200,
            state="disabled"
        )
        self.stop_button.pack(side="right", padx=10, expand=True)
        
        # Footer
        footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        footer_frame.pack(fill="x", pady=20)
        
        footer_text = ctk.CTkLabel(
            footer_frame,
            text="Created by ALECS © 2024",
            font=ctk.CTkFont(size=10)
        )
        footer_text.pack()
        
    def on_bot_type_change(self, value):
        logger.info(f"Bot type changed to: {value}")
        
    def update_status(self, message, is_error=False):
        self.status_label.configure(
            text=message,
            text_color="red" if is_error else "white"
        )
        
    def start_bot(self):
        if not self.url_entry.get():
            self.update_status("Please enter a TikTok URL!", True)
            return
            
        self.is_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        # Get number of actions
        num_actions = self.num_actions.get()
        num_actions = int(num_actions) if num_actions else None
        
        # Create bot instance
        try:
            self.bot = TikTokBot(
                video_url=self.url_entry.get(),
                action_type=self.bot_type.get(),
                min_delay=int(self.min_delay.get()),
                max_delay=int(self.max_delay.get())
            )
            
            # Start bot in a separate thread
            self.bot_thread = threading.Thread(
                target=self.run_bot,
                args=(num_actions,)
            )
            self.bot_thread.daemon = True
            self.bot_thread.start()
            
            self.update_status("Bot started successfully!")
            
        except Exception as e:
            self.update_status(f"Error starting bot: {str(e)}", True)
            self.stop_bot()
        
    def stop_bot(self):
        self.is_running = False
        self.update_status("Stopping bot...")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        if self.bot:
            try:
                self.bot.driver.quit()
            except:
                pass
            self.bot = None
        
    def run_bot(self, num_actions):
        try:
            self.bot.run(num_actions)
        except Exception as e:
            self.update_status(f"Bot error: {str(e)}", True)
        finally:
            self.stop_bot()

class TikTokBot:
    def __init__(self, video_url, action_type='Views', min_delay=30, max_delay=60):
        """Initialize TikTok Bot"""
        self.video_url = video_url
        self.action_type = action_type
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        """Configure and initialize Chrome WebDriver with stealth mode"""
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument('--disable-popup-blocking')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--silent')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option("detach", True)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            stealth(self.driver,
                   languages=["en-US", "en"],
                   vendor="Google Inc.",
                   platform="Win32",
                   webgl_vendor="Intel Inc.",
                   renderer="Intel Iris OpenGL Engine",
                   fix_hairline=True)
            
            logger.info("WebDriver initialized successfully with stealth mode")
        except Exception as e:
            logger.error(f"Error setting up WebDriver: {str(e)}")
            raise

    def solve_captcha(self):
        """Handle CAPTCHA detection and waiting"""
        try:
            max_attempts = 3
            attempt = 0
            while attempt < max_attempts:
                try:
                    captcha_button = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Continue')]"))
                    )
                    logger.info("Waiting for CAPTCHA resolution...")
                    time.sleep(5)
                except:
                    logger.info("CAPTCHA resolved or not present")
                    break
                attempt += 1
        except Exception as e:
            logger.error(f"Error in CAPTCHA handling: {str(e)}")

    def perform_action(self):
        """Perform TikTok action (views, hearts, followers)"""
        try:
            self.solve_captcha()

            # Wait for page to be fully loaded
            time.sleep(10)  # Increased initial wait time

            # Click appropriate action button with retry
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    # Find and click the action button
                    action_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{self.action_type}')]"))
                    )
                    action_button.click()
                    logger.info(f"Found and clicked {self.action_type} button")
                    break
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed to click {self.action_type} button. Retrying...")
                    time.sleep(2)

            time.sleep(5)  # Increased wait time after clicking service button

            # Input URL with retry
            for attempt in range(max_attempts):
                try:
                    # Find and fill the URL input
                    input_field = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
                    )
                    input_field.clear()
                    input_field.send_keys(self.video_url)
                    logger.info("URL entered successfully")
                    break
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed to enter URL. Retrying...")
                    time.sleep(2)

            time.sleep(3)

            # Click Search with retry
            for attempt in range(max_attempts):
                try:
                    search_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search')]"))
                    )
                    search_button.click()
                    logger.info("Clicked search button")
                    break
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed to click search. Retrying...")
                    time.sleep(2)

            time.sleep(5)

            # Click Send with retry
            for attempt in range(max_attempts):
                try:
                    send_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send')]"))
                    )
                    send_button.click()
                    logger.info("Clicked send button")
                    break
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed to click send. Retrying...")
                    time.sleep(2)
            
            logger.info(f"{self.action_type} sent successfully!")
            delay = random.randint(self.min_delay, self.max_delay)
            time.sleep(delay)
            
            try:
                self.driver.refresh()
                time.sleep(5)
            except:
                logger.warning("Failed to refresh page, continuing anyway...")

        except Exception as e:
            logger.error(f"Error performing {self.action_type} action: {str(e)}")
            try:
                self.driver.save_screenshot(f"error_{int(time.time())}.png")
                logger.info("Screenshot saved")
            except:
                pass
            try:
                self.driver.refresh()
                time.sleep(10)
            except:
                pass

    def run(self, num_actions=None):
        """Run the bot for specified number of actions or indefinitely"""
        try:
            # Navigate to the website
            self.driver.get("https://vipto.de/")
            time.sleep(5)

            action_count = 0
            while True:
                if num_actions and action_count >= num_actions:
                    break
                    
                self.perform_action()
                action_count += 1
                logger.info(f"Completed {action_count} actions")

        except Exception as e:
            logger.error(f"Error in bot execution: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()

def main():
    app = TikTokBotGUI()
    app.mainloop()

if __name__ == "__main__":
    main()