from pyswip import Prolog

# Initialize Prolog
prolog = Prolog()
prolog.consult("../knowledge_base/skin_diseases.pl")  

# All unique symptoms from rules 
symptoms_questions = [
    "itching", "circular_rash", "oily_skin", "pimples_with_pus",
    "dry_skin", "inflammation", "thick_silvery_scales", "red_patches",
    "redness", "swelling", "intense_itching", "rashes", "burrows",
    "facial_flushing", "visible_veins", "raised_welts", 
    "asymmetrical_moles", "irregular_borders", "evolving_moles"
]

# Collect user symptoms
print("="*60)
print("Welcome to DermExpert (Command Line Interface)!")
print("Did you know there is now a GUI? Run `python derm_expert_gui.py`!")
print("="*60)
print("Answer yes/no to symptoms. This is not medical advice. See a doctor after this.")
for symptom in symptoms_questions:
    answer = input(f"Do you have {symptom.replace('_', ' ')}? (yes/no): ").strip().lower()
    if answer == "yes":
        prolog.assertz(f"fact({symptom})")

# Run forward chaining
list(prolog.query("forward_chain"))

# Get diagnosed diseases
diseases = list(prolog.query("rule(_, D, _), fact(D)"))

if diseases:
    print("\nBased on your symptoms, possible diagnoses:")
    for diag in set(d['D'] for d in diseases):  # Unique
        # Get explanation (rule conditions)
        conds = list(prolog.query(f"rule(_, '{diag}', Conditions)"))[0]['Conditions']
        cond_str = ", ".join(conds).replace("_", " ")
        print(f"- {diag.capitalize()}: Because you reported: {cond_str}.")
        
        # Get advice
        adv = list(prolog.query(f"advice('{diag}', Adv)"))[0]['Adv']
        print(f"  Preliminary advice: {adv}")
        print(f"  Severity: {'Mild' if len(conds) < 3 else 'Moderate'} (based on symptom count—consult a pro for accurate assessment).")
else:
    print("\nNo matching diagnosis based on inputs. If symptoms persist, consult a doctor.")

# Optional: Reset facts for re-runs (in a real app, use a loop)