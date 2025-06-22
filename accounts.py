import itertools
import os

def ask(prompt, optional=True):
    if optional:
        prompt += " (Press Enter to skip): "
    else:
        prompt += " (Required): "

    ans = input(prompt).strip()
    return ans if ans else (None if optional else ask(prompt, optional))

def build_passwords(words, symbols, limit=1000):
    combos = set()
    for i in range(1, 4):  # Combine 1 to 3 words
        for combo in itertools.permutations(words, i):
            for sym in symbols or [""]:
                combos.add("".join(combo) + sym)
                if len(combos) >= limit:
                    return list(combos)
    return list(combos)

def handle_one_account():
    print("\n⚙️  Starting a new victim profile...\n")

    first_name = ask("Victim's First Name", optional=False)
    title = ask("Title (e.g., jha)")
    nickname = ask("Nickname")
    age = ask("Age")
    dob = ask("Date of Birth (dd-mm-yyyy)")
    country = ask("Country")
    state = ask("State")
    city = ask("City")

    extra_names = []

    fam = ask("Does the victim care deeply about family/friends? (yes/no)", optional=False)
    if fam.lower() == "yes":
        print("\n➕ Enter known names of close ones. (Leave blank to skip any):")
        for label in ["Mother", "Father", "Sister", "Brother", "Best Friend"]:
            name = ask(f"{label}'s Name")
            if name:
                extra_names.append(name)

    games = []
    addicted = ask("Is the victim addicted to games? (yes/no)", optional=False)
    if addicted.lower() == "yes":
        print("🎮 You can add up to 2 games.")
        g1 = ask("   Game 1")
        g2 = ask("   Game 2")
        games += list(filter(None, [g1, g2]))

    symbols_raw = ask("Enter special numbers or symbols (separated by commas, like @,!,123)")
    symbols = [s.strip() for s in symbols_raw.split(",") if s.strip()]

    # Merge everything
    base_words = list(filter(None, [
        first_name, title, nickname, age,
        dob.replace("-", "") if dob else None,
        country, state, city
    ] + extra_names + games))

    if not base_words:
        print("❌ No valid data provided. Skipping.")
        return

    print("\n🔄 Generating password list...")

    passwords = build_passwords(base_words, symbols)
    print(f"✅ {len(passwords)} passwords generated.")

    save = ask("Do you want to save this list to a file? (y/n)", optional=False)
    if save.lower() == "y":
        fname = f"/sdcard/{first_name.lower()}_passwords.txt"

        # Delete old file
        if os.path.exists(fname):
            os.remove(fname)

        try:
            with open(fname, "w") as f:
                f.write("\n".join(passwords))
            print(f"📁 Passwords saved to {fname}")
        except Exception as e:
            print(f"❌ Error saving: {e}")
    else:
        print("🛑 Not saved.")

# ────────────────────────────────────────

print("🔐 Insta Password Generator (Multi Victim Mode) 🔐\n")

while True:
    handle_one_account()
    more = ask("\nDo you want to add another victim? (y/n)", optional=False)
    if more.lower() != "y":
        print("✅ Done. Exiting.")
        break
