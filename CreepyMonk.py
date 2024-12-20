import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QMainWindow, QSplitter
from PyQt5.QtGui import QTextCursor, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for both development and PyInstaller.
    :param relative_path: Relative file path to the resource
    :return: Absolute file path
    """
    # Adjust for images directory
    relative_path = os.path.join("images", relative_path)

    if hasattr(sys, '_MEIPASS'):  # When bundled with PyInstaller
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)


class AdventureGame(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window size to 50% of the screen
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 0.6)
        height = int(screen.height() * 0.6)
        self.resize(width, height)

        self.setWindowTitle('COLOURFUL WOMEN IN AMBROSIO’S LIFE')
        self.start_screen()

        self.location_full_names = {
            'purgatory': 'Purgatory',
            'elvira': 'Elvira\'s Apartment',
            'matilda': 'Matilda in the Monastery',
            'antonia': 'Antonia\'s Tomb'
        }
        self.end_paragraphs1 = [
            "Ambrosio blinked as the air around him grew still and heavy, the suffocating weight of judgment returning. The faint glow of divine light "
            "illuminated the vast, ethereal space, and before him stood the canvas—blank, waiting, and unrelenting.<br>",

            "God: Your journey is complete, Ambrosio. Now, face the truth of your sins. Take the brush, and let your hand reveal what lies within your soul.<br>",

            "The painting hovered before him, incomplete but alive with swirling colors—black for death, red for violence, white for innocence, gold for ambition, "
            "sable for deceit, and rose for faith betrayed. Ambrosio stood trembling, the brush in his hand as his voice broke the silence.<br>",

            "\"I see it now. The power I held was never mine to take. Elvira, Matilda, Antonia—they trusted me, and I betrayed them. I should have been their protector, "
            "their guide, but I destroyed their faith, their love, and their innocence. This painting is my soul laid bare—my punishment and my confession. Let it stand not "
            "only for my sins but as a warning to all who would misuse power. I see my pride, my cruelty, my sin. For that, I repent, and for that, I accept judgment.\"<br>",

            "With trembling hands, Ambrosio raised the brush and made the final stroke. The swirling colors stilled, and the image emerged: a towering man shrouded in shadow, "
            "holding a limp, veiled woman. Her sorrowful figure seemed alive, her delicate frame a silent accusation, while his looming presence radiated guilt and unrelenting power.<br>",

            "The painting pulsed with light, sharp and piercing, its glow illuminating the void. Slowly, Ambrosio reached for the brush one last time and signed his name at the bottom "
            "of the canvas. As the final mark dried, the canvas began to rise, hovering in the air.<br>",

            "Ambrosio fell to his knees, bowing his head before the painting. His voice, low but resolute, filled the space:<br>",

            "\"I will write a sonnet—a warning to any who see this work, a testament to the ruin pride and power can bring. Let my words and this painting speak together, so no soul "
            "walks the path I have tread.\"<br>",

            "The painting glowed faintly, its light softening, as though awaiting its companion words.<br>",
        ]
        self.end_paragraphs2 = [
            "Ambrosio gazed upon the painting, his voice low and heavy with remorse:<br>",

            "\"Men and monks alike wield great power over women, a power that shapes their lives in ways we often fail to see. Their well-being, their dignity, so often rests in our hands, "
            "and it is our choice to either uplift them with grace or crush them with control. As in a dance, men and women are partners in life, moving together in balance and trust. One leads, "
            "the other follows, but neither can thrive without the other.<br>",

            "To hold such power is not a privilege but a sacred responsibility, a duty to protect, to guide with care. Yet I—driven by pride, blinded by lust—turned trust into chains and harmony "
            "into ruin. This painting speaks not only of grace but of the fragility of control. Let it remind all who see it that life itself is a dance, and power, when wielded with cruelty, "
            "destroys not only the one held but also the one who holds. Let us learn to carry others gently, lest we fall together into darkness.\"<br>"
        ]
        self.final_text = [
            "The void dissolved, and the painting descended, its glow dimming to a faint, steady pulse. "
            "The swirling colors—black, red, white, gold, sable, and rose—settled into sharp clarity, each stroke "
            "vivid and alive. The light faded entirely, leaving the painting hovering in silence, its weight undeniable.<br>",

            "The scene shifted to a small, austere cell. The bare stone walls were cold and unadorned, save for a "
            "simple cot and a wooden desk. Above the desk hung the Madonna, her serene visage framed in candlelight, "
            "a silent witness to the faith and ambition that once filled the room.<br>",

            "Two monks entered, their steps quiet as they carried the new painting into the cell. Without a word, "
            "they removed the Madonna, lowering her gently to the floor. The new canvas was hung in her place, its "
            "heavy frame settling into the stone wall as though it had always belonged there.<br>",

            "The image emerged in the dim light: a towering man holding a veiled woman, her body limp in his arms. "
            "Her sorrowful figure seemed to drift between light and shadow, while the man’s form loomed with equal parts "
            "guilt and power. The colors glowed faintly—black shrouding the edges, red streaking through the heart, white "
            "barely visible in the veil, and gold, sable, and rose pulsing with quiet menace.<br>",

            "A novice stepped through the doorway, his robe trailing on the floor. He stopped abruptly, his breath catching "
            "as his gaze fell upon the painting. The room felt heavier, the flickering candlelight bending faintly toward the "
            "canvas as though drawn to it.<br>",

            "The novice knelt, his head bowed low. The silence in the room was absolute, broken only by the faint rustle of "
            "fabric as he remained there, motionless.<br>",

            "Above him, the painting hung, its glow subtle yet unyielding. The Madonna was gone, her gentleness replaced by "
            "the unspoken weight of what now remained.<br>"
        ]
        self.intro_paragraphs = [
            "'What?' He cried, darting at him a look of fury: 'Dare you still implore the Eternal's mercy? Would you feign penitence, and again "
            "act an Hypocrite's part? Villain, resign your hopes of pardon. Thus I secure my prey!'",

            "As He said this, darting his talons into the Monk's shaven crown, He sprang with him from the rock. The Caves and mountains rang "
            "with Ambrosio's shrieks. The Daemon continued to soar aloft, till reaching a dreadful height, He released the sufferer. Headlong "
            "fell the Monk through the airy waste; The sharp point of a rock received him; and He rolled from precipice to precipice, till bruised "
            "and mangled He rested on the river's banks.",

            "Life still existed in his miserable frame: He attempted in vain to raise himself; His broken and dislocated limbs refused to perform "
            "their office, nor was He able to quit the spot where He had first fallen. The Sun now rose above the horizon; Its scorching beams darted "
            "full upon the head of the expiring Sinner. Myriads of insects were called forth by the warmth; They drank the blood which trickled from "
            "Ambrosio's wounds; He had no power to drive them from him, and they fastened upon his sores, darted their stings into his body, covered him "
            "with their multitudes, and inflicted on him tortures the most exquisite and insupportable. The Eagles of the rock tore his flesh piecemeal, "
            "and dug out his eyeballs with their crooked beaks.",

            "A burning thirst tormented him; He heard the river's murmur as it rolled beside him, but strove in vain to drag himself towards the sound. "
            "Blind, maimed, helpless, and despairing, venting his rage in blasphemy and curses, execrating his existence, yet dreading the arrival of death "
            "destined to yield him up to greater torments, six miserable days did the Villain languish.",

            "On the Seventh a violent storm arose: The winds in fury rent up rocks and forests: The sky was now black with clouds, now sheeted with fire: "
            "The rain fell in torrents; It swelled the stream; The waves overflowed their banks; They reached the spot where Ambrosio lay, and when they "
            "abated carried with them into the river the Corse of the despairing Monk.",

            "- The above was text from Matthew Lewis', <i>The Monk</i>",

            "Darkness swallows Ambrosio as he writhes upon jagged stones that dig mercilessly into his flesh. The suffocating stench of sulfur fills the air, "
            "acrid and choking, mingling with the ceaseless wails of despair that echo like an endless dirge. The oppressive heat scorches his skin, yet offers no light, "
            "leaving him blind to the desolation around him. The faint taste of ash clings to his tongue, dry and bitter.<br>",

            "Then, through the unyielding blackness, a light begins to grow—a sharp, otherworldly brilliance that cuts through the dark. It illuminates nothing yet feels alive, "
            "its clarity piercing yet cool, unlike the searing flames of Hell. Ambrosio shields his eyes with trembling hands. A voice follows, deep and resonant, steady as the toll "
            "of a cathedral bell. It fills the air, at once calming and unrelenting.<br>",

            "\"Ambrosio, my lost and wayward child, you are now in purgatory.\"<br>",

            "The monk trembled, recognizing divinity. His hands, instruments of sin and ambition, now reached toward the light. “Who speaks?” he croaked, his voice hoarse. "
            "“Who dares disturb my torment?”<br>",

            "<b>God:</b> I am the Shepherd who tends even to His stray sheep. I am He whom you once served in purity, before pride led you astray.<br>",

            "Ambrosio fell to his knees. “Lord, why do You now appear, only to witness my torment?”<br>",

            "The light warmed, casting a golden glow.<br>",

            "<b>God:</b> Even in your vilest acts, I did not forget you. I am merciful and offer you a chance to repent.<br>",

            "Ambrosio’s voice faltered. “Repent? After all I have done? My crimes—”<br>",

            "<b>God:</b> Your sins are grievous, Ambrosio, but my mercy is unmeasured. You wronged those placed under your care, defiled innocence, and made others tools of your desires. "
            "Do you understand the depth of your trespass?<br>",

            "Ambrosio bowed his head. “I do, my Lord. Their faces haunt me. Their suffering brands my very soul.”<br>",

            "<b>God:</b> Then hear My will. You will return to the mortal realm—not to live, but to confront the truth of your actions. You will revisit the women you wronged. Through their stories, "
            "you will create a painting—as a testament of your sins. This painting will serve as a warning to other men tempted by Lucifer. It will stand as a reminder of the cost of sin, "
            "and the destruction wrought by turning from My path. Completing this painting will be your task to enter purgatory. Should you fail, you will return here to burn for eternity.<br>",

            "Ambrosio shuddered, the weight of the task pressing upon him. “How can I face them, my Lord? How can I bear their judgment? Those wretched insensible women!”<br>",

            "<b>God:</b> You will see them as they were, as you made them. The truth will guide your hand to paint a work that captures not only their suffering, but your role in their fall.<br>",

            "The light began to fade. Before it vanished, the voice spoke one final time:<br>",

            "<b>God:</b> Ambrosio, will you face your sins and repent to stay in purgatory for the rest of your life?<br>",

            "The monk trembled, then bowed his head.<br>",

            "\"Yes.\"<br>"
        ]
        self.location_interaction_completed = {
            'elvira': False,
            'matilda': False,
            'antonia': False
        }

        self.game_state = 'start'  # Start in the 'start' phase
        self.workbench_step = 0  # Initialize the workbench step counter
        self.used_items = []
        self.on_complete = None  # Initialize on_complete callback
        self.keypress_ready = True  # Ensures we only handle keypresses after a short delay
        
    def start_screen(self):
        # Create the start button screen
        self.start_widget = QWidget()
        self.setCentralWidget(self.start_widget)
        
        start_layout = QVBoxLayout()
        start_layout.setAlignment(Qt.AlignCenter)
        
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        
        start_layout.addWidget(self.start_button)
        self.start_widget.setLayout(start_layout)
    
    def start_game(self):
        # Set up the main game screen
        self.play_widget = QWidget()
        self.setCentralWidget(self.play_widget)

        # Initialize inventory and ungrabbed items
        self.inventory = []  # Start with an empty inventory

        # Map locations to available items and their associated images
        self.location_items = {
            'purgatory': {},
            'elvira': {'black': get_resource_path('black.pdf')},
            'antonia': {'red': get_resource_path('red.pdf'), 'white': get_resource_path('white.pdf')},
            'matilda': {'sable': get_resource_path('full.pdf'), 'gold': get_resource_path('gold.pdf'), 'rose': get_resource_path('rose.pdf')}
        }

        # Initialize locations
        self.locations = ['purgatory', 'elvira', 'matilda', 'antonia']
        self.current_location = 'purgatory'  # Starting location

        # Create a splitter to dynamically resize top and bottom sections
        self.splitter = QSplitter(Qt.Vertical)

        # Output area (80% of height)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("background-color: black; color: white; padding-left: 10px; padding-right: 5px;")
        self.output_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Remove vertical scrollbar
        self.output_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Remove horizontal scrollbar
        self.splitter.addWidget(self.output_area)

        # Input area (20% of height)
        self.input_line = QLineEdit()
        self.input_line.setMaxLength(30)
        self.input_line.setPlaceholderText("Enter command here...")
        self.input_line.setStyleSheet("background-color: lightgrey; color: black; padding-left: 10px;")
        self.input_line.returnPressed.connect(self.process_input)
        self.splitter.addWidget(self.input_line)

        # Adjust the initial splitter ratio
        self.splitter.setSizes([int(self.height() * 0.8), int(self.height() * 0.2)])

        # Set layout with splitter
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        self.play_widget.setLayout(layout)

        # Start the click-through sequence for the introduction
        self.click_through_text(self.intro_paragraphs, next_state='main', on_complete=self.start_main_game)

    def update_output(self, text, image_path=None):
        self.output_area.moveCursor(QTextCursor.End)
        if image_path:
            self.output_area.insertHtml(f'<img src="{image_path}" width="300"><br>')
        else:
            self.output_area.insertHtml(f'{text}<br>')
        self.output_area.moveCursor(QTextCursor.End)

    def process_input(self):
        user_input = self.input_line.text().strip().lower()
        self.input_line.clear()

        if not user_input:
            return

        # Display the user input in grey
        if user_input:  # Only display if input is not empty
            self.update_output(f"<span style='color:gray;'>{user_input}</span><br>")

        # If in main game state, process the main game commands
        if self.game_state == 'main':
            # Split command into parts, handle multiple spaces
            parts = user_input.split()
            command = parts[0].lower() if parts else ""

            # Validate the command
            valid_commands = ['show', 'list', 'grab', 'help', 'move', 'current', 'use']
            if command not in valid_commands:
                self.update_output(f'<span style="color:black;">{command} is not a valid command.</span><br>')
                return

            # Validate 'use' command
            if command == 'use' and len(parts) > 1 and parts[1].lower() == 'easel':
                if self.current_location == 'purgatory':
                    if len(self.inventory) == 6:
                        self.click_through_text(
                            self.end_paragraphs1,
                            next_state='main',
                            on_complete=lambda: self.show_undetailed_pdf_then_continue()
                        )
                    else:
                        self.update_output("You need exactly 6 colors in your inventory to use the easel.<br>")
                else:
                    self.update_output("The easel is in purgatory. Please use command 'move to purgatory' first.<br>")
                    
            # Handle 'help' command
            if command == 'help':
                self.update_output('Welcome to COLOURFUL WOMEN IN AMBROSIO’S LIFE!<br><br>' +
                            'Instructions:<br>' + 
                            'Use commmand \'move to\' followed by a reachable location to move there. Ex. \'move to elvira\'<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Valid locations: <b>\'purgatory\'</b> for Purgatory, <b>\'elvira\'</b> for Elvira\'s Apartment,<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>\'matilda\'</b> Matilda in the Monestary, and <b>\'antonia\'</b> for Antonia\'s Tomb<br>' +
                            'Use command \'current location\' to print out the current location of the player<br>' +
                            'Use command \'grab\' followed by a reachable colour to grab the colour and add it to your inventory  (note, items are bolded)<br>' +
                            'Use command \'list items\' to print out a list of all items held in the inventory, and all colours available to grab<br>' +
                            'Use command \'show\' followed by an item in your inventory name to view it<br>' +
                            'Use command \'use easel\' while in purgatory to try painting<br>' +
                            'Use command \'help\' to print out these instructions once again<br><br>')
                return

            # Handle 'current location' command
            if command == 'current' and len(parts) > 1 and parts[1].lower() == 'location':
                full_location_name = self.location_full_names.get(self.current_location, self.current_location)
                self.update_output(f"You are currently at {full_location_name}.<br>")
                return
            elif command == 'current':
                self.update_output("Invalid syntax. Use 'current location'.<br>")
                return

            # Handle 'grab' command
            if command == 'grab':
                item_name = " ".join(parts[1:])  # Combine the rest into the item name
                available_items = self.location_items.get(self.current_location, {})
                if item_name in available_items:
                    # Safely retrieve the file name
                    image_file = available_items[item_name]
                    # Add item to inventory and remove from location
                    self.inventory.append((item_name, image_file))
                    del self.location_items[self.current_location][item_name]
                    self.update_output(f"You grabbed {item_name}.<br>")
                    self.show_pdf(image_file)  # Automatically display the item after grabbing
                    # Check if enough colours acquired
                    if len(self.inventory) == 6:
                        self.update_output("You now have 6 items in your inventory. Return to purgatory and investigate the painting easel.<br>")
                elif any(i[0] == item_name for i in self.inventory):
                    self.update_output(f"{item_name} is already in your inventory!<br>")
                else:
                    self.update_output(f"There is no colour '{item_name}' to grab at this location.<br>")
                return

            # Handle 'list items' command
            if command == 'list':
                if len(parts) == 2 and parts[1] == 'items':
                    if self.inventory:
                        inventory_items = ', '.join(item[0] for item in self.inventory)
                        self.update_output(f"Items in your inventory: {inventory_items}<br>")
                    else:
                        self.update_output("Your inventory is empty.<br>")
                    location_items = self.location_items.get(self.current_location, {})
                    if location_items:
                        location_items_list = ', '.join(location_items.keys())
                        self.update_output(f"Items available at this location: {location_items_list}<br>")
                    else:
                        self.update_output("No items available to grab at this location.<br>")
                    return
                else:
                    self.update_output(f"'list' is not a valid command. Did you mean 'list items'?<br>")
                return

            # Handle 'show' command
            if command == 'show':
                item_name = " ".join(parts[1:])  # Combine the rest into the item name
                for inv_item, image_file in self.inventory:
                    if inv_item == item_name:
                        self.update_output(f"Showing {item_name}.<br>")
                        self.show_pdf(image_file)
                        return
                self.update_output(f"You do not have '{item_name}' in your inventory.<br>")
                return

            # Handle 'move to' command
            if command == 'move' and len(parts) > 1 and parts[1].lower() == 'to':
                location = " ".join(parts[2:])  # Combine remaining parts into the location name
                if location in self.locations:
                    if location == self.current_location:
                        self.update_output(f"You are already at {location}!<br>")
                    else:
                        self.enter_area(location)
                else:
                    self.update_output(f"{location} is not a valid location.<br>")
                return
            elif command == 'move':
                self.update_output(f"Invalid syntax. Use 'move to {location}'.<br>")
                return
        
        elif self.game_state == 'question_answer':
            self.handle_question_answer_input(user_input)

        else: self.update_output("Invalid game state. Please restart the game.<br>")

    def list_inventory(self):
        available_items = [item[0] for item in self.inventory if item[0] not in self.used_items and item[0] not in ['potion', 'sonnets', 'map']]
        if available_items:
            inventory_items = ', '.join(available_items)
            self.update_output(f"Your available inventory: {inventory_items}<br>")
        else:
            self.update_output("No items are currently available for selection.<br>")

    def enter_area(self, location):
        self.current_location = location

        if location == 'purgatory':
            full_location = 'Purgatory'
        elif location == 'elvira':
            full_location = 'Elvira\'s Apartment'
        elif location == 'matilda':
            full_location = 'Matilda in the Monestary'
        elif location == 'antonia':
            full_location = 'Antonia\'s Tomb'

        self.update_output(f"You have arrived at {full_location}.<br>")

        if location == 'purgatory':
            self.update_output(
            "The air was heavy and still, smothering all light. Beneath your feet lay soft, green grass, vibrant yet incongruous in the suffocating gloom. Beyond it, nothing remained—only "
            "endless darkness stretching into the void. A thick mist wrapped the world, cloaking everything. A single beam of pale light broke through, casting long, jagged shadows around "
            "you.The silence pressed heavily, a suffocating weight broken now and then by faint, ghostly murmurs that seemed to rise from unseen depths. The air tasted of despair and decay, "
            "each breath a struggle. Time and direction vanished in the fog.<br>"
            )
        
        elif location == 'elvira':
            suppress_prompt = self.location_interaction_completed['elvira']
            self.click_through_text([
                "You are transported to a small, modest bedroom—the sanctuary of Antonia’s innocence and Elvira’s protection. The faint scent of flowers mingles with the crisp, clean air that "
                "flows through pale curtains swaying gently at the window. A soft glow from the candlestick on the wooden table flickers, casting warm light over the neatly made bed with its "
                "pristine white sheets, where Antonia lies peacefully asleep. The faint creak of the floor beneath you and the fragile clink of the rosary add to the stillness. Yet, the sweetness "
                "of the space is tainted by a heavy sadness, as if the room itself remembers the tragedy that will unfold.<br>",

                "<b>God:</b> This was a place of innocence, a refuge of love and devotion. Yet you, Ambrosio, turned it into a site of violence and betrayal. Look upon what was once whole, and see what you have destroyed.<br>",

                "The air thickens as the scene before you shifts. A memory begins to unfold, and you are forced to relive the moment of Elvira’s death. Her terrified voice fills the room as the events play out before your eyes:<br>",

                "“Terrified at the fury which flashed in his eyes, and at the tremendous threats which He uttered, Elvira sank upon her knees and besought his mercy in terms the most pathetic "
                "and touching. Unmoved by her sorrow and finding his threats unavailing, the Barbarian resolved to silence her complaints forever. Rushing upon her, He clasped his hands round "
                "her throat, and pressing it with his utmost strength, He persisted in his attempt till her voice was for ever silenced. Her lifeless and disfigured body fell motionless at his "
                "feet. He gazed upon it with horror. A frightful blackness spread itself over her visage; her limbs moved no more; the blood was chilled in her veins, and her heart had forgotten to beat.”<br>"
                "<i>(The Monk, Page 160)</i><br>",

                "The memory fades, and the room transforms. The bed is unmade, its sheets darkened by shadow. A shattered vase spills petals across the floor, symbols of innocence destroyed. "
                "Elvira’s lifeless body lies before you, her face consumed by a 'frightful blackness.'<br>",

                "<b>God:</b> Her face, marred by the blackness of death, reflects your betrayal and violence. This darkness is not only hers—it is the shadow of your soul. Look upon it and confront what you have done.<br>"
            ], next_state='main', on_complete=lambda: self.start_question_for_location(
                location=location,
                intro="Which commandment did you break by taking her life?",
                options=[
                    "(a) You shall not steal.",
                    "(b) You shall have no other gods before me.",
                    "(c) You shall not murder."
                ],
                correct_answer='c',
                outro=(
                    "The room darkens further, and Elvira’s voice echoes, filled with sorrow:<br>"
                    "“The <b>blackness</b> that mars my face is the mark of your betrayal. You extinguished my life, leaving only shadows in your wake. Carry this <b>blackness</b> with you—it is yours now.”<br>"
                )
            ), skip_final_prompt=suppress_prompt)
        
        elif location == 'matilda':
            suppress_prompt = self.location_interaction_completed['matilda']
            self.click_through_text([
            "You enter the monastery’s library, where dim candlelight dances across towering shelves of ancient books. The air is thick with the weight of past sins, "
            "carrying the faint scent of incense mingled with a darker, sour trace of decay. At the center stands a grand desk, draped in a sable cloth embroidered "
            "with golden symbols, its surface seeming to absorb the flickering light. The silence is oppressive, broken only by the distant creak of old wood, as "
            "though the room itself mourns what was lost here.<br>",

            "<b>God:</b> “Here is where your path began to twist, Ambrosio. Within these walls, you let yourself be blinded by her golden promises and consumed by the shadows she cast. "
            "Watch now, and see the truth of what you chose.”<br>",

            "The room grows brighter as a memory takes form. You see Matilda standing before you, cloaked in a long sable robe, the dark fabric flowing like a shadow across the floor. "
            "Her eyes gleam with power, and her voice is soft yet commanding:<br>",

            "“She was now cloathed in a long sable Robe, on which was traced in gold embroidery a variety of unknown characters. Her hair was loose and flowed wildly upon her shoulders; "
            "Her eyes sparkled with terrific expression; and her whole demeanor was calculated to inspire the beholder with awe and admiration.”<br>"
            "<i>(The Monk, Page 145)</i><br>",

            "Matilda speaks:<br>",

            "“You are meant for so much more than these vows, Ambrosio. Let go of your chains, and I will lead you to power and freedom beyond your imagination.”<br>",

            "The shadows of her robe spread through the room, dimming the light and suffocating the space in sable darkness.<br>",

            "<b>God:</b> The sable she wore was no mere garment, Ambrosio. It was the shadow of destruction, the darkness you allowed into your soul. See it now for what it was.<br>",

            "As the shadows fade, the golden embroidery on Matilda’s robe begins to glow, illuminating her flowing hair. The memory shifts, and you see her step closer, her golden hair "
            "gleaming in the candlelight, almost angelic in its brilliance.<br>",

            "“What was his amazement at beholding the exact resemblance of his admired Madona? The same exquisite proportion of features, the same profusion of golden hair, the same rosy lips, "
            "heavenly eyes, and majesty of countenance adorned Matilda!”<br>"
            "<i>(The Monk, Page 44)</i><br>",

            "<b>God:</b> You saw her golden beauty, her rosy cheeks, and her sable robe, and you chose them over your vows as a monk. You desired what was not yours to take, and in doing so, "
            "you broke My law. Tell me, Ambrosio: which commandment did you violate here?”<br>"
        ], next_state='main', on_complete=lambda: self.start_question_for_location(
                location=location,
                intro="Which commandment did you break by desiring her beauty, her promises, and her power?",
                options=[
                    "(a) You shall not bear false witness.",
                    "(b) You shall not covet.",
                    "(c) You shall not steal."
                ],
                correct_answer='b',
                outro=(
                    "“You shall not covet. By longing for her promises of power, <b>golden</b> beauty, <b>rosy</b> cheeks, and <b>sable</b> robes you abandoned righteousness and gave yourself to pride and desire.”<br>"
                )
            ), skip_final_prompt=suppress_prompt)
        
        elif location == 'antonia':
            suppress_prompt = self.location_interaction_completed['antonia']
            self.click_through_text([
                "The vision sharpens, revealing the bustling interior of the monastery’s chapel. The faint murmur of prayers and rustling robes fills the air, mingling with the heavy scent of incense. "
                "Among the congregation, Ambrosio’s gaze locks on Antonia. She stands beside her mother, her delicate figure framed by a flowing white gown fastened with a pale blue sash. Her golden ringlets "
                "cascade softly down her back, catching the warm glow of candlelight, and her face is veiled in quiet reverence. Her modest movements and downcast eyes exude an air of angelic purity.<br>",

                "<b>God:</b> Here is where you first saw her, Ambrosio. A soul filled with faith, her heart untainted by sin. But you did not see her devotion. You saw only her innocence, "
                "and in your heart, you sought to claim it.<br>",

                "His eyes lingered, drawn not to her prayer but to the fragile beauty that accompanied it. Her modesty, her reverence—each movement spoke of a soul untainted, yet to Ambrosio, "
                "they were invitations rather than virtues. She seemed almost unearthly, a vision set apart from the rest of the congregation, untouched by the world’s cruelties.<br>",

                "“It was of the most dazzling whiteness, and received additional charms from being shaded by the tresses of her long fair hair, which descended in ringlets to her waist. "
                "Her bosom was carefully veiled. Her dress was white; it was fastened by a blue sash, and just permitted to peep out from under it a little foot of the most delicate proportions.”<br>"
                "<i>(The Monk, pg 4)</i><br>",

                "<b>God:</b> You saw her white gown, her modesty, her gentle prayers. But instead of guiding her, you let your heart be consumed by covetous desire.<br>",

                "As her delicate figure shimmered in the soft light of the church, her innocence glowing like a beacon, the vision began to shift. The warmth of the chapel faded, and a suffocating darkness enveloped the space. "
                "The faint scent of incense was replaced by the damp, acrid stench of decay. You find yourself in the cold, oppressive confines of a tomb. Rough-hewn stone walls press inward, and the faint drip of water echoes "
                "through the silence, mingling with the muffled cries of distant anguish. A single torch flickers weakly, its light casting jagged shadows across the chamber.<br>",

                "Before you lies Antonia, trembling, her white gown now stained and torn, a fragile figure surrounded by darkness. The air feels heavy with dread, and her quiet sobs pierce the silence, pleading for mercy that will not come.<br>",

                "Then the memory sharpens, pulling you into the violent moment:<br>",

                "“Quickened by her cries, the sound of footsteps was heard approaching. The Abbot expected every moment to see the Inquisitors arrive. Antonia still resisted, and He now enforced her silence by means the most horrible and inhuman. "
                "He still grasped Matilda's dagger: Without allowing himself a moment's reflection, He raised it, and plunged it twice in the bosom of Antonia! She shrieked, and sank upon the ground. The Monk endeavoured to bear her away with him, "
                "but She still embraced the Pillar firmly. At that instant the light of approaching Torches flashed upon the Walls. Dreading a discovery, Ambrosio was compelled to abandon his Victim, and hastily fled back to the Vault, where He had left Matilda.”<br>"
                "<i>(The Monk, Page 204)</i><br>",

                "The vision lingers on Antonia’s lifeless form, her blood pooling on the cold stone floor, her once-white gown now soaked in red. The torchlight flickers as though struggling to endure the weight of the scene, "
                "casting her face into shadow—a haunting reminder of innocence stolen and a soul betrayed.<br>"
            ], next_state='main', on_complete=lambda: self.start_question_for_location(
                location=location,
                intro="Which commandment did you break by coveting Antonia’s purity and murdering her?",
                options=[
                    "(a) You shall not covet, and you shall not murder.",
                    "(b) You shall not bear false witness, and you shall not steal.",
                    "(c) Honor your father and mother."
                ],
                correct_answer='a',
                outro=(
                    "You shall not covet. By desiring what was not yours to take, you turned her innocence into your ruin.<br>"
                    "The vision fades, leaving the tomb shrouded in shadow. The white</b> of Antonia’s gown glows faintly, a ghostly remnant of her purity, while the crimson of her blood spreads across the stone, vivid and inescapable.<br>"
                    "Her voice echoes softly, filled with sorrow:<br>"
                    "“<b>White</b> for my innocence, Ambrosio. <b>Red</b> for the pain you caused. These colors are yours now, a mark of the life you took and the purity you mercilessly coveted.”<br>"
                )
            ), skip_final_prompt=suppress_prompt)

    def start_question_for_location(self, location, intro, options, correct_answer, outro):
        """
        Start the question-answer sequence for the given location only if it hasn't been completed.
        """
        if not self.location_interaction_completed[location]:
            self.question_answer_state(intro, options, correct_answer, outro)
        else:
            # No action needed, as the click-through text has already been displayed
            pass

    def start_main_game(self):
        # Transition to the main game loop
        self.update_output('Welcome to COLOURFUL WOMEN IN AMBROSIO’S LIFE!<br><br>' +
                            'Instructions:<br>' + 
                            'Use commmand \'move to\' followed by a reachable location to move there. Ex. \'move to elvira\'<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Valid locations: <b>\'purgatory\'</b> for Purgatory, <b>\'elvira\'</b> for Elvira\'s Apartment,<br>' +
                            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>\'matilda\'</b> Matilda in the Monestary, and <b>\'antonia\'</b> for Antonia\'s Tomb<br>' +
                            'Use command \'current location\' to print out the current location of the player<br>' +
                            'Use command \'grab\' followed by a reachable colour to grab the colour and add it to your inventory  (note, items are bolded)<br>' +
                            'Use command \'list items\' to print out a list of all items held in the inventory, and all colours available to grab<br>' +
                            'Use command \'show\' followed by an item in your inventory name to view it<br>' +
                            'Use command \'use easel\' while in purgatory to try painting<br>' +
                            'Use command \'help\' to print out these instructions once again<br><br>')
        self.enter_area('purgatory')  # Enter the initial location

    def show_pdf(self, pdf_path):
        """
        Show the given PDF file in the default system viewer.
        :param pdf_path: Relative file path to the PDF
        """
        full_path = get_resource_path(pdf_path)

        # Ensure the file exists
        if os.path.exists(full_path):
            # Open the PDF with the default system viewer
            os.system(f'open "{full_path}"')  # macOS/Linux
            # For Windows, use os.system(f'start "" "{full_path}"')
        else:
            self.update_output("<span style='color:black;'>PDF not found!</span><br>")

    def keyPressEvent(self, event):
        if self.game_state == 'reading':
            self.handle_reading_keypress()
            return

        # Default behavior for other key press events
        super().keyPressEvent(event)

    def click_through_text(self, text_array, next_state='main', on_complete=None, skip_final_prompt=False):
        """
        Initiates a click-through text sequence, allowing the user to progress through an array of strings.
        """
        self.text_sequence = text_array  # Store the text sequence to display
        self.text_index = 0  # Start at the first text in the sequence
        self.next_state = next_state  # State to switch to after the sequence ends
        self.on_complete = on_complete  # Store the completion callback
        self.skip_final_prompt = skip_final_prompt  # Whether to suppress the final prompt

        self.input_line.setEnabled(False)  # Disable input
        self.game_state = 'reading'  # Set game state to 'reading'
        self.keypress_ready = False  # Disable keypress handling temporarily

        # Display the first piece of text
        self.update_output(self.text_sequence[self.text_index] + "<br>")
        # Display "Press any key" prompt if there are more items
        if len(self.text_sequence) > 1 or not self.skip_final_prompt:
            self.update_output("<span style='color:gray;'>Press any key (except spacebar) to continue...</span><br>")

        # Re-enable keypress handling after a short delay
        QTimer.singleShot(100, lambda: setattr(self, 'keypress_ready', True))
        
    def handle_reading_keypress(self):
        """
        Handles keypress events during the 'reading' game state.
        Advances through the text sequence or ends the sequence if complete.
        """
        if not self.keypress_ready:
            return  # Ignore keypress if not ready

        self.keypress_ready = False  # Disable keypress handling until the next text is displayed
        self.text_index += 1  # Move to the next text in the sequence

        if self.text_index < len(self.text_sequence):
            # Display the next text
            self.update_output(self.text_sequence[self.text_index] + "<br>")
            # Show the prompt only if it's not the last piece of text or skip_final_prompt is False
            if self.text_index < len(self.text_sequence) - 1 or not self.skip_final_prompt:
                self.update_output("<span style='color:gray;'>Press any key (except spacebar) to continue...</span><br>")
            self.keypress_ready = True  # Re-enable keypress handling for the next item
        else:
            # End the sequence
            self.text_sequence = []  # Clear the text sequence
            self.text_index = 0  # Reset the index

            self.input_line.setEnabled(True)  # Re-enable input
            self.game_state = self.next_state  # Transition to the next state

            # Execute the callback if provided
            if self.on_complete:
                self.on_complete()

    def end_game_message(self):
        self.update_output("The story has concluded. Thank you for playing my game! You can now read over the story, or exit the game.<br>")
        self.input_line.setEnabled(False)  # Disable input field

    def question_answer_state(self, intro, options, correct_answer, outro):
        """
        Handles a question-answer interaction state.
        :param intro: A string that introduces the question to the user.
        :param options: A list of 3 strings representing the possible answers.
        :param correct_answer: A character ('a', 'b', or 'c') that is the correct answer.
        :param outro: A string to display once the correct answer is given.
        """
        # Store the parameters for use during the question/answer interaction
        self.question_intro = intro
        self.question_options = options
        self.correct_answer = correct_answer.lower()
        self.question_outro = outro

        # Initialize the state and display the question
        self.game_state = 'question_answer'
        self.update_output(f"{self.question_intro}<br>")
        for option in self.question_options:
            self.update_output(f"{option}<br>")
        self.update_output("<span style='color:gray;'>Enter 'a', 'b', or 'c' to answer.</span><br>")

    def handle_question_answer_input(self, user_input):
        """
        Handles user input during the question-answer interaction state.
        :param user_input: The input from the user.
        """
        user_answer = user_input.strip().lower()

        # Check if the answer is correct
        if user_answer == self.correct_answer:
            self.update_output(f"{self.question_outro}<br>")
            
            # Mark the location as completed
            for location, completed in self.location_interaction_completed.items():
                if not completed and self.current_location == location:
                    self.location_interaction_completed[location] = True
                    break

            # Return to the main state
            self.game_state = 'main'
        elif user_answer in ['a', 'b', 'c']:
            # Incorrect answer, prompt the user to try again
            self.update_output("Incorrect answer. Please try again. Enter 'a', 'b', or 'c'.<br>")
        else:
            # Invalid input
            self.update_output("Invalid input. Please enter 'a', 'b', or 'c'.<br>")

    def check_for_six_colors(self):
        """
        Check if the user has 6 colors in their inventory and return a boolean.
        """
        colors_in_inventory = [item for item, _ in self.inventory if item not in ['empty canvas', 'potion', 'sonnets', 'map']]
        return len(colors_in_inventory) == 6

    def post_purgatory_check(self):
        """
        Check for the painting prompt after the purgatory click-through sequence.
        """
        if self.check_for_six_colors():
            self.update_output("You have gathered all six colors. Use command 'use easel' to paint and complete your journey.<br>")

    def post_location_check(self, suppress_prompt):
        """
        Check for the "head to purgatory" prompt after other location click-through sequences.
        """
        if self.check_for_six_colors() and not suppress_prompt:
            self.update_output("You have gathered all six colors. Head to Purgatory and use the easel to paint.<br>")

    def show_undetailed_pdf_then_continue(self):
        """Show the undetailed PDF and start the next text sequence."""
        self.show_pdf("undetailed_full.pdf")
        self.click_through_text(
            self.end_paragraphs2,
            next_state='main',
            on_complete=lambda: self.show_full_pdf_then_continue()
        )

    def show_full_pdf_then_continue(self):
        """Show the full PDF and start the final text sequence."""
        self.show_pdf("full_w_poem.pdf")
        self.click_through_text(
            self.final_text,
            next_state='ended',
            on_complete=self.end_game_message
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = AdventureGame()
    game.show()
    sys.exit(app.exec_())
