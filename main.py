import subprocess
import time
import random
import sys
from datetime import datetime, timedelta
from logger import write_log

def get_random_delay_minutes():
    return random.randint(30, 600)

def run_wheel_script():
    try:
        write_log("Lancement de wheel.py...", "info")
        result = subprocess.run([sys.executable, "wheel.py"], capture_output=False)
        write_log(f"wheel.py terminé avec code: {result.returncode}", "info")
        return result.returncode == 0
    except Exception as e:
        write_log(f"Erreur lors de l'exécution: {e}", "error")
        return False

def main():
    write_log("=== Scheduler pour wheel.py ===", "info")
    write_log("Exécution toutes les 24h + 0-10min aléatoires", "info")
    write_log(None, "space")
    
    while True:
        run_wheel_script()
        
        base_delay = 24 * 60 * 60  # 24 heures en secondes
        random_delay = get_random_delay_minutes()
        total_delay = base_delay + random_delay
        
        next_run = datetime.now() + timedelta(seconds=total_delay)
        
        write_log(f"Prochaine exécution dans {total_delay // 3600}h {(total_delay % 3600) / 60:.1f}min", "info")
        write_log(f"Prochaine exécution prévue: {next_run.strftime('%Y-%m-%d %H:%M:%S')}", "info")
        write_log(None, "space")
        
        time.sleep(total_delay)

if __name__ == "__main__":
    main()