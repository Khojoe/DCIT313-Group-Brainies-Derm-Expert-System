% Dynamic facts for symptoms and inferred diseases
:- dynamic fact/1.

% Rules: rule(ID, Disease, [Symptoms])
rule(1, ringworm, [itching, circular_rash]).
rule(2, acne, [oily_skin, pimples_with_pus]).
rule(3, eczema, [dry_skin, itching, inflammation]).
rule(4, psoriasis, [thick_silvery_scales, red_patches]).
rule(5, dermatitis, [redness, swelling, itching]).
rule(6, scabies, [intense_itching, rashes, burrows]).

% Preliminary advice (Source-mapped to Mayo Clinic, Cleveland Clinic, CDC)
advice(ringworm, "Likely a fungal infection (CDC). Use over-the-counter antifungal creams to treat mild cases. Also, keep the area dry/clean. Do not use steroid creams as they worsen it. Consult a doctor if severe.").
advice(acne, "Common in oily skin (Mayo Clinic). Wash gently twice a day with a mild cleanser and use OTC benzoyl peroxide or salicylic acid. Avoid scrubbing and tight clothing. See a dermatologist if persistent.").
advice(eczema, "Possible atopic dermatitis (Cleveland Clinic). Moisturize daily, preferably right after bathing, with fragrance-free creams. Avoid known triggers and hot showers. Seek medical advice for strong flare-ups.").
advice(psoriasis, "Chronic skin condition. Moisturize and use soothing topical treatments. Consult a doctor for systemic treatments or light therapy options.").
advice(dermatitis, "General skin irritation. Avoid allergens or triggers, keep skin hydrated, and use anti-itch creams or cool compresses. See a doctor if it persists or blisters form.").
advice(scabies, "Highly contagious mite infestation. Requires prescription medication like permethrin. Wash all bedding and clothing in hot water. Consult a doctor immediately.").

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