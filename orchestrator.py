import time
import threading
from datetime import datetime
from data_engine.websocket_client import BinanceEngine
from questionnaires import q2_interest, q1_breakthrough, q3_aggressive, q4_efficiency, q5_hold_logic

class SystemOrchestrator:
    def __init__(self, ui_callback=None):
        self.ui_callback = ui_callback
        self.engine = BinanceEngine()
        self.running = False
        self.active_leads = {
            'q1': {'active': False, 'tries': 0},
            'q3': {'active': False, 'tries': 0}
        }
    
    def log(self, msg, color="#ffffff"):
        print(f"[ORCHESTRATOR]: {msg}")
        if self.ui_callback:
            self.ui_callback(msg, color)

    def start(self):
        """Starts the main engine and the Q2 loop."""
        self.running = True
        
        # Start Data Engine
        threading.Thread(target=self.engine.start, daemon=True).start()
        self.log("BinanceEngine started.", "#3498db")
        
        # Start Q2 Loop (Main Survey)
        threading.Thread(target=self._run_q2_loop, daemon=True).start()
        self.log("Q2 Survey Loop started (10 min interval).", "#3498db")

        # Start Sub-Task Processors (Q1/Q3 checks)
        # We check frequently (e.g. every 1 min) if it's time to run a retry
        threading.Thread(target=self._run_subtask_manager, daemon=True).start()

    def _run_q2_loop(self):
        """Surveys the market every 10 minutes."""
        while self.running:
            try:
                # Wait for data engine to warm up if needed
                if self.engine.last_price == 0:
                    print("DEBUG [ORCHESTRATOR]: Waiting for BinanceEngine to provide price data...")
                    time.sleep(5)
                    continue

                print(f"DEBUG [ORCHESTRATOR]: Q2 Survey iteration started at {datetime.now()}")
                snapshot = self.engine.get_snapshot()
                result = q2_interest.survey_market(snapshot)
                
                self.log(f"Q2 Survey: Points={result['total_points']} Status={result['status']}", result['color'])
                
                if result['trigger_next']:
                    self._trigger_leads()
                
                # Sleep 10 minutes (600 seconds)
                # For testing purposes, we might want to scale time, but let's stick to spec
                time.sleep(600)
                
            except Exception as e:
                self.log(f"Q2 Error: {e}", "#e74c3c")
                print(f"DEBUG [ORCHESTRATOR]: Exception in Q2 loop: {traceback.format_exc()}")
                time.sleep(60)

    def _trigger_leads(self):
        """Activates Q1 and Q3 logic chains."""
        self.log("Lead Generated! Triggering Q1 and Q3 chains...", "#2ecc71")
        
        # Activate Q1
        self.active_leads['q1']['active'] = True
        self.active_leads['q1']['tries'] = 0
        self.active_leads['q1']['last_run'] = 0 # timestamp
        
        # Activate Q3
        self.active_leads['q3']['active'] = True
        self.active_leads['q3']['tries'] = 0
        self.active_leads['q3']['last_run'] = 0

    def _run_subtask_manager(self):
        """Checks if Q1 or Q3 need to run (retry logic)."""
        print("DEBUG [ORCHESTRATOR]: Sub-task manager thread active (Q1/Q3 retries).")
        while self.running:
            now = time.time()
            
            # --- Q1 Logic ---
            q1_state = self.active_leads['q1']
            if q1_state['active']:
                # Run if never run or 5 mins (300s) passed since last run
                if now - q1_state['last_run'] > 300:
                    print(f"DEBUG [ORCHESTRATOR]: Q1 activation detected. Triggering process...")
                    self._process_q1()
                    q1_state['last_run'] = time.time()

            # --- Q3 Logic ---
            q3_state = self.active_leads['q3']
            if q3_state['active']:
                if now - q3_state['last_run'] > 300:
                    print(f"DEBUG [ORCHESTRATOR]: Q3 activation detected. Triggering process...")
                    self._process_q3()
                    q3_state['last_run'] = time.time()
            
            time.sleep(5) # Check state every 5 seconds

    def _process_q1(self):
        state = self.active_leads['q1']
        state['tries'] += 1
        
        print(f"[Q1 CHAIN] Starting attempt {state['tries']}/3...")
        
        if state['tries'] > 3:
            self.log("Q1 Chain: MAX TRIES REACHED. Stopping.", "#e74c3c")
            state['active'] = False
            return

        self.log(f"Q1 Chain: executing attempt {state['tries']}/3...", "#f1c40f")
        snapshot = self.engine.get_snapshot()
        print("[Q1 CHAIN] Got snapshot, calling evaluate_breakthrough...")
        report = q1_breakthrough.evaluate_breakthrough(snapshot, direction="buying") # Defaulting to buying for now
        
        print(f"[Q1 CHAIN] ✓ Evaluation complete. Points={report['total_points']}, Success={report['success']}")
        self.log(f"Q1 Result: Points={report['total_points']} Success={report['success']}", "#f1c40f")

        if report['success']:
            print("[Q1 CHAIN] SUCCESS! Proceeding to Q5...")
            self.log("Q1 SUCCESS! Moving to Q5.", "#2ecc71")
            state['active'] = False
            self._run_q5(snapshot)

    def _process_q3(self):
        state = self.active_leads['q3']
        state['tries'] += 1
        
        print(f"[Q3 CHAIN] Starting attempt {state['tries']}/3...")
        
        if state['tries'] > 3:
            self.log("Q3 Chain: MAX TRIES REACHED. Stopping.", "#e74c3c")
            state['active'] = False
            return

        self.log(f"Q3 Chain: executing attempt {state['tries']}/3...", "#e67e22")
        snapshot = self.engine.get_snapshot()
        print("[Q3 CHAIN] Got snapshot, calling evaluate_aggression...")
        report = q3_aggressive.evaluate_aggression(snapshot)
        
        print(f"[Q3 CHAIN] ✓ Evaluation complete. Points={report['total_points']}, Verdict={report['verdict']}")
        self.log(f"Q3 Result: Points={report['total_points']} Verdict={report['verdict']}", "#e67e22")

        if report['success']:
            print("[Q3 CHAIN] SUCCESS! Proceeding to Q4...")
            self.log("Q3 SUCCESS! Moving to Q4 verification.", "#2ecc71")
            state['active'] = False # Stop retrying Q3
            self._run_q4(snapshot)
            
    def _run_q4(self, snapshot):
        print("[Q4 VERIFY] Starting efficiency verification...")
        self.log("Q4: Verifying Efficiency...", "#9b59b6")
        report = q4_efficiency.verify(snapshot, direction="buying")
        
        print(f"[Q4 VERIFY] ✓ Verification complete. Confirmed={report['confirmed']}")
        if report['confirmed']:
            print("[Q4 VERIFY] CONFIRMED! Proceeding to Q5...")
            self.log("Q4 CONFIRMED. Moving to Q5.", "#2ecc71")
            self._run_q5(snapshot)
        else:
            print("[Q4 VERIFY] REJECTED. Chain terminates.")
            self.log("Q4 REJECTED. Chain ends.", "#e74c3c")

    def _run_q5(self, snapshot):
        print("[Q5 ADVICE] Generating trading consultation...")
        self.log("Q5: Generating Advice...", "#8e44ad")
        advice = q5_hold_logic.generate_advice(snapshot)
        print(f"[Q5 ADVICE] ✓ Consultation ready!")
        print(f"[Q5 ADVICE] Short-term: {advice['verdict_summary']['Short_Term']}")
        print(f"[Q5 ADVICE] Med/Long-term: {advice['verdict_summary']['Medium_Long_Term']}")
        self.log(f"CONSULTATION READY: {advice['verdict_summary']['Short_Term']}", "#9b59b6")
