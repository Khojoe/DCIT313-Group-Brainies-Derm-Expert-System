import customtkinter as ctk
from tkinter import messagebox
from pyswip import Prolog

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class DermExpertGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DermExpert - Skin Disease Diagnosis Pro")
        self.geometry("650x550")
        
        # Initialize Prolog
        self.prolog = Prolog()
        try:
            self.prolog.consult("../knowledge_base/skin_diseases.pl")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load knowledge base: {e}")
            self.destroy()
            return

        self.symptoms_questions = [
            "itching", "circular_rash", "oily_skin", "pimples_with_pus",
            "dry_skin", "inflammation", "thick_silvery_scales", "red_patches",
            "redness", "swelling", "intense_itching", "rashes", "burrows",
            "facial_flushing", "visible_veins", "raised_welts", 
            "asymmetrical_moles", "irregular_borders", "evolving_moles"
        ]
        
        self.current_question_index = 0
        self.reported_symptoms = []
        
        self.setup_ui()

    def setup_ui(self):
        # Header Frame
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray80", "gray20"))
        self.header_frame.pack(fill="x", pady=(0, 20))
        
        self.lbl_title = ctk.CTkLabel(
            self.header_frame, 
            text="DermExpert Pro", 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        )
        self.lbl_title.pack(pady=15)

        self.lbl_disclaimer = ctk.CTkLabel(
            self, 
            text="Disclaimer: This is not medical advice. Always consult a doctor.", 
            text_color="#e74c3c",
            font=ctk.CTkFont(family="Helvetica", size=12, slant="italic")
        )
        self.lbl_disclaimer.pack(pady=5)

        # Question Frame
        self.question_frame = ctk.CTkFrame(self, width=500, height=300, corner_radius=15)
        self.question_frame.pack(pady=20, padx=40, fill="both", expand=True)
        self.question_frame.pack_propagate(False)

        self.lbl_question = ctk.CTkLabel(
            self.question_frame, 
            text="", 
            font=ctk.CTkFont(size=18), 
            wraplength=450
        )
        self.lbl_question.pack(pady=(60, 40))

        # Buttons
        self.btn_frame = ctk.CTkFrame(self.question_frame, fg_color="transparent")
        self.btn_frame.pack()

        self.btn_yes = ctk.CTkButton(
            self.btn_frame, text="Yes", width=120, command=lambda: self.answer("yes"),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_yes.grid(row=0, column=0, padx=20)

        self.btn_no = ctk.CTkButton(
            self.btn_frame, text="No", width=120, command=lambda: self.answer("no"),
            fg_color="#e74c3c", hover_color="#c0392b",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_no.grid(row=0, column=1, padx=20)
        
        # Result Text Area
        self.result_text = ctk.CTkTextbox(self, width=550, height=250, font=ctk.CTkFont(size=14))
        
        self.btn_restart = ctk.CTkButton(
            self, text="Restart Diagnostic", command=self.restart,
            font=ctk.CTkFont(size=14, weight="bold")
        )

        self.ask_question()

    def ask_question(self):
        if self.current_question_index < len(self.symptoms_questions):
            symptom = self.symptoms_questions[self.current_question_index]
            formatted_symptom = symptom.replace("_", " ")
            self.lbl_question.configure(text=f"Do you have {formatted_symptom}?")
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
        self.result_text.pack(pady=20)
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
        
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")

        if diseases:
            self.result_text.insert("end", "Based on your symptoms, possible diagnoses:\n\n")
            unique_diagnoses = set(d['D'] for d in diseases)
            for diag in unique_diagnoses:
                try:
                    conds_query = list(self.prolog.query(f"rule(_, '{diag}', Conditions)"))
                    if conds_query:
                        conds = conds_query[0]['Conditions']
                        cond_str = ", ".join(conds).replace("_", " ")
                        self.result_text.insert("end", f"▶ {diag.capitalize()}: Because you reported: {cond_str}.\n")
                        
                        severity_str = 'Mild' if len(conds) < 3 else 'Moderate'
                        self.result_text.insert("end", f"   Severity: {severity_str} (based on symptom count).\n")
                    
                    adv_query = list(self.prolog.query(f"advice('{diag}', Adv)"))
                    if adv_query:
                        adv = adv_query[0]['Adv']
                        if isinstance(adv, bytes):
                            adv = adv.decode('utf-8')
                        self.result_text.insert("end", f"   Advice: {adv}\n\n")
                except Exception as e:
                    self.result_text.insert("end", f"   Error fetching details: {e}\n\n")
        else:
            self.result_text.insert("end", "No matching diagnosis based on inputs.\nIf symptoms persist, please consult a doctor.")
            
        self.result_text.configure(state="disabled")

    def restart(self):
        try:
            list(self.prolog.query("retractall(fact(_))"))
        except:
            pass
            
        self.reported_symptoms = []
        self.current_question_index = 0
        self.result_text.pack_forget()
        self.btn_restart.pack_forget()
        self.question_frame.pack(pady=20, padx=40, fill="both", expand=True)
        self.ask_question()

if __name__ == "__main__":
    app = DermExpertGUI()
    app.mainloop()
