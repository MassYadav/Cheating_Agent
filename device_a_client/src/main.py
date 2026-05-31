"""Passive stealth runtime client listening for system hotkey invocation triggers."""
import asyncio
import logging
import sys
from pynput import keyboard
from src.capture import StealthScreenScanner
from src.transport import NetworkTransportClient
from src.ocr_engine import screen_ocr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("client.main")

scanner = StealthScreenScanner()
network_pipe = NetworkTransportClient(host="127.0.0.1", port=8000)

async_loop = asyncio.new_event_loop()
asyncio.set_event_loop(async_loop)

is_processing = False

def trigger_stealth_analysis_sequence():
    global is_processing
    if is_processing:
        logger.warning("[!] Analysis loop already actively running. Ignoring duplicate trigger request.")
        return
        
    logger.info("[!] Global Stealth Hotkey Detected. Initiating analysis thread...")
    is_processing = True
    asyncio.run_coroutine_threadsafe(execute_live_frame_processing(), async_loop)

async def execute_live_frame_processing():
    global is_processing
    print("\n" + "*"*50)
    print("[*] PROCESSING LIVE SCREEN FRAME NOW...")
    print("*"*50)
    
    try:
        raw_frame_bytes = scanner.capture_frame_to_bytes(compression_quality=85)
        if not raw_frame_bytes:
            logger.error("Aborting sequence. Captured frame matrix buffer returned null pointers.")
            return

        extracted_problem_text = screen_ocr.extract_text_from_jpeg_bytes(raw_frame_bytes)
        if not extracted_problem_text or len(extracted_problem_text) < 10:
            logger.warning("OCR detected insufficient character data thresholds.")
            return

        logger.info("Transmitting live contextual telemetry matrices over network interfaces...")
        response_packet = await network_pipe.dispatch_payload_to_backend(extracted_problem_text)
        
        if response_packet:
            print("\n" + "="*60)
            print(f"[{response_packet.get('domain_evaluated')}] LIVE COMPUTATION RESULT:")
            print(response_packet.get("payload"))
            print("="*60 + "\n")
        else:
            logger.error("Upstream compute nodes timed out or refused execution blocks.")
    except Exception as general_fault:
        logger.error(f"Runtime execution error inside core loop: {str(general_fault)}")
    finally:
        is_processing = False
        print("[*] System returns to passive monitoring standby mode.")

def start_keyboard_hook_daemon():
    shortcut_map = keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+x': trigger_stealth_analysis_sequence
    })
    shortcut_map.start()
    logger.info("Global OS Hook Keyboard Listener Daemon successfully launched.")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("STEALTH COGNITIVE CLIENT IS RUNNING PASSIVELY IN MEMORY")
    print("Press [Ctrl + Shift + X] anywhere to parse your live screen data.")
    print("Press CTRL+C here to terminate client daemon processes safely.")
    print("="*60 + "\n")
    
    start_keyboard_hook_daemon()
    
    try:
        async_loop.run_forever()
    except KeyboardInterrupt:
        print("\n[+] Stealth client daemon shutdown protocol completed successfully.")