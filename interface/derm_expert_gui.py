import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

class DermExpertGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DermExpert - Skin Disease Diagnosis")
        self.root.geometry("600x500")
        self.root.configure(bg="#f4f4f9")
        
        # Initialize Prolog
        self.prolog = Prolog()
        try:
            self.prolog.consult("../knowledge_base/skin_diseases.pl")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load knowledge base: {e}")
            self.root.destroy()
            return
            
        self.symptoms_questions = [
            "itching", "circular_rash", "oily_skin", "pimples_with_pus",
            "dry_skin", "inflammation", "thick_silvery_scales", "red_patches",
            "redness", "swelling", "intense_itching", "rashes", "burrows"
        ]
        
        self.current_question_index = 0
        self.reported_symptoms = []
        
        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        header_frame.pack(fill=tk.X)
        tk.Label(
            header_frame, 
            text="DermExpert", 
            font=("Helvetica", 18, "bold"), 
            bg="#2c3e50", 
            fg="white"
        ).pack()
        
        tk.Label(
            self.root, 
            text="Disclaimer: This is not medical advice. Always consult a doctor.", 
            font=("Helvetica", 10, "italic"), 
            bg="#f4f4f9", 
            fg="#e74c3c"
        ).pack(pady=10)

        # Question Frame
        self.question_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.question_frame.pack(pady=30, fill=tk.BOTH, expand=True)

        self.lbl_question = tk.Label(
            self.question_frame, 
            text="", 
            font=("Helvetica", 14), 
            bg="#f4f4f9", 
            wraplength=500
        )
        self.lbl_question.pack(pady=20)

        # Buttons
        btn_frame = tk.Frame(self.question_frame, bg="#f4f4f9")
        btn_frame.pack(pady=10)

        self.btn_yes = ttk.Button(btn_frame, text="Yes", command=lambda: self.answer("yes"))
        self.btn_yes.grid(row=0, column=0, padx=10)

        self.btn_no = ttk.Button(btn_frame, text="No", command=lambda: self.answer("no"))
        self.btn_no.grid(row=0, column=1, padx=10)
        
        # Result Text Area
        self.result_text = tk.Text(self.root, height=10, width=65, state=tk.DISABLED, font=("Helvetica", 11))
        self.result_text.pack(pady=10)
        self.result_text.pack_forget() # Hide initially

        self.btn_restart = ttk.Button(self.root, text="Restart Diagnostic", command=self.restart)
        self.btn_restart.pack(pady=10)
        self.btn_restart.pack_forget()

        self.ask_question()

    def ask_question(self):
        if self.current_question_index < len(self.symptoms_questions):
            symptom = self.symptoms_questions[self.current_question_index]
            formatted_symptom = symptom.replace("_", " ")
            self.lbl_question.config(text=f"Do you have {formatted_symptom}?")
        else:
            self.process_diagnosis()

    def answer(self, ans):
        if ans == "yes":
            symptom = self.symptoms_questions[self.current_question_index]
            self.reported_symptoms.append(symptom)
        self.current_question_index += 1
        self.ask_question()

    def process_diagnosis(self):
        self.question_frame.pack_forget()
        self.result_text.pack(pady=10)
        self.btn_restart.pack(pady=10)
        
        # Assert facts
        for symptom in self.reported_symptoms:
            try:
                self.prolog.assertz(f"fact({symptom})")
            except Exception:
                pass

        # Run forward chaining
        list(self.prolog.query("forward_chain"))

        # Get diagnosed diseases
        diseases = list(self.prolog.query("rule(_, D, _), fact(D)"))
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        if diseases:
            self.result_text.insert(tk.END, "Based on your symptoms, possible diagnoses:\n\n")
            unique_diagnoses = set(d['D'] for d in diseases)
            for diag in unique_diagnoses:
                # Get conditions
                try:
                    conds_query = list(self.prolog.query(f"rule(_, '{diag}', Conditions)"))
                    if conds_query:
                        conds = conds_query[0]['Conditions']
                        cond_str = ", ".join(conds).replace("_", " ")
                        self.result_text.insert(tk.END, f"- {diag.capitalize()}: Because you reported: {cond_str}.\n")
                        
                        severity_str = 'Mild' if len(conds) < 3 else 'Moderate'
                        self.result_text.insert(tk.END, f"  Severity: {severity_str} (based on symptom count).\n")
                    
                    # Get advice
                    adv_query = list(self.prolog.query(f"advice('{diag}', Adv)"))
                    if adv_query:
                        adv = adv_query[0]['Adv']
                        if isinstance(adv, bytes):
                            adv = adv.decode('utf-8')
                        self.result_text.insert(tk.END, f"  Advice: {adv}\n\n")
                except Exception as e:
                    self.result_text.insert(tk.END, f"  Error fetching details: {e}\n\n")
        else:
            self.result_text.insert(tk.END, "No matching diagnosis based on inputs.\nIf symptoms persist, please consult a doctor.")
            
        self.result_text.config(state=tk.DISABLED)

    def restart(self):
        # Retract all facts
        try:
            list(self.prolog.query("retractall(fact(_))"))
        except:
            pass
            
        self.reported_symptoms = []
        self.current_question_index = 0
        self.result_text.pack_forget()
        self.btn_restart.pack_forget()
        self.question_frame.pack(pady=30, fill=tk.BOTH, expand=True)
        self.ask_question()

if __name__ == "__main__":
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 11), padding=6)
    
    app = DermExpertGUI(root)
    root.mainloop()
