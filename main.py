# main.py

from bot_tele import BotTelegram
import requests
import time

if __name__ == '__main__':
    # Initialize BotTelegram object
    bot_telegram = BotTelegram()

    offset = 0
    while True:
        try:
            response = bot_telegram.send_telegram_request("getUpdates", {"offset": offset, "timeout": 30})
            if response["ok"]:
                for result in response["result"]:
                    bot_telegram.process_message(result.get("message", {}))
                    if "callback_query" in result:
                        bot_telegram.handle_button_click(result["callback_query"])
                    offset = result["update_id"] + 1
            # else:
            #     print("Failed to get updates:", response)
        except requests.exceptions.ConnectionError as e:
            print("Connection error occurred:", e)
            # Wait for a short period before retrying
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            # Handle other request-related errors as needed
            break
        except Exception as e:
            print("An unexpected error occurred:", e)
            break
    bot_telegram.close_arduino_connection()  # Close Arduino connection when the program ends
