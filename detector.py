import doc_analysis
from sys import exit
import os

#user parameters
p = os.path
dir = p.dirname(p.abspath(__file__))
txt_only = True
sensitivity = 5

#app data
SETTINGS_FILE = "settings.set"
WRONG_DIR = "INVALID"
source_dir = str(dir)

def format_dir(dir):
    if not dir.endswith("\\"):
        dir += "\\" 
    return dir.replace("\"","")

fancy_input = lambda prompt: input("\n" + prompt + "\n> ")

def load_default():
    global dir, txt_only, sensitivity

    p = os.path
    dir = p.dirname(p.abspath(__file__))
    txt_only = True
    sensitivity = 5

    save_settings()
    
def load_settings():
    global dir, txt_only, sensitivity

    try:
        in_file = open(os.path.join(source_dir, SETTINGS_FILE), mode = "r")
        settings = in_file.read()
        in_file.close()
    except IOError as ioe:
        print("An error occured while loading the settings. Loading default settings...", ioe)
        load_default()
        return
    
    print(settings)
    for setting in settings.split(): #yes this is inefficient, but it's only 3 settings
        print(settings.split())
        if setting.startswith("dir"):
            dir = setting[setting.find("=")+1:].replace("@"," ")
        elif setting.startswith("txt_only"):
            txt_only = True if setting[setting.find("=")+1:] == '1' else False
        elif setting.startswith("sensitivity"):
            sensitivity = float(setting[setting.find("=")+1:])
        
    if dir == WRONG_DIR:
        dir = source_dir


def save_settings():
    set_to_str = "dir=" + dir.replace(" ","@") + "\ntxt_only=" + str(1 if txt_only else 0) + "\nsensitivity=" + str(sensitivity)
    try:
        out_file = open(os.path.join(source_dir, SETTINGS_FILE), mode = "w")
        out_file.write(set_to_str)
        out_file.close()
    except IOError as ioe:
        print("Error when writing to settings file:", ioe)

def user_setup():
    global dir, txt_only, sensitivity
    OPTIONS_STR = "\nOptions Menu:\n1. Change directory\n2. Select input files by type\n3. Set output sensitivity\n4. Back to main menu"
    changes_made = False

    choice = fancy_input(OPTIONS_STR)

    while True:
        answer = -1

        #select directory
        if choice == '1':
            print(f"Current directory: {dir}\n\nThe input files should be located in this directory.")
            while answer != 'y' and answer != 'n':
                answer = fancy_input("Would you like to change directory? (y/n)").lower()
                if answer == 'y':
                    dir = format_dir(fancy_input("Paste the desired directory here: "))
                    changes_made = True
                    print(changes_made)

        #select file type
        elif choice == '2':
            while answer != '1' and answer != '2':
                answer = fancy_input("1. Use txt files only (default)\n2. Use any non-binary files in the directory")

                if answer == '1':
                    if not txt_only:
                        changes_made = True
                    txt_only = True
                elif answer == '2':
                    print("Please note that some file types might confuse the detector. This shouldn't be an issue for "+
                    "most mark-up languages like HTML.")
                    if txt_only:
                        changes_made = True
                    txt_only = False
        
        #select sensitivity
        elif choice == '3':
            print("The sensitivity score is a measure of how much 2 documents match with each other."+
            "\nA score of 0 would indicate the documents are the same. Scores are relative only to each other."+
            "\nBy adjusting the sensitivity you can determine how ruthless the program is at detecting plagiarized files.")

            while answer <= 0:
                try:
                    answer = float(fancy_input("Please give a value >= 0"))
                except ValueError:
                    answer = -1

            if sensitivity != answer:
                sensitivity = answer
                changes_made = True
        
        #back to main menu
        elif choice == '4':
            print('owo',changes_made)
            return changes_made
        
        choice = fancy_input(OPTIONS_STR)


if __name__ == "__main__":

    load_settings()
    print("This program scans all text files in a given directory and compares each one to all others as to find " +
    "the pairs that are more likely to have copied / plagiariazed text.\n"
    )

    print(f"\nCurrent directory: {dir}\nSearch only txt files: {txt_only}\nDetection sensitivity: {sensitivity}")
    choice = fancy_input("\nType 'O' for options.\nPress any other key to continue")
    
    if choice.lower() == 'o':
        if user_setup(): #if changes were made
            save_settings()
    
    try:
        pairs = doc_analysis.TFIDF(dir, txt_only,[os.path.basename(__file__), os.path.basename(doc_analysis.__file__), SETTINGS_FILE])
    except FileNotFoundError as exc:
        print("\nError: Could not find the data files!", exc)
        dir = WRONG_DIR #flush invalid directory
        save_settings()
        exit(1)
    except ValueError as ve:
        print(ve)
        exit(1)

    if pairs[0].score > sensitivity:
        print("\nNo suspicious files detected", pairs[0].score)
    else:
        print("\nResults sorted by decreasing degree of suspicion (with 0 being a clear-cut copy):")
        for pair in pairs:
            if pair.score > sensitivity:
                break
            print(pair)
