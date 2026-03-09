% Dynamic facts for symptoms and inferred diseases
:- dynamic fact/1.

% Rules: rule(ID, Disease, [Symptoms])
rule(1, ringworm, [itching, circular_rash]).
rule(2, acne, [oily_skin, pimples_with_pus]).
rule(3, eczema, [dry_skin, itching, inflammation]).
rule(4, psoriasis, [thick_silvery_scales, red_patches]).
rule(5, dermatitis, [redness, swelling, itching]).
rule(6, scabies, [intense_itching, rashes, burrows]).

% Preliminary advice (not a substitute for medical care)
advice(ringworm, "Likely fungal infection. Consult a doctor for antifungal creams. Keep the area dry and clean.").
advice(acne, "Common in oily skin. Wash gently with mild soap; consider over-the-counter benzoyl peroxide. See a dermatologist if severe.").
advice(eczema, "Manage dryness with moisturizers. Avoid irritants; use steroid creams if prescribed. Seek medical advice.").
advice(psoriasis, "Chronic condition. Moisturize and use topical treatments. Consult a doctor for options like light therapy.").
advice(dermatitis, "Avoid triggers like allergens. Use anti-itch creams and cool compresses. See a doctor if it persists.").
advice(scabies, "Highly contagious mite infestation. Requires prescription medication like permethrin. Wash all bedding/clothes. Consult a doctor immediately.").

% Forward chaining inference engine
forward_chain :-
  findall(Conc-ID, (rule(ID, Conc, Conditions),
                    forall(member(C, Conditions), fact(C)),
                    \+ fact(Conc)), ToAdd),
  (ToAdd \= [] ->
      forall(member(Conc-ID, ToAdd), assertz(fact(Conc))),
      forward_chain
  ;   true
  ).